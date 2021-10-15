import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from bokeh.plotting import figure

sns.set(font_scale=1)
# DATA_URL = "https://raw.githubusercontent.com/li-boxuan/streamlit-example/master/house_prices.csv"
DATA_URL = "./house_prices.csv"
DESC_URL = "./description.csv"


@st.cache(persist=True)
def load_desc():
    return pd.read_csv(DESC_URL, header=None)


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows).drop('Id', axis=1)
    return data


@st.cache(persist=True)
def find_max_corr(df, top_n=2):
    corr = df.corr()['SalePrice'][:].sort_values()
    # drop row with highest correlation, i.e. target value (SalePrice) itself
    corr.drop(corr.tail(1).index, inplace=True)
    top_n_indices = corr.abs().tail(top_n).index
    return top_n_indices


def draw_box_plot(df):
    keywords = df.columns.tolist()
    keywords.remove("YearBuilt")
    keywords.remove("SalePrice")
    keywords = ["SalePrice"] + keywords  # put sale price as the default option
    dependent_var = st.selectbox(
        'View trending of:',
        keywords
    )

    min_year = df["YearBuilt"].min()
    max_year = df["YearBuilt"].max()
    values = st.slider('Select a range of values', min_year, max_year, (1960, 2010))

    df_sub = df[(df["YearBuilt"] <= values[1]) & (df["YearBuilt"] >= values[0])]
    plt.figure(figsize=(40, 20))
    fig, ax = plt.subplots()
    sns.boxplot(x='YearBuilt', y=dependent_var, data=df_sub, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)


def draw_correlation_map(df):
    correlation = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation, ax=ax, cmap="YlGnBu", annot=True, fmt=".2f", square=True, annot_kws={"size":8})
    st.pyplot(fig)


# load data
df = load_data(None)
desc_df = load_desc()

################################
#          Side bar            #
################################
with st.sidebar:
    st.header("Data Overview")
    # Search box to find description of each field
    columns = df.columns.tolist()
    columns = columns[-1:] + columns[:-1]
    keyword = st.selectbox(
        'Find more on:',
        columns
    )

    desc_df.columns = ["keyword", "description"]
    st.write(keyword, ":", desc_df[desc_df["keyword"] == keyword]["description"].tolist()[0])

    if keyword == "SalePrice":
        st.write(df[keyword])
    else:
        # show price together with the feature
        st.write(df[[keyword, "SalePrice"]])

################################
#         Main Panel           #
################################

# Introduction
st.header("What affect a house price?")
st.markdown("Let us explore what the factors of the house price are, using 1500 data points collected in Ames, Iowa, "
            "available on [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques). See if this "
            "gives you any insight on estimating housing prices!")

num_of_features = len(df.columns) - 1
df_numeric = df.select_dtypes(include=np.number)
num_of_numeric_features = len(df_numeric.columns) - 1
num_of_categorical_features = num_of_features - num_of_numeric_features
st.markdown("Out of {} features, {} are numerical features and {} are categorical features.".format(
            num_of_features, num_of_numeric_features, num_of_categorical_features))

# Draw correlation heatmap
st.subheader("How correlated are these values?")

numeric_features = df_numeric.drop("SalePrice", axis=1).columns
top_n = 10
options = st.multiselect(
    'Select features to view correlations (default values: top ' + str(top_n) +
    ' features that are correlated to price)',
    numeric_features,
    find_max_corr(df_numeric, top_n).tolist()
)

options.append("SalePrice")
draw_correlation_map(df_numeric[options])

# Draw boxplot by year
st.subheader("How do houses change over the year (based on built date)?")
draw_box_plot(df_numeric)
