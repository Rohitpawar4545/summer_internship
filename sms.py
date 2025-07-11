import streamlit as st
from twilio.rest import Client
import urllib.parse

--- Twilio Credentials (use st.secrets or env vars in production) ---
ACCOUNT_SID = "34eb0c6c132671d3"
AUTH_TOKEN = "27b1b4dec5de7"
TWILIO_PHONE = "+1543"  # Your Twilio number

 --- Streamlit Page Settings ---
st.set_page_config(page_title="Twilio Toolkit", page_icon="📞", layout="centered")
st.title("Messaging & Calling")

--- Tabs for SMS and Voice ---
tab1, tab2 = st.tabs(["📩 Send SMS", "📞 Make a Call"])


with tab1:
    st.header("📩 Send SMS")
    st.markdown("Send SMS messages using Twilio and Python.")

    to_sms = st.text_input("Recipient Phone Number (with country code)", "+91", key="sms_number")
    sms_message = st.text_area("Your Message", "Hello from Python via Twilio! 🐍")

    if st.button("Send SMS"):
        if not to_sms.strip() or not sms_message.strip():
            st.warning("Please enter both phone number and message.")
        else:
            try:
                client = Client(ACCOUNT_SID, AUTH_TOKEN)
                message = client.messages.create(
                    body=sms_message,
                    from_=TWILIO_PHONE,
                    to=to_sms
                )
                st.success(f"✅ SMS sent successfully! Message SID: {message.sid}")
            except Exception as e:
                st.error(f"❌ Failed to send SMS: {e}")


with tab2:
    st.header("📞 Make a Voice Call")
    st.markdown("Send a real voice call using Twilio and Python.")

    to_call = st.text_input("Recipient Phone Number (with country code)", "+91", key="call_number")
    call_message = st.text_area("Voice Message", "Hello! This is a test call using Python.")

    if st.button("📞 Call Now"):
        if not to_call.strip() or not call_message.strip():
            st.warning("Please enter both phone number and voice message.")
        else:
            try:
                client = Client(ACCOUNT_SID, AUTH_TOKEN)

                encoded_message = urllib.parse.quote(f"<Response><Say voice='alice'>{call_message}</Say></Response>")
                url = f"http://twimlets.com/echo?Twiml={encoded_message}"

                call = client.calls.create(
                    to=to_call,
                    from_=TWILIO_PHONE,
                    url=url
                )
                st.success(f"✅ Call initiated! Call SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Failed to initiate call: {e}")
