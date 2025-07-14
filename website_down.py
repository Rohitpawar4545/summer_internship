# 📁 Save this file as: website_downloader.py

import streamlit as st
import requests
from urllib.parse import urlparse
import os

# Set Streamlit page config
st.set_page_config(page_title="Website Data Downloader", page_icon="🌐", layout="centered")

st.title("🌐 Website Data Downloader using Python")
st.markdown("Enter any website URL to download its HTML source code as a `.html` file.")

# Input: Website URL
url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")

if st.button("📥 Download Website Data"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        try:
            response = requests.get(url)
            response.raise_for_status()

            parsed_url = urlparse(url)
            filename = f"{parsed_url.netloc.replace('.', '_')}.html"

            # Save HTML content to file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)

            # Provide download button
            with open(filename, "rb") as f:
                st.success("✅ Website data downloaded successfully!")
                st.download_button(
                    label="📄 Download HTML File",
                    data=f,
                    file_name=filename,
                    mime="text/html"
                )

            os.remove(filename)  # Clean up after download
        except Exception as e:
            st.error(f"❌ Failed to download website: {e}")
