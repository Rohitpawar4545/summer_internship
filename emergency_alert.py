import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# 1. Sample Data (You can replace this with a real dataset)
data = {
    "message": [
        "My father is unconscious and not breathing",            # Real
        "I just want to test how fast you respond",              # Fake
        "There's been a car accident outside my home",           # Real
        "Send ambulance quickly or I will sue",                  # Fake
        "My child fell down and is bleeding badly",              # Real
        "No emergency, just needed a ride",                      # Fake
        "There is a fire and someone is trapped inside",         # Real
        "I was bored and wanted to see the ambulance",           # Fake
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0]  # 1 = Real, 0 = Fake
}
df = pd.DataFrame(data)

# 2. Pipeline: TF-IDF + Naive Bayes
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

model.fit(df['message'], df['label'])

# 3. Streamlit UI
st.title("🚑Fake Emergency Detector")

user_input = st.text_area("Enter Emergency Description", "")

if st.button("Check"):
    prediction = model.predict([user_input])[0]
    prob = model.predict_proba([user_input])[0][prediction]

    if prediction == 1:
        st.success(f"✅ This appears to be a *Real Emergency* (Confidence: {prob:.2f})")
    else:
        st.error(f"🚫 This might be a *Fake Emergency* (Confidence: {prob:.2f})")







