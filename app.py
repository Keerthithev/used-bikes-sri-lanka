import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Sri Lanka Used Bikes Dashboard",
    layout="wide",
    page_icon="🛵",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI + Mobile Text Visibility Fix
st.markdown("""
    <style>
    body, .stApp, .css-1v0mbdj, .stMarkdown, .css-1d391kg, .stButton>button, .css-1d391kg * {
        color: #1e2a44 !important;
        background-color: #f5f6fa !important;
    }
    .sidebar .sidebar-content {
        background-color: #1e2a44 !important;
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #4a69bd !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stMetric {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    h1, h2, h3 {
        color: #1e2a44 !important;
    }
    .css-1d391kg {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_bike_data.csv")
    return df

df = load_data()

# Sidebar Filters
with st.sidebar:
    st.title("🔍 Filter Options")
    brands = sorted(df['Brand'].dropna().unique())
    selected_brand = st.multiselect("Select Brand", brands, default=brands, key="brand_filter")
    
    bike_types = sorted(df['Bike Type'].dropna().unique())
    selected_type = st.multiselect("Select Bike Type", bike_types, default=bike_types, key="type_filter")
    
    min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.slider("Select Year Range", min_year, max_year, (2010, max_year), key="year_filter")
    
    min_price, max_price = int(df['Price'].min()), int(df['Price'].max())
    price_range = st.slider("Price Range (LKR)", min_price, max_price, (50000, 2000000), step=10000, key="price_filter")

# Apply Filters
filtered_df = df[
    (df['Brand'].isin(selected_brand)) &
    (df['Bike Type'].isin(selected_type)) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
    (df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])
]

# Header
st.title("🛵 Sri Lanka Used Bike Market Analysis")
st.markdown("""
    Explore the Sri Lankan used bike market with interactive filters and visualizations. Data sourced from **ikman.lk** (up to 2023).
    Built by **Keerthigan Thevarasa**.
""")

# KPI Metrics
st.markdown("### 📌 Key Market Stats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Listings", f"{len(filtered_df):,}")
with col2:
    st.metric("Average Price (LKR)", f"{filtered_df['Price'].mean():,.0f}")
with col3:
    st.metric("Average Year", f"{filtered_df['Year'].mean():.1f}")

st.markdown("---")

# Visualizations
st.markdown("## 📈 Market Insights")
tab1, tab2 = st.tabs(["Overview", "Detailed Analysis"])

with tab1:
    col4, col5 = st.columns(2)
    with col4:
        fig1 = px.histogram(
            filtered_df, x='Brand', color='Brand',
            title="📦 Listings by Brand", template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig1.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col5:
        fig2 = px.histogram(
            filtered_df, x='Year', nbins=15,
            title="📅 Distribution by Year", template="plotly_white",
            color_discrete_sequence=['#4a69bd']
        )
        fig2.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col6, col7 = st.columns(2)
    with col6:
        fig3 = px.box(
            filtered_df, x='Brand', y='Price', color='Brand',
            title="💰 Price Distribution by Brand", template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig3.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig3, use_container_width=True)
    
    with col7:
        fig4 = px.scatter(
            filtered_df, x='Year', y='Price', color='Brand', size='Price',
            title="🕓 Price vs Year", template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig4.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig4, use_container_width=True)
    
    fig5 = px.pie(
        filtered_df, names='Bike Type',
        title="🚲 Bike Type Distribution", template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig5.update_traces(textinfo='percent+label')
    fig5.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig5, use_container_width=True)

# Data Preview
st.markdown("## 📄 Top Listings")
st.dataframe(
    filtered_df.head(100).style.format({"Price": "₨{:,.0f}", "Year": "{:.0f}"}),
    use_container_width=True
)

# Footer
st.markdown("---")
st.markdown(
    "🔧 Developed by **Keerthigan Thevarasa** | Data from [ikman.lk](https://ikman.lk) via [Kaggle](https://www.kaggle.com) | "
    "Powered by Streamlit and Plotly",
    unsafe_allow_html=True
)
