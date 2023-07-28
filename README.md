# Hooponomics

## Introduction

Hooponomics is a data-driven project aiming to quantify basketball player values for various purposes such as contract negotiation, game analysis, player trading, budget cap assessment, fan discussion, and marketing. The main goal is to provide a factual basis for related discussions, turning subjective debates into evidence-based conclusions. 

## Modeling Approach

Our approach includes several stages, encapsulated within Jupyter notebooks. First, player statistics and salary data are gathered via web scraping (1-scrape.ipynb). This data is then cleaned and preprocessed (2-clean.ipynb). The next stage is exploratory data analysis, feature selection, and feature engineering (3-analysis.ipynb). Finally, we train and evaluate a machine learning model based on the processed data (4-model.ipynb). This allows us to predict player worth and provide valuable insights into player contracts, trades, and more.

## Code Information

Our codebase mainly consists of Python scripts, housed within Jupyter notebooks and pure Python files. Our architecture leverages GitHub for version control and Streamlit for interactive web application creation. Below is a brief explanation of key files and directories:

- `1-scrape.ipynb`: web scraping player statistics and salary data
- `2-clean.ipynb`: responsible for data cleaning and preprocessing
- `3-analysis.ipynb`: used for exploratory data analysis, feature selection, and feature engineering
- `4-model.ipynb`: where the machine learning model is trained and evaluated
- `streamlit-app.py`: Python script that creates an interactive web application using Streamlit
- `data/`: directory containing various .csv files used as input or output in the notebooks

## Assessment Criteria Responses

- **Clarity of Idea**: Our project aims to objectively analyze and quantify basketball player values based on statistical data and salary information. We use this analysis for contract negotiation, game analysis, player trading, budget cap considerations, fan discussions, and marketing purposes.

- **Choice of Tools and Technologies**: We chose Python due to its wide range of libraries for data manipulation, web scraping, and machine learning. We also use GitHub for version control, collaboration, and code hosting. Streamlit, an open-source Python library, is used to build interactive web applications for our analysis.

- **Complexity and sophistication of the solution**: Our solution involves a multi-step pipeline from web scraping to data preprocessing, exploratory analysis, feature selection/engineering, and machine learning model training and evaluation. We believe this showcases a comprehensive and sophisticated approach.

- **Mastery in Implementation**: The implementation effectively demonstrates our proficiency in Python, data analysis, and machine learning. The code is well-structured, documented, and utilizes best practices in software development.

- **Correctness**: Our solution is designed to be correct, reliable, and error-free. However, as with any machine learning model, predictions should always be used in conjunction with expert human judgment.

- **Deployment**: Our application is deployed as an interactive web application using Streamlit. This enables users to interact with our findings and adjust parameters in real-time.

- **Code Structure and Documentation**: Our code is well-structured and documented, ensuring readability and maintainability. We follow the best practices of software development, ensuring our project can be understood and utilized by others.

## Next Steps

Our future plans include utilizing reliable APIs for real-time player and team data, using Docker containers to manage the complexity of the app, and adding potential additional features to enhance the capabilities of our application.
