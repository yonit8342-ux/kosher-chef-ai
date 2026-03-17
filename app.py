import streamlit as st
import google.generativeai as genai

# 1. הגדרות דף ועיצוב RTL (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

st.markdown("""
    <style>
    /* הגדרת כיוון הטקסט לכל האפליקציה */
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL;
        text-align: right;
    }
    /* תיקון שדה הקלט שיהיה נוח לכתיבה בעברית */
    input {
        direction: RTL !important;
        text-align: right !important;
    }
    /* עיצוב כפתור */
    div.stButton > button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. הגדרת המפתח והמודל
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # שימוש במודל 1.5-flash-8b - מהיר ופנוי יותר
    model = genai.GenerativeModel('gemini-1.5-flash-8b')

# 3. ממשק המשתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו מצרכים וקבלו מתכון כשר מוצמד לימין:")

ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: דג, שום, שמן זית...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        try:
            with st.spinner('השף מנסה מודל מהיר...'):
                response = model.generate_content(f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון שמצאתי:")
                # הצגת המתכון בתוך תיבה מעוצבת ומוצמדת לימין
                st.markdown(f"""
                <div style="direction: RTL; text-align: right; background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            if "429" in str(e):
                st.error("גם המודל הזה עמוס כרגע. גוגל מגבילה את הבקשות בחינם, כדאי לחכות דקה.")
            else:
                st.error(f"שגיאה בחיבור: {e}")
    else:
        st.warning("בבקשה הזינו מצרכים קודם.")
