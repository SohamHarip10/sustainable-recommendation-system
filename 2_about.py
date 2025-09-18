import streamlit as st

st.set_page_config(page_title="About", layout="centered")

# TITLE
st.markdown('<h1 style="text-align:center; color:#2E7D32;">About This Project</h1>', unsafe_allow_html=True)
st.write("---")

# PROJECT DESCRIPTION
st.markdown("""
### Project Overview
This project helps users make **sustainable purchasing decisions** by recommending eco-friendly alternatives for everyday products.

The system uses:
- Dataset of products with eco-scores, prices, and categories  
- Machine Learning Model to suggest sustainable choices  
- Interactive dashboard to visualize sustainability data
""")

st.write("---")

# SDG GOAL
st.markdown("### UN SDG Goal Addressed: Responsible Consumption and Production (Goal 12)")
st.markdown("""
This project promotes:
- Responsible consumption
- Reduction of waste and pollution
- Awareness about eco-friendly products
""")

# TEAM MEMBERS
st.markdown("### Team Members")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("Chaitanya Powar |\nRole: ML Model Development")
with col2:
    st.markdown("Soham Harip |\nRole: Streamlit Frontend & Integration")
with col3:
    st.markdown("Amit Hajare |\nRole: Data Cleaning & Preprocessing")

st.write("---")
st.markdown("<p style='text-align:center;'>💚 Developed with passion for sustainability 💚</p>", unsafe_allow_html=True)
