import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns

sns.set(font_scale=1)
DATA_URL = "https://raw.githubusercontent.com/li-boxuan/streamlit-example/master/house_prices.csv"


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows).drop('Id', axis=1)
    return data


@st.cache(persist=True)
def find_max_corr(df, top_n=2):
    corr = df.corr()['SalePrice'][:].sort_values()
    # drop row with highest correlation, i.e. target value (SalePrice) itself
    corr.drop(corr.tail(1).index, inplace=True)
    return corr.head(top_n).append(corr.tail(top_n))


def draw_correlation_map(df):
    st.write("Correlation map")
    correlation = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation, ax=ax, cmap="YlGnBu", annot=True, fmt=".2f", square=True, annot_kws={"size":8})
    st.pyplot(fig)


st.write("Data in tabular format")
df = load_data(None)
df

df_numeric = df.select_dtypes(include=np.number)
numeric_features = df_numeric.drop("SalePrice", axis=1).columns

top_n = 3
options = st.multiselect(
    'Select features to view correlations (default values: top ' + str(top_n * 2) + ' correlated features)',
    numeric_features,
    find_max_corr(df_numeric, top_n).index.tolist()
)

options.append("SalePrice")
draw_correlation_map(df_numeric[options])

