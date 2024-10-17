
import pandas as pd
import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide'
)

# Optimized data caching and error handling
@st.cache_data
def get_data():
    try:
        df = pd.read_csv('supermarket_sales.csv')
    except FileNotFoundError:
        st.error("File not found. Please upload the correct file.")
        return pd.DataFrame()  # Return an empty DataFrame to avoid errors
    return df

df = get_data()

# Sidebar for filters with collapsibility
with st.sidebar.expander("Filter Options", expanded=True):
    city = st.multiselect(
        "Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique()
    )
    customer_type = st.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique()
    )
    gender = st.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

# Filter dataframe based on sidebar inputs
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# Title and KPIs
st.title(":bar_chart: Sales Dashboard")
st.markdown('##')

# Top KPIs
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

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

st.markdown("---")

# Optimized bar chart creation function
def create_bar_chart(data, x, y, title):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=['#0083B8'] * len(data),
        template="plotly_white"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )
    return fig

# Sales by product line [Bar Chart]
sales_by_product_line = (
    df_selection.groupby(by=['Product_line']).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = create_bar_chart(
    sales_by_product_line, x="Total", y=sales_by_product_line.index, title="<b>Sales by Product Line</b>"
)

# Extract hour from Time
df_selection["hour"] = pd.to_datetime(df_selection["Time"], format="%H:%M").dt.hour

# Sales by hour [Bar Chart]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = create_bar_chart(
    sales_by_hour, x=sales_by_hour.index, y="Total", title="<b>Sales by Hour</b>"
)

# Display charts
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)