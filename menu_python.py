import streamlit as st
from twilio.rest import Client
import urllib.parse
import tweepy
import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit
import requests

# ---- CONFIG ----
st.set_page_config(page_title="Unified Social Media Toolkit", page_icon="🌐", layout="centered")
st.title("🌐 Unified Social Media Toolkit")

# ---- CREDENTIALS ----
TWILIO_SID = "ACxxxxxxxxxxxxxxxx"
TWILIO_TOKEN = "xxxxxxxxxxxxxxxx"
TWILIO_PHONE = "+1234567890"

TWITTER_API_KEY = "xxxxxxxx"
TWITTER_API_SECRET = "xxxxxxxx"
TWITTER_ACCESS_TOKEN = "xxxxxxxx"
TWITTER_ACCESS_SECRET = "xxxxxxxx"

EMAIL_FROM = "youremail@gmail.com"
EMAIL_PASS = "yourapppassword"

# ---- MENU ----
menu = st.sidebar.selectbox("📂 Select Tool", [
    "📩 SMS Sender",
    "📞 Voice Call",
    "📸 Instagram Message",
    "🐦 Twitter Poster",
    "📧 Email Sender",
    "💬 WhatsApp Sender",
    "🔗 LinkedIn Auto Poster"
])

# ---- SMS Sender ----
if menu == "📩 SMS Sender":
    st.header("📩 Send SMS using Twilio")
    phone = st.text_input("Recipient Phone Number", "+91")
    message = st.text_area("Message")

    if st.button("Send SMS"):
        try:
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            msg = client.messages.create(body=message, from_=TWILIO_PHONE, to=phone)
            st.success(f"✅ SMS sent! SID: {msg.sid}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---- Voice Call ----
elif menu == "📞 Voice Call":
    st.header("📞 Make Voice Call using Twilio")
    call_to = st.text_input("Phone Number", "+91")
    voice_msg = st.text_area("Voice Message", "Hello! This is a test call.")

    if st.button("Make Call"):
        try:
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            encoded_msg = urllib.parse.quote(f"<Response><Say>{voice_msg}</Say></Response>")
            url = f"http://twimlets.com/echo?Twiml={encoded_msg}"
            call = client.calls.create(to=call_to, from_=TWILIO_PHONE, url=url)
            st.success(f"✅ Call started! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---- Instagram Message (Simulated) ----
elif menu == "📸 Instagram Message":
    st.header("📸 Simulated Instagram Message")
    st.warning("Instagram API is restricted. This is a simulation.")
    user = st.text_input("Instagram Username")
    msg = st.text_area("Message")

    if st.button("Simulate Send"):
        if user and msg:
            st.success(f"✅ Simulated sending message to @{user}")
        else:
            st.warning("Please fill in all fields.")

# ---- Twitter Poster ----
elif menu == "🐦 Twitter Poster":
    st.header("🐦 Post Tweet")
    tweet = st.text_area("Enter your tweet", max_chars=280)

    if st.button("Post Tweet"):
        try:
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
            api = tweepy.API(auth)
            api.verify_credentials()
            api.update_status(tweet)
            st.success("✅ Tweet posted!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---- Email Sender ----
elif menu == "📧 Email Sender":
    st.header("📧 Send Email via Gmail SMTP")
    to = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message Body")

    if st.button("Send Email"):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL_FROM
            msg['To'] = to

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_FROM, EMAIL_PASS)
                server.sendmail(EMAIL_FROM, to, msg.as_string())

            st.success("✅ Email sent successfully.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---- WhatsApp Sender ----
elif menu == "💬 WhatsApp Sender":
    st.header("💬 Send WhatsApp Message using PyWhatKit")
    phone = st.text_input("Phone Number", "+91")
    message = st.text_area("Message")

    if st.button("Send WhatsApp Now"):
        try:
            kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10, tab_close=True)
            st.success("✅ WhatsApp message sent.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---- LinkedIn Poster ----
elif menu == "🔗 LinkedIn Auto Poster":
    st.header("🔗 Auto Post on LinkedIn")

    access_token = st.text_input("Access Token", type="password")
    linkedin_urn = st.text_input("LinkedIn URN (e.g., urn:li:person:xxxx)")
    linkedin_msg = st.text_area("Post Content", "Excited to share my new project!")

    if st.button("Post to LinkedIn"):
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json"
            }

            post_data = {
                "author": linkedin_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": linkedin_msg
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            res = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=post_data)
            if res.status_code == 201:
                st.success("✅ Posted successfully to LinkedIn!")
            else:
                st.error(f"❌ Failed. Status Code: {res.status_code}")
                st.code(res.text)
        except Exception as e:
            st.error(f"❌ Error: {e}")
