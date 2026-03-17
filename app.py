import streamlit as st
import requests

st.title("בדיקת מודלים זמינים")

api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("חסר מפתח API ב-Secrets!")
else:
    # בקשה לקבלת רשימת המודלים
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            st.success("הצלחנו להתחבר! הנה המודלים הזמינים עבורך:")
            # מציג רק את שמות המודלים כדי שיהיה קריא
            models = [m['name'] for m in data.get('models', [])]
            for m in models:
                st.write(f"✅ {m}")
        else:
            st.error(f"שגיאה מהשרת: {data.get('error', {}).get('message', 'Unknown Error')}")
            st.write(data)
    except Exception as e:
        st.error(f"שגיאה בחיבור: {e}")
