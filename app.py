import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="🌱 Sustainable Product Recommendation", layout="wide")

# --------- LOAD DATA ---------
df = pd.read_csv(
    r"C:\Users\Soham Harip\OneDrive\Desktop\sustainable-reco\backend\catalog_indexed.csv"
)

# Normalize columns
df["id"] = df["id"].astype(str)
df["category"] = df["category"].astype(str)
df["name"] = df["name"].astype(str)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# --------- MODEL + FAISS INDEX LOADING ---------
@st.cache_resource
def load_model():
    """Load the embedding model (cached for performance)."""
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def build_faiss_index(_model, df):
    """Create FAISS index from catalog data. (model ignored for hashing)"""
    combined_text = (
        df["name"].fillna("")
        + " " + df["description"].fillna("")
        + " " + df["brand"].fillna("")
        + " " + df["category"].fillna("")
    )
    embeddings = _model.encode(combined_text.tolist(), normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings

# Load model & index
model = load_model()
index, embeddings = build_faiss_index(model, df)


# --------- SEARCH FUNCTION ---------
def search_products(query, top_k=50):
    """Return top_k most similar products for the query."""
    if not query.strip():
        return df
    query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")
    D, I = index.search(query_embedding, top_k)
    return df.iloc[I[0]]

# --------- CUSTOM CSS ---------
st.markdown(
    """
    <style>
    /* Title Banner */
    .title-box {
        text-align: center;
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #4caf50;
        font-size: 40px;
        font-weight: bold;
        color: #2e7d32;
        margin-bottom: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        font-size: 1.3em;
        color: #388E3C;
        margin-bottom: 20px;
    }
    /* Navigation Buttons */
    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 10px 0 20px 0;
    }
    .nav-btn {
        background-color: #f1f8e9;
        border: 2px solid #4caf50;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        color: #2e7d32;
        text-decoration: none;
        transition: all 0.2s ease-in-out;
    }
    .nav-btn:hover {
        background-color: #c8e6c9;
        cursor: pointer;
    }
    /* Product Cards */
    .card {
        background: #f4f9f4;
        border: 2px solid #d4edda;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        display: flex;
    }
    .card img {
        width: 120px;
        height: 120px;
        object-fit: contain;
        margin-right: 15px;
    }
    .rating {
        font-weight: bold;
        color: #ff9800;
    }
    .buy-btn {
        background: #4caf50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------- QUERY PARAMS ---------
query_params = st.query_params
product_id = query_params.get("product_id")
if isinstance(product_id, list):
    product_id = product_id[0]

# --------- SIDEBAR ---------
st.sidebar.header("🔍 Filters")
category = st.sidebar.selectbox(
    "Select Category",
    ["All", "Clothing", "Electronics", "Groceries", "Personal Care", "Drinkware"],
)
price_min, price_max = st.sidebar.slider("Price Range ($)", 0, 500, (0, 500))

sort_option = st.sidebar.radio(
    "Sort By",
    ["None", "Rating: High → Low", "Price: High → Low", "Price: Low → High"],
    index=0,
)


# --------- PRODUCT PAGE ---------
if product_id:
    product_rows = df[df["id"] == str(product_id)]
    if not product_rows.empty:
        product = product_rows.iloc[0].to_dict()

        st.markdown(f'<div class="title-box">{product.get("name","")}</div>', unsafe_allow_html=True)
        if pd.notna(product.get("img_url")):
            st.image(product["img_url"], width=200)

        st.markdown(f"**Category:** {product.get('category','')}")
        st.markdown(f"**Material:** {product.get('material','')}")
        st.markdown(f"**Brand:** {product.get('brand','')}")
        st.markdown(f"**Price:** ${product.get('price','')}")
        st.markdown(f"**Rating:** {product.get('rating','')} ⭐ ({product.get('reviewsCount','')} reviews)")
        st.markdown(f"**In Stock:** {product.get('inStockText','')}")
        st.markdown(f"**Description:** {product.get('description','')}")
        if pd.notna(product.get("url")):
            st.markdown(
                f"<a class='buy-btn' href='{product['url']}' target='_blank'>Buy Now</a>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button("⬅ Back to Products"):
            query_params.clear()
            st.rerun()
    else:
        st.warning("⚠️ Product not found. Please go back and select another product.")
        if st.button("⬅ Back to Products"):
            query_params.clear()
            st.rerun()

# --------- MAIN PAGE ---------
else:
    st.markdown('<div class="title-box">🌱 Sustainable Product Recommendation</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Find eco-friendly alternatives for your shopping needs</p>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Search Products",
        placeholder="🔍 Search products...",
        key="search",
        max_chars=50,
        label_visibility="collapsed",
    )

    filtered_df = search_products(search_query)

    # Apply filters
    if category != "All":
        filtered_df = filtered_df[filtered_df["category"].str.contains(category, case=False, na=False)]
    filtered_df = filtered_df[
        (filtered_df["price"] >= float(price_min)) & (filtered_df["price"] <= float(price_max))
    ]

    # Apply sorting
    if sort_option == "Rating: High → Low":
        filtered_df = filtered_df.sort_values(by="rating", ascending=False, na_position="last")
    elif sort_option == "Price: High → Low":
        filtered_df = filtered_df.sort_values(by="price", ascending=False, na_position="last")
    elif sort_option == "Price: Low → High":
        filtered_df = filtered_df.sort_values(by="price", ascending=True, na_position="last")

    # Pagination
    items_per_page = 20
    total_items = len(filtered_df)
    total_pages = max(1, (total_items - 1) // items_per_page + 1)
    current_page = st.sidebar.number_input("Select Page", min_value=1, max_value=total_pages, value=1, step=1)
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]

    st.subheader(f"Recommended Products (Page {current_page} of {total_pages})")

    if filtered_df.empty:
        st.warning("⚠️ No products found for your search/filters.")
    else:
        for _, row in page_df.iterrows():
            pid = row["id"]
            st.markdown(
                f"""
            <div class="card">
                <img src="{row.get('img_url','')}" alt="{row.get('name','')}">
                <div>
                    <b>🛒 Product:</b> <a href='?product_id={pid}'>{row.get('name','')}</a><br>
                    <b>📂 Category:</b> {row.get('category','')}<br>
                    <b>💰 Price:</b> ${row.get('price','')}<br>
                    <b>⭐ Rating:</b> <span class="rating">{row.get('rating','')}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.write("---")
    st.markdown(
        "<p style='text-align:center;'>Developed by <b>Team Green</b> 🌱 | <a href='#'>GitHub Repo</a></p>",
        unsafe_allow_html=True,
    )
