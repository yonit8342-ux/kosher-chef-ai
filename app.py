import streamlit as st
import requests

st.title("אבחון מודלים זמינים")

api_key = "AIzaSyAial-YtGsqJ8ez7ZZRr7VChxbUJklKq8M"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

if st.button("בדוק מודלים זמינים"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models_data = response.json()
            st.success("התחברות הצליחה! הנה המודלים שזמינים עבורך:")
            for model in models_data.get('models', []):
                st.write(f"**שם המודל:** `{model['name']}`")
                st.write(f"פעולות נתמכות: {model['supportedGenerationMethods']}")
                st.write("---")
        else:
            st.error(f"שגיאה {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"שגיאה בחיבור: {e}")
