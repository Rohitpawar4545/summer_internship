import streamlit as st
from instagrapi import Client
import tempfile
import os

# --- Section Title ---
st.markdown("## 📸 Instagram Photo Uploader")

# --- Input Instagram Credentials ---
with st.expander("🔐 Enter Instagram Login Details"):
    username = st.text_input("Username", key="rohitpawar_45rp")
    password = st.text_input("Password", type="password", key="redhat45")

# --- Upload Image and Caption ---
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
caption = st.text_area("📝 Caption", value="🚀 Just uploaded via Python! #Python #DevOps #Automation")

# --- Upload Button ---
if st.button("🚀 Upload to Instagram"):
    if not username or not password:
        st.error("⚠️ Please enter both username and password.")
    elif not uploaded_file:
        st.error("⚠️ Please upload an image first.")
    else:
        try:
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Initialize Instagram client and login
            cl = Client()
            cl.login(username, password)

            # Upload the image
            cl.photo_upload(tmp_path, caption)

            st.success("✅ Photo uploaded successfully!")
            os.remove(tmp_path)

        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
