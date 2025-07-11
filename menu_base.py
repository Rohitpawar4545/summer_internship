import streamlit as st
import pandas as pd
import datetime
import re
import os
import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from openai import OpenAI
from twilio.rest import Client

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(page_title="Multi-Tool Dashboard", layout="centered", page_icon="🧰")

st.sidebar.title("🔧 NAVIGATION")
choice = st.sidebar.radio("Select a Tool", [
    "🚑 Fake Emergency Detector",
    "📱 WhatsApp Message Sender",
    "🎓 Student Guider",
    "🐳 Docker Manager",
    "📞 Twilio Voice Caller",
    "✉️ Email Sender"
])

# ------------------ 1. Fake Emergency Detector ------------------ #
if choice == "🚑 Fake Emergency Detector":
    st.title("🚑 Fake Emergency Detector")
    st.write("Use AI to detect whether an emergency message is real or fake.")

    data = {
        "message": [
            "My father is unconscious and not breathing",
            "I just want to test how fast you respond",
            "There's been a car accident outside my home",
            "Send ambulance quickly or I will sue",
            "My child fell down and is bleeding badly",
            "No emergency, just needed a ride",
            "There is a fire and someone is trapped inside",
            "I was bored and wanted to see the ambulance",
        ],
        "label": [1, 0, 1, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)

    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])
    model.fit(df['message'], df['label'])

    user_input = st.text_area("Enter Emergency Description:")
    if st.button("Check"):
        pred = model.predict([user_input])[0]
        prob = model.predict_proba([user_input])[0][pred]
        if pred == 1:
            st.success(f"✅ Real Emergency Detected (Confidence: {prob:.2f})")
        else:
            st.error(f"🚫 Fake Emergency Detected (Confidence: {prob:.2f})")

# ------------------ 2. WhatsApp Message Sender ------------------ #
elif choice == "📱 WhatsApp Message Sender":
    st.title("📱 WhatsApp Message Sender")

    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        - WhatsApp Web must be open
        - Use full number with +91
        - You can send or schedule messages
        """)

    def is_valid_number(phone):
        return re.match(r"^\+\d{10,15}$", phone)

    tab1, tab2 = st.tabs(["📤 Send Now", "⏰ Schedule"])

    with tab1:
        st.subheader("Send Instantly")
        phone = st.text_input("Phone Number", "+91", key="phone_now")
        message = st.text_area("Message", key="msg_now")

        if st.button("Send Now"):
            if not is_valid_number(phone) or not message.strip():
                st.warning("Enter valid number and message.")
            else:
                try:
                    kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
                    st.success("✅ Message sent successfully.")
                except Exception as e:
                    st.error("Failed to send.")
                    st.code(str(e))

    with tab2:
        st.subheader("Schedule Message")
        phone_sched = st.text_input("Phone Number", "+91", key="phone_sched")
        message_sched = st.text_area("Message", key="msg_sched")
        col1, col2 = st.columns(2)
        hour = col1.number_input("Hour", 0, 23, datetime.datetime.now().hour)
        minute = col2.number_input("Minute", 0, 59, (datetime.datetime.now().minute + 2) % 60)

        if st.button("Schedule"):
            if not is_valid_number(phone_sched) or not message_sched.strip():
                st.warning("Enter valid number and message.")
            else:
                try:
                    kit.sendwhatmsg(phone_sched, message_sched, int(hour), int(minute), wait_time=10, tab_close=True)
                    st.success("✅ Message scheduled successfully.")
                except Exception as e:
                    st.error("Failed to schedule.")
                    st.code(str(e))

# ------------------ 3. Student Guider using Gemini ------------------ #
elif choice == "🎓 Student Guider":
    st.title("🎓 Student Guider - Career Advice with Gemini")

    api_key = "YOUR_GEMINI_API_KEY"  # Replace with your Gemini API key
    gemini_model = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    def student_guider(prompt_text):
        try:
            mymsg = [
                {"role": "system", "content": "Act as a student guider"},
                {"role": "user", "content": prompt_text}
            ]
            response = gemini_model.chat.completions.create(model="gemini-2.5-flash", messages=mymsg)
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error: {str(e)}"

    query = st.text_area("Ask your academic/career question:")
    if st.button("Get Advice"):
        if query.strip():
            with st.spinner("Thinking..."):
                response = student_guider(query)
                st.success("✅ Suggested Advice:")
                st.write(response)
        else:
            st.warning("Please enter a question.")

# ------------------ 4. Docker Manager ------------------ #
elif choice == "🐳 Docker Manager":
    st.title("🐳 Docker Control Panel")

    task = st.selectbox("Choose Docker Action", [
        "Launch new container",
        "Stop container",
        "Remove container",
        "Start container",
        "List images",
        "List all containers",
        "Pull image from Docker Hub"
    ])

    if task == "Launch new container":
        name = st.text_input("Container Name")
        image = st.text_input("Docker Image (e.g. ubuntu)")
        if st.button("Launch"):
            output = os.popen(f"docker run -dit --name {name} {image}").read()
            st.success("✅ Container Launched")
            st.code(output)

    elif task == "Stop container":
        name = st.text_input("Container Name to Stop")
        if st.button("Stop"):
            output = os.popen(f"docker stop {name}").read()
            st.success("🛑 Container Stopped")
            st.code(output)

    elif task == "Remove container":
        name = st.text_input("Container Name to Remove")
        if st.button("Remove"):
            output = os.popen(f"docker rm -f {name}").read()
            st.warning("🗑️ Container Removed")
            st.code(output)

    elif task == "Start container":
        name = st.text_input("Container Name to Start")
        if st.button("Start"):
            output = os.popen(f"docker start {name}").read()
            st.success("▶️ Container Started")
            st.code(output)

    elif task == "List images":
        if st.button("List Docker Images"):
            output = os.popen("docker images").read()
            st.code(output)

    elif task == "List all containers":
        if st.button("List All Containers"):
            output = os.popen("docker ps -a").read()
            st.code(output)

    elif task == "Pull image from Docker Hub":
        image = st.text_input("Image Name (e.g. ubuntu)")
        if st.button("Pull Image"):
            output = os.popen(f"docker pull {image}").read()
            st.success("📥 Image Pulled")
            st.code(output)

# ------------------ 5. Twilio Voice Caller ------------------ #
elif choice == "📞 Twilio Voice Caller":
    st.title("📞 Twilio Voice Caller")
    st.markdown("Send a real voice call using Twilio + Python.")

    ACCOUNT_SID = "YOUR_TWILIO_SID"
    AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
    TWILIO_PHONE = "+19803512110"

    to_number = st.text_input("Recipient Phone Number", "+91XXXXXXXXXX")
    voice_message = st.text_area("Message to Speak", "Hello! This is a test call using Python.")

    if st.button("📞 Call Now"):
        if not to_number.strip() or not voice_message.strip():
            st.warning("Please enter both phone number and message.")
        else:
            try:
                fallback_twiml_url = "http://demo.twilio.com/docs/voice.xml"  # You can replace with your hosted XML
                client = Client(ACCOUNT_SID, AUTH_TOKEN)
                call = client.calls.create(to=to_number, from_=TWILIO_PHONE, url=fallback_twiml_url)
                st.success(f"✅ Call initiated! Call SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Failed to initiate call: {e}")

# ------------------ 6. Email Sender ------------------ #
elif choice == "✉️ Email Sender":
    st.title("✉️ Email Sender")
    st.markdown("Send emails using your Gmail account via SMTP.")

    sender_email = st.text_input("Your Gmail Address", "your_email@gmail.com")
    password = st.text_input("App Password (not Gmail password)", type="password")
    recipient_email = st.text_input("Recipient Email", "")
    subject = st.text_input("Subject", "Test Email")
    body = st.text_area("Email Body", "This is the body of the email.")

    if st.button("Send Email"):
        if not recipient_email or '@' not in recipient_email:
            st.warning("Invalid recipient email address.")
        elif not sender_email or not password:
            st.warning("Sender email and password required.")
        else:
            try:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = recipient_email

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, [recipient_email], msg.as_string())

                st.success(f"✅ Email sent to {recipient_email}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
