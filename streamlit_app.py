import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns

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
    return corr.head(top_n).append(corr.tail(top_n))


def draw_correlation_map(df):
    st.write("Correlation map")
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

# Draw correlation heatmap
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


