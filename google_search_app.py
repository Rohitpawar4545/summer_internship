# Filename: google_search_app.py

import streamlit as st
from googleapiclient.discovery import build

# API config
API_KEY = "AIzaSyAVQN8uHysUzQZJGr2RCA64y2Eo0W5NLIA"
CSE_ID = "4771baf51856b4f89"

# Search function
def google_search(query, api_key, cse_id):
    service = build("customsearch", "v1", developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id, num=5).execute()
    return result.get("items", [])

# Streamlit UI
st.set_page_config(page_title="Google Search App", page_icon="🔍", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🔧 App Info")
    st.markdown("""
    **Google Search App**
    - Powered by Google CSE API
    - Built with Python & Streamlit
    - Developed by Rohit Pawar 💻
    """)
    st.markdown("---")
    st.info("Enter any search term in the main page to see results!")

# Main title
st.markdown("<h1 style='text-align: center;'>🔍 Google Search with Python</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Search the web using Google Custom Search API</p>", unsafe_allow_html=True)
st.markdown("---")

# Search input
search_query = st.text_input("📥 Enter your search query", placeholder="e.g., What is Python?", help="Type anything you want to search")

# Search results
if search_query:
    with st.spinner("🔎 Searching Google..."):
        try:
            results = google_search(search_query, API_KEY, CSE_ID)
            if not results:
                st.warning("No results found.")
            else:
                for item in results:
                    st.markdown(
                        f"""
                        <div style='
                            background-color: #f9f9f9;
                            padding: 20px;
                            border-radius: 12px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                            margin-bottom: 15px;
                        '>
                            <h4 style='margin-bottom: 5px;'>{item.get("title")}</h4>
                            <p style='margin-bottom: 10px; color: #555;'>{item.get("snippet")}</p>
                            <a href='{item.get("link")}' target='_blank'>🌐 Visit Site</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        except Exception as e:
            st.error(f"Error: {e}")
