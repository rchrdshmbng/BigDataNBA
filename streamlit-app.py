#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Hooponomics: The NBA Player Value Predictor", page_icon="🏀", initial_sidebar_state="expanded")

##########################################
##  Load and Prep Data                  ##
##########################################

@st.cache
def load_and_prep_players():
    dfplayers = pd.read_csv('data/app_dfplayers.csv')
    marketvalue_dict = {0:'0-5', 5:'5-10',10:'10-15',15:'15-20',20:'20-25',25:'25-30', 30:'30+'}
    dfplayers['Market Value ($M)'] = dfplayers['Sal_class_predict'].apply(lambda val: marketvalue_dict[val])
    dfplayers['Salary ($M)'] = dfplayers['SalFinal'].round(1).apply(lambda val:'<2' if val < 2 else val).astype(str)
    dfplayers['Surplus Value ($M)'] = dfplayers['Surplus_value'].round(1).apply(lambda val:'0' if val == 0 else val).astype(str)
    dfplayers['Height'] = dfplayers['Height'].apply(lambda val: val.split('-')[0] + "'" + val.split('-')[1] + "\"" )
    dfplayers['Weight'] = dfplayers['Weight'].apply(lambda val: str(val) + ' lb')
    dfplayers['Position'] = dfplayers['Pos']
    dfplayers = dfplayers.set_index('Name', drop=False)
    return dfplayers

@st.cache
def load_and_prep_teams():
    dfteams = pd.read_csv('data/app_dfteams.csv')
    team_to_tm = {k:v for k,v in zip(dfteams['Team_Name'],dfteams['Team'])}
    dfteams = dfteams.rename(columns={"Team":"Tm", "Team_Name":"Team", "Surplus_value":"Net Surplus Value ($M)"})
    return dfteams, team_to_tm

dfplayers = load_and_prep_players()
dfteams, team_to_tm = load_and_prep_teams()

cols = ['Name','Team','Position', 'Age', 'Height', 'Weight', 'Salary ($M)','Market Value ($M)', 'Surplus Value ($M)',]


##########################################
##  Style and Formatting                ##
##########################################

# CSS for tables

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>   """

center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """
    
center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True) 
st.markdown(center_row_text, unsafe_allow_html=True) 

# More Table Styling

def color_surplusvalue(val):
    if str(val) == '0':
        color = 'azure'
    elif str(val)[0] == '-':
        color = 'lightpink'
    else:
        color = 'lightgreen'
    return 'background-color: %s' % color

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                      ('color', 'black'),  ('font-weight', 'bold'),
                      ('background', '#c5c2ef'),('border', '1.2px solid')]

#set font color to black for all cells
cell_properties = [('font-size', '16px'),('text-align', 'center'),('color','black')]

dfstyle = [{"selector": "th", "props": heading_properties},
               {"selector": "td", "props": cell_properties}]

# Expander Styling

st.markdown(
    """
<style>
.streamlit-expanderHeader {
 #   font-weight: bold;
    background: aliceblue;
    font-size: 18px;
    color: black;
}
</style>
""",
    unsafe_allow_html=True,
)

    
  

##########################################
##  Title, Tabs, and Sidebar            ##
##########################################

st.title("Hooponomics: The NBA Player Value Predictor")
st.markdown('''##### <span style="color:gray">Predicting NBA players' market value based on their statistical performance</span>
            ''', unsafe_allow_html=True)
                
tab_player, tab_team, tab_explore, tab_guide = st.tabs(["Player Lookup", "Team Lookup", "Explore", "Guide"])

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('figures/playerphoto.jpg',  use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown(" ## About Hooponomics")
st.sidebar.markdown("The Hooponomics prediction model places each current NBA player into one of seven market value classes, reflecting the expected yearly salary range if they were to sign a new contract at the end of the 2021-22 season.  It was trained on free agent data from the preceding five years, using a curated set of basic player stats and advanced metrics."  )

##########################################
## Player Tab                           ##
##########################################

with tab_player:
    player = st.selectbox("Choose a player (or click below and start typing):", dfplayers.Name, index =508)
    
    player_pos = dfplayers[dfplayers.Name == player].Pos.to_list()[0]
    player_sal_class_predict = dfplayers[dfplayers.Name == player].Sal_class_predict.to_list()[0]
    player_max_proba = dfplayers[dfplayers.Name == player].Max_proba.to_list()[0]          
    player_salary = dfplayers[dfplayers.Name == player]['Salary ($M)'].to_list()[0]
    if player_salary == '<2':
        player_salary = '<$2M'
    else:
        player_salary = '$' +  player_salary + 'M'   
    player_marketvalue = dfplayers[dfplayers.Name == player]['Market Value ($M)'].to_list()[0]
    if player_marketvalue == '30+':
        player_marketvalue = '$30M+'
    else:
        player_marketvalue = '$' +  player_marketvalue + 'M'
    player_url = 'https://www.basketball-reference.com' + dfplayers[dfplayers.Name == player]['ID'].to_list()[0]                   
    
    st.write(f'''
         ##### <div style="text-align: center"> In the 2021-22 NBA season, <span style="color:blue">[{player}]({player_url})</span> earned a salary of <span style="color:blue"> {player_salary}   </span> </div>
         
          ##### <div style="text-align: center"> According to our model, his market value was <span style="color:blue">{player_marketvalue}</span> </div>
         ''', unsafe_allow_html=True)
    
    styler_player = (dfplayers[dfplayers.Name == player][cols]
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle)
                   .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']]))
    st.table(styler_player)
    
    
    st.markdown('''#### Most Similar Players:''', unsafe_allow_html=True)

    df_mostsimilar = (dfplayers[(dfplayers.Name != player) & (dfplayers.Sal_class_predict == player_sal_class_predict)
                              &  (dfplayers.Pos == player_pos) ]
                               .sort_values(by='Max_proba', key=lambda col: np.abs(col-player_max_proba))[cols][:10])

    styler_mostsimilar = (df_mostsimilar.style
                          .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                          .hide(axis='index')
                          .set_table_styles(dfstyle)
                          .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])
                         )                                                  
    st.table(styler_mostsimilar)
    
    st.success('''**Note on Our Algorithm:**  

The machine learning model deployed in this app is a Random Forest 
Classifier that uses the following information to predict a player's market value: Games Played, Games Started, 
Minutes Per Game, Points Per Game, Usage Percentage, Offensive Box Plus/Minus (OBPM), Value Over Replacement Player (VORP), 
and Win Shares (WS), all scraped from [Basketball Reference](http://www.basketball-reference.com).  

The seven market value classes used were:  \$0-5M, \$5-10M, \$10-15M, \$15-20M, \$20-25M, \$25-30M, and $30M+.  In keeping with best data science practices, the model was trained and fine-tuned on player data from previous years and was not exposed to any data from the 2021-22 NBA season before generating these predictions.''')

    
##########################################
## Team Tab                             ##
##########################################    
    
with tab_team:
    team = st.selectbox("Choose a team (or click below and start typing):", dfteams.Team, index=1)
   
    styler_team = (dfplayers[dfplayers.Team == team_to_tm[team]][cols].style
                          .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                          .hide(axis='index')
                          .set_table_styles(dfstyle)
                          .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])                                                    )
    st.table(styler_team)
    
    st.success('''**A Brief Note on Methods:**  

The machine learning model deployed in this app is a Random Forest 
Classifier that uses the following information to predict a player's market value: Games Played, Games Started, 
Minutes Per Game, Points Per Game, Usage Percentage, Offensive Box Plus/Minus (OBPM), Value Over Replacement Player (VORP), 
and Win Shares (WS), all scraped from [Basketball Reference](http://www.basketball-reference.com).  

The seven market value classes used were: \$0-5M, \$5-10M, \$10-15M, \$15-20M, \$20-25M, \$25-30M, and $30M+.  In keeping with best data science practices, the model was trained and fine-tuned on player data from previous years and was not exposed to any data from the 2021-22 NBA season before generating these predictions.''')

    
##########################################
## Explore Tab                          ##
##########################################
   
with tab_explore:
    #set the font color to black
    st.markdown('<style>div.stButton > button:first-child {color: black;}</style>', unsafe_allow_html=True)
    
    ########## 
    expand_allplayers = st.expander("Most Overvalued/Undervalued Players", expanded=False)
    
    with expand_allplayers:
        
        slider1, slider2 = st.columns([4,10])
        with slider1:
            num_entries = st.slider('Number of players to show:', 0, 30, 5, step =5)
        with slider2:
            st.write('')

        cb1, cb2, cb3, cb4, cb5, cb6, cb7 = st.columns([1,1,1,1,1,1,4])
        with cb1:
            is_all = st.checkbox('All  ', value=True)
        with cb2:
            if is_all:
                is_pg = st.checkbox('PG  ', value=True, disabled=True)
            else:
                is_pg = st.checkbox('PG  ', value=False)
        with cb3:
            if is_all:
                is_sg = st.checkbox('SG  ', value=True, disabled=True)
            else:
                is_sg = st.checkbox('SG  ', value=False)
        with cb4:
            if is_all:
                is_sf = st.checkbox('SF  ', value=True, disabled=True)
            else:
                is_sf = st.checkbox('SF  ', value=False)
        with cb5:
            if is_all:
                is_pf = st.checkbox('PF  ', value=True, disabled=True)
            else:
                is_pf = st.checkbox('PF  ', value=False)
        with cb6:
            if is_all:
                is_c = st.checkbox('C  ', value=True, disabled=True)
            else:
                is_c = st.checkbox('C  ', value=False)
        with cb7:
            st.write('')
           
        position_mask = ((dfplayers.Pos == 'C' if is_c else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'PF' if is_pf else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'PG' if is_pg else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'SG' if is_sg else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'SF' if is_sf else dfplayers.Pos == 'Unicorn') 
                        )
        
        if position_mask.any():
            
            st.markdown('''#### Most Undervalued Players:''', unsafe_allow_html=True)
            
            styler_undervalued = (dfplayers[(dfplayers.Surplus_value > 0) & position_mask]
                                  .sort_values('Surplus_value',ascending=False)[cols][:num_entries]
                                  .style
                                  .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])                                                    )
   
            st.table(styler_undervalued)
    
            st.markdown('''#### Most Overvalued Players:''', unsafe_allow_html=True)
    
            styler_overvalued = (dfplayers[(dfplayers.Surplus_value < 0) & position_mask]
                                  .sort_values('Surplus_value',ascending=True)[cols][:num_entries]
                                  .style
                                  .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])                                                    )
   
            st.table(styler_overvalued)
          
        
    ##########   
    expand_teamvalues = st.expander("Net Surplus Value by Team")
    
    with expand_teamvalues:
                
        teamcol1, teamcol2 = st.columns(2)

        with teamcol1:            
            styler_teamsurplus1= (dfteams[['Team',"Net Surplus Value ($M)"]]
                                  .sort_values("Net Surplus Value ($M)",ascending=False)[0:15]
                                  .style.format(precision=1)   #.style.set_precision(1)
                                  .set_properties(**{'background': 'cornsilk', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ["Net Surplus Value ($M)"]])  
                                 )
            st.table(styler_teamsurplus1)
                                                                                                          
        with teamcol2:
            styler_teamsurplus2= (dfteams[['Team',"Net Surplus Value ($M)"]]
                                  .sort_values("Net Surplus Value ($M)",ascending=False)[15:]
                                   .style.format(precision=1)      #.style.set_precision(1)
                                  .set_properties(**{'background': 'cornsilk', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ["Net Surplus Value ($M)"]])  
                                 )
            st.table(styler_teamsurplus2)

   
            
            
    
    ##########    
    expand_histograms = st.expander("Salaries & Market Values")
    
    with expand_histograms:
        
        st.write('''##### <span style="color:blue"> Distribution of salaries and predicted market values \
                     for all 605 NBA players who played in the 2021-22 season.</span>''', unsafe_allow_html=True)
        
        st.markdown("####  Player Salaries:")
        st.image('figures/salaries.png')
        
        st.markdown("####  Player Market Values:")
        st.image('figures/marketvalues.png')
        
##########################################
## Guide Tab                            ##
##########################################

with tab_guide:

    st.markdown(" ### Our Project Guide 🔎 ")

    ########## 
    guide1 = st.expander('🏀 Player Market Value Estimation: Our Approach')
    with guide1:
        st.write('''Basketball player's salary and his real market value often aren't aligned due to the nature of fixed, multi-year contracts. We leveraged machine learning techniques to predict a player's new contract amount, based on historical data of free agents' performance and salary changes. This model can be retroactively applied to all players to estimate their market value.''')

    ##########
    guide2 = st.expander("🏀 Machine Learning Model Utilized")
    with guide2:
        st.write('''We employed a Random Forest Classifier, an ensemble of Decision Trees, for predicting the market value. The model classifies players into seven salary range groups and ensures balanced representation to avoid bias towards a dominant class.''')

    ##########
    guide3 = st.expander("🏀 Model Training Process")
    with guide3:
        st.write('''The model was trained on the data of free agents from 2015 to 2020, using their stats from their contract's last year. We stratified the data into training, validation, and holdout sets, tuned hyperparameters based on the validation set, and finalized the model on the combined data.''')
    
    ##########
    guide4 = st.expander("🏀 Features Considered by the Model")
    with guide4:
        st.write('''Our model uses eight key stats as input features, encompassing both rate and volume metrics, to provide a comprehensive view of a player's performance. This includes points per game, minutes per game, games started, usage percentage, offensive box plus/minus, value over replacement player, and win shares.''')
    
    ##########
    guide5 = st.expander("🏀 Model Performance")
    with guide5:
        st.write('''Our model achieved an accuracy of 68% on the 2020 holdout set, with misclassifications generally not being extreme outliers. This supports the model's reliability.''')

    ##########
    guide6 = st.expander("🏀 Surplus Value Calculation")
    with guide6:
        st.write('''Surplus value is the conservative difference between a player's market value and his actual salary. It's zero when the salary is within the market value range, and it's the difference when the salary falls outside this range.''')

    ##########
    guide7 = st.expander("🏀 Why is $30M+ the highest class?")
    with guide7:
        st.write('''As per NBA rules, the first year of a new contract can't exceed a range of \$28.1M to \$39.3M. Most teams offer the highest available salary to eligible players, hence we grouped all "max players" into a $30M+ class.''')

    ##########
    guide8 = st.expander("🏀 Determining Similar Players")
    with guide8:
        st.write('''Our Random Forest model, apart from predicting a player's market value, also estimates the probability of this prediction. We used this to find the players most similar to a given player, by comparing these probability estimates.''')

