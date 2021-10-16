# Description

What are the factors that determine a house price in the U.S.? As students,
we probably don't have enough money to buy a property now, but hopefully we
could in the future. Let's get prepared early and have a deep dive into the
U.S. housing market! In this project, we present 1500 entries of housing data
from Armes, Iowa. After going through this interactive website, you should have
a rough idea about the determining factors for housing prices! Specifically,
you should be able to answer the following questions:

1) What are the most important factors that determine the housing price?
2) How do house characteristics (including price) change over the year?
3) For a given property, what value leads to highest price?

# Rationale for Design Decisions

I used different visual encodings and interaction techniques for different
parts.

1. Data Overview

The side panel on the left side shows data overview. It provides a dropdown
menu where the reader can choose the property that they are interested. The
panel will show a description of that property, and also the full data for
that property, in the tabular form. The side panel can be collapsed and it
is mainly used as a reference. Initially, I printed out the whole table, but
I found it was difficult to look up a particular feature. I also tried
different visualizations, but they were too "heavy" for a side panel, and
would distract users. Now the side panel is concise and can provide full
information as reference.

2. House Location

To help readers have an understanding of where are the houses located, I
use `pydeck_chart` which enables displaying data points on an open street map.
The dataset itself only contains neighborhood names, so I scrape the GPS coordinates
data from an external website. With GPS coordinates, the locations of all houses
are clearly shown on a single map. The map is interactive and can be dragged,
zoomed in and out. Initially, I considered simply printing out the neighborhood
names, but I thought a visualization would be much better.

3. Correlations with Housing Price

To help readers find out the correlations of the numerical values, and thus
what the most important factors are, I use a heatmap together with a multi-selector.
I preprocess the data and display the top 10 features that are highly correlated
with the housing price by default. Users can choose other values that are interested in.

4. Changes over Years

All the houses are built in different years, ranging from 1872 to 2010. What a
long time span! An interesting question is, how are the characteristics of houses
changing over the year? Are new houses larger and more expensive? Do Americans
have larger garage areas than before? To enable this exploration, I use selector
and slider for interaction, and box plots for visualization. Users can freely
choose the characteristics and the time span they are interested in. Initially,
I didn't use the slider, but then I found out there might be too much data showing
in a single graph, losing the ability to display details. With the slider, users
can not only have an overview but also spot subtle differences in a short period
of time.

5. Estimated Sale Price

Many characteristics of a house are categorical values. How do these values
determine housing prices? In this section, I use a selector for interaction
and a bar plot for visualization. Readers can select a single categorical
variable they are interested in, and view the average (predicted) price based
on each category. For example, users can easily determine which neighborhoods
are likely better by visualizing bar plot of neighboods category. I tried
different plots including box plot, but I feel they are too complicated and
can distract users from gaining an overall idea. The bar plot is concise and
easy to read.

# Overview of Development Process

This is a solo project. I spent around 15 hours finishing this project.
- 3 hours browsing and selecting the dataset
- 3 hours preparing data, including:
  - Download dataset from Kaggle
  - Scrape description data for each feature
  - Scrape GPS coordinates for each house using [external API](https://www.latlong.net/convert-address-to-lat-long.html)
  - Fix inconsistencies between the primary data and secondary data
- 1 hour reading Streamlit API documentation
- 6 hours developing the application
- 1 hour figuring out deploying the application on Streamlit
- 1 hour writing this documentation