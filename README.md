 🌱 Sustainable Recommendation System  

A **Streamlit + FastAPI powered web application** that recommends sustainable products based on semantic search and displays rich visualizations to promote eco-friendly choices.  

---

## 📌 Features  

✅ **Semantic Search** – Search for products using natural language queries.  
✅ **Eco-Score Based Recommendations** – Suggests products with higher sustainability scores.  
✅ **Interactive Visualizations** –  
- Eco-Score Distribution  
- Average Eco-Score by Category  
- Price vs Eco-Score Scatter  
- Category-wise Product Share (Pie Chart)  
✅ **Modern UI** – Simple, clean, and responsive interface.  

---

## 🛠 Tech Stack  

- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Model:** SentenceTransformer (semantic search)  
- **Database:** CSV / Pandas  
- **Visualization:** Plotly  

---
## 📂 Project Structure 

sustainable-recommendation-system/
│
├── backend/
│ ├── main.py # FastAPI backend
│ └── sustain_reco_model/ 
│
├── pages/
│ ├── 1_visualizations.py # Visualization page
│ └── other_pages.py # Additional pages
│
├── app.py # Streamlit entry point
├── requirements.txt # Dependencies
└── README.md 

## 🚀 Installation & Setup  

1. Clone the repository
```bash
git clone https://github.com/SohamHarip10/sustainable-recommendation-system.git
cd sustainable-recommendation-system

2. Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate # On Linux

3. Install Dependencies
pip install -r requirements.txt

4. Download Model File
backend/sustain_reco_model/

5. Run Backend (FastAPI)
uvicorn backend.main:app --reload

6. Run Frontend (Streamlit)
streamlit run app.py
