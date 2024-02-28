# Hooponomics: A Data-Driven Approach to Quantifying NBA Player Value

## Introduction

Hooponomics is an innovative project focused on the world of professional basketball, specifically the National Basketball Association (NBA). The goal of this project is to create an analytical model that can predict the potential value of NBA players. Leveraging data science and machine learning techniques, this project aims to offer insights into contract negotiations, player trading, game analysis, and marketing strategies. 

## Modeling Approach

The modeling approach in Hooponomics is implemented in a systematic and structured manner. It starts with data collection, where we gather player statistics and salary data through web scraping (Refer to `1-scraping.ipynb`). This is followed by data cleaning and preprocessing to ensure data integrity and reliability (Refer to `2-cleaning.ipynb`). After cleaning, the data is used to train a machine learning model, which is developed and evaluated (Refer to `3-modeling.ipynb`). Additional data is gathered and the dataset is prepared for integration into the web application (Refer to `4-preparation.ipynb`).

## Code Information

Our project employs Python as the primary coding language, with the code stored and version-controlled on GitHub. The codebase is organized into different Jupyter notebooks, each with a specific role:

- `1-scraping.ipynb`: This notebook includes a web scraper to gather player statistics and salary data.
- `2-cleaning.ipynb`: This notebook is responsible for data cleaning and preprocessing.
- `3-modeling.ipynb`: Machine learning model is trained and evaluated in this notebook.
- `4-preparation.ipynb`: This notebook gathers additional data and prepares the dataset for integration into the web app.

There is also a Python script (`streamlit-app.py`) that creates an interactive web application using Streamlit, and a data folder (`data/`) that contains various .csv files used as input or output in the notebooks.

## Future Plans

We plan to integrate a reliable API for real-time data of players and teams, adopt Docker containers to accommodate the complexity of the app, and add potential additional features to enhance the project's value and efficiency.
