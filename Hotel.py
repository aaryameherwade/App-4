import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title="Hotel Finder Dashboard",
    page_icon="🏨",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.title{
    font-size:42px;
    font-weight:bold;
    color:#00D4FF;
    text-align:center;
}

.subtitle{
    color:white;
    text-align:center;
    font-size:18px;
}

.hotel-card{
    background:#1E1E1E;
    padding:15px;
    border-radius:12px;
    border:1px solid #333;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="title">🏨 Hotel Finder Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Search Hotels & Get Smart Recommendations</p>',
    unsafe_allow_html=True
)

# ----------------------------
# Load Data
# ----------------------------

df = pd.read_csv("hotels.csv")

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("🔍 Search Hotel")

cities = sorted(df["City"].unique())

city = st.sidebar.selectbox(
    "Select City",
    cities
)

price = st.sidebar.slider(
    "Maximum Price (₹)",
    1000,
    10000,
    5000
)

rating = st.sidebar.slider(
    "Minimum Rating",
    1.0,
    5.0,
    4.0
)

# ----------------------------
# Filter
# ----------------------------

result = df[
    (df["City"] == city)
    &
    (df["Price"] <= price)
    &
    (df["Rating"] >= rating)
]

# ----------------------------
# Metrics
# ----------------------------

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Hotels Found",
    len(result)
)

if len(result):

    c2.metric(
        "Average Price",
        f"₹{int(result['Price'].mean())}"
    )

    c3.metric(
        "Average Rating",
        round(result["Rating"].mean(), 2)
    )

    c4.metric(
        "Top Hotel",
        result.iloc[0]["Hotel"]
    )

# ----------------------------
# Hotel Cards
# ----------------------------

st.subheader("🏨 Available Hotels")

if len(result) == 0:

    st.warning("No Hotels Found.")

else:

    for i, row in result.iterrows():

        with st.container():

            left, right = st.columns([3,1])

            with left:

                st.markdown(f"""
                ### {row['Hotel']}

                📍 **City:** {row['City']}

                ⭐ **Rating:** {row['Rating']}

                💰 **Price:** ₹{row['Price']}

                🛏 Rooms Available: {row['Rooms']}

                🍽 Breakfast Included: {row['Breakfast']}

                🚗 Parking: {row['Parking']}

                📶 Free WiFi: {row['Wifi']}

                """)

            with right:

                st.button(
                    "Book Now",
                    key=i
                )

        st.divider()

# ----------------------------
# Price Chart
# ----------------------------

if len(result):

    st.subheader("💰 Hotel Price Comparison")

    fig = px.bar(
        result,
        x="Hotel",
        y="Price",
        color="Rating",
        text="Price",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# Rating Chart
# ----------------------------

if len(result):

    st.subheader("⭐ Rating Distribution")

    fig2 = px.scatter(
        result,
        x="Price",
        y="Rating",
        color="Hotel",
        size="Rooms",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ----------------------------
# Recommendation
# ----------------------------

if len(result):

    best = result.sort_values(
        ["Rating","Price"],
        ascending=[False,True]
    ).iloc[0]

    st.success(
        f"""
🏆 Recommended Hotel

{best['Hotel']}

⭐ Rating : {best['Rating']}

💰 Price : ₹{best['Price']}

Reason:
Highest rated hotel within your selected budget.
"""
    )

# ----------------------------
# Data Table
# ----------------------------

st.subheader("📋 Hotel Data")

st.dataframe(
    result,
    use_container_width=True
)
