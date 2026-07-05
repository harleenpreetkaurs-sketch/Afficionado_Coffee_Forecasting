import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Afficionado Coffee Roasters Dashboard",
    page_icon="☕",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("data/Afficionado Coffee Roasters.xlsx")

    # Feature Engineering
    df["Revenue"] = df["transaction_qty"] * df["unit_price"]
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S")
    df["Hour"] = df["transaction_time"].dt.hour

    return df

df = load_data()

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a Page",
    [
        "Home",
        "Dashboard",
        "Store Analysis",
        "Forecasting",
        "About"
    ]
)

# ---------------- HOME ----------------
if page == "Home":

    st.title("☕ Afficionado Coffee Roasters")
    st.subheader("Data-Driven Forecasting & Peak Demand Prediction")

    st.markdown("""
This dashboard analyzes coffee shop sales using historical transaction data.

### Objectives

- Forecast future demand
- Identify peak sales hours
- Compare store performance
- Improve staffing decisions
- Reduce inventory waste
""")

# ---------------- DASHBOARD ----------------
elif page == "Dashboard":

    st.title("Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Revenue", f"${df['Revenue'].sum():,.2f}")
    c2.metric("Transactions", f"{len(df):,}")
    c3.metric("Quantity Sold", f"{df['transaction_qty'].sum():,}")
    c4.metric("Stores", df["store_location"].nunique())

    st.markdown("---")

    revenue_store = df.groupby("store_location")["Revenue"].sum().reset_index()

    fig = px.bar(
        revenue_store,
        x="store_location",
        y="Revenue",
        color="Revenue",
        title="Revenue by Store"
    )

    st.plotly_chart(fig, use_container_width=True)

    category = df.groupby("product_category")["Revenue"].sum().reset_index()

    fig2 = px.pie(
        category,
        names="product_category",
        values="Revenue",
        title="Revenue by Category"
    )

    st.plotly_chart(fig2, use_container_width=True)

    hourly = df.groupby("Hour")["Revenue"].sum().reset_index()

    fig3 = px.line(
        hourly,
        x="Hour",
        y="Revenue",
        markers=True,
        title="Peak Sales Hours"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------- STORE ----------------
elif page == "Store Analysis":

    st.title("Store Analysis")

    store = st.selectbox(
        "Select Store",
        df["store_location"].unique()
    )

    filtered = df[df["store_location"] == store]

    st.metric(
        "Revenue",
        f"${filtered['Revenue'].sum():,.2f}"
    )

    top_products = (
        filtered.groupby("product_detail")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Revenue",
        y="product_detail",
        orientation="h",
        title="Top 10 Products"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- FORECAST ----------------
elif page == "Forecasting":

    st.title("Forecasting")

    st.info(
        "The Prophet forecasting model was trained separately in the project notebook. "
        "This dashboard focuses on visual analytics and reporting."
    )

    st.success("Forecasting module completed successfully.")

# ---------------- ABOUT ----------------
else:

    st.title("About")

    st.markdown("""
### Project

Data-Driven Forecasting & Peak Demand Prediction for Afficionado Coffee Roasters

### Tools Used

- Python
- Streamlit
- Pandas
- Plotly
- Prophet

### Business Benefits

- Better inventory planning
- Improved staffing
- Peak demand prediction
- Revenue monitoring
- Data-driven decision making
""")

