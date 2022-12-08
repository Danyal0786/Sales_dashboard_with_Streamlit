import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as stc 
import numpy as np


st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)


html_temp = """
		<div style="background-color:#009688;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Sales Dashboard </h1>
		<h4 style="color:white;text-align:center;">Estimating total sales by each category</h4>
		</div>
		"""

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarket_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

stc.html(html_temp) 
st.dataframe(df)


# ----------Sidebar------------

st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df['Gender'].unique()
)

payment = st.sidebar.multiselect(
    "Select the Product Line:",
    options=df["Payment"].unique(),
    default=df['Payment'].unique()
)


product_line = st.sidebar.multiselect(
    "Select the Product Line:",
    options=df["Product_line"].unique(),
    default=df['Product_line'].unique()
)


df_selection = df.query(
    "City== @city & Customer_type == @customer_type & Gender == @gender & Product_line== @product_line & Payment == @payment"
)

st.dataframe(df_selection)


# ---------Main Page----------

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)



left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product_line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)



# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_hourly_sales, use_container_width=True)



# ---------Area Chart---------

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Product line', 'Customer type', 'Rating'])



#  -------Pyplot histogram-----------

import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Product line', 'Customer type', 'Rating'])


left_column,right_column = st.columns(2)
left_column.area_chart(chart_data,  use_container_width=True)
right_column.line_chart(chart_data,use_container_width=True)





