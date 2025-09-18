import streamlit as st
import pandas as pd
import plotly.express as px

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="📊 Sustainability Analytics", layout="wide")

# --------- LOAD DATA ---------
df = pd.read_csv(r"C:\Users\Soham Harip\OneDrive\Desktop\sustainable-reco\backend\catalog_indexed.csv")

# Clean data
df = df.dropna(subset=["price", "rating", "category"])
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df = df.dropna(subset=["price", "rating"])

# --------- TITLE ---------
st.markdown('<h1 style="text-align:center; color:#2E7D32;">📊 Sustainability Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2em; color:#388E3C;">Explore price trends, ratings, and category insights</p>', unsafe_allow_html=True)
st.write("---")

# --------- VISUALIZATIONS ---------

# 1️⃣ Category Distribution Pie Chart
st.subheader("🛍️ Product Category Distribution")
category_counts = df["category"].value_counts().reset_index()
category_counts.columns = ["category", "count"]

fig_pie = px.pie(
    category_counts,
    values="count",
    names="category",
    title="Distribution of Products by Category",
    hole=0.3,  # Makes it a donut chart (looks cleaner)
)

fig_pie.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(fig_pie, use_container_width=True)


# 2️⃣ Average Price by Category
st.subheader("📂 Average Price by Category")
avg_price = df.groupby("category", as_index=False)["price"].mean()
fig2 = px.bar(avg_price, x="category", y="price", title="Average Price per Category")
fig2.update_traces(marker_color="#81c784")
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Rating Distribution
st.subheader("⭐ Rating Distribution")
fig3 = px.histogram(df, x="rating", nbins=10, title="Distribution of Product Ratings")
fig3.update_traces(marker_color="#ff9800")
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Price vs Rating Scatter Plot
st.subheader("📈 Price vs Rating")
fig4 = px.scatter(df, x="price", y="rating", color="category",
                  hover_data=["name", "brand"],
                  title="Price vs Rating by Category",
                  size="rating")
st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Top Rated Products (Optional, shows only top 10)
st.subheader("🏆 Top 10 Highest Rated Products")
top_rated = df.sort_values(by="rating", ascending=False).head(10)
fig5 = px.bar(top_rated, x="name", y="rating", color="category",
              title="Top 10 Rated Products")
fig5.update_xaxes(tickangle=45)
st.plotly_chart(fig5, use_container_width=True)

st.write("---")
st.markdown("<p style='text-align:center;'>📈 Data Visualizations to Promote Awareness</p>", unsafe_allow_html=True)
