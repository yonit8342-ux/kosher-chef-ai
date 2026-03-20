import streamlit as st
import requests

# עיצוב RTL (הצמדה לימין) - בדיוק כמו שביקשת
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# שליפת המפתח מה-Secrets
api_key = st.secrets.get("GEMINI_KEY")

st.title("🍲 שף כשר AI - גרסה מתוקנת")
ingredients = st.text_input("מה נבשל היום?", placeholder="הכנס מצרכים...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        with st.spinner('מתחבר לשרת...'):
            # הכתובת היציבה ביותר שמונעת שגיאות 404
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}"}]}]}
            
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    recipe = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("הנה המתכון:")
                    st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px;">{recipe}</div>', unsafe_allow_html=True)
                elif response.status_code == 429:
                    st.error("עומס זמני על המפתח (429). המתן דקה ונסה שוב.")
                else:
                    st.error(f"שגיאה {response.status_code}: וודא שמפתח ה-API תקין.")
            except Exception as e:
                st.error(f"תקלה בחיבור: {e}")
