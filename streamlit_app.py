import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import pydeck as pdk

sns.set(font_scale=1)
DATA_URL = "./house_prices.csv"
DESC_URL = "./description.csv"
GPS_URL = "./gps_coordinates.csv"


@st.cache(persist=True)
def load_desc():
    return pd.read_csv(DESC_URL, header=None)


def load_gps_coordinates():
    return pd.read_csv(GPS_URL)


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


def draw_bar_plot(df):
    keywords = df.columns.tolist()
    keywords.remove("SalePrice")
    independent_var = st.selectbox(
        'View estimated price based on category:',
        keywords
    )
    fig, ax = plt.subplots()
    sns.barplot(x=independent_var, y="SalePrice", data=df, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)


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
    values = st.slider('Select a range of years', int(min_year), int(max_year), (1960, 2010))

    df_sub = df[(df["YearBuilt"] <= values[1]) & (df["YearBuilt"] >= values[0])]
    fig, ax = plt.subplots()
    sns.boxplot(x='YearBuilt', y=dependent_var, data=df_sub, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)


def draw_correlation_map(df):
    correlation = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation, ax=ax, cmap="YlGnBu", annot=True, fmt=".2f", square=True, annot_kws={"size":8})
    st.pyplot(fig)


def draw_map(df_gps, df):
    df_location = df[["Neighborhood"]]
    df_location["lat"] = df_location["Neighborhood"].apply(lambda x: df_gps[df_gps["Location"] == x]["Lat"].tolist()[0])
    df_location["lon"] = df_location["Neighborhood"].apply(lambda x: df_gps[df_gps["Location"] == x]["Lon"].tolist()[0])
    df_location.drop("Neighborhood", axis=1, inplace=True)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=42.026798,
            longitude=-93.620178,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df_location,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_location,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))


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
    st.markdown("For more information on meaning of each categorical field, see "
                "[here](https://raw.githubusercontent.com/li-boxuan/house_price_visualization/main/categorical_info.txt)")

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

# Draw map
st.subheader("Where are those houses located?")
df_gps = load_gps_coordinates()
draw_map(df_gps, df)

# Draw correlation heatmap
st.subheader("How correlated are numerical values?")

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

# Draw categorical barplots
st.subheader("What is the estimated sale price for each category?")
df_categorical = df.select_dtypes(exclude=np.number)
df_categorical["SalePrice"] = df["SalePrice"]
draw_bar_plot(df_categorical)

