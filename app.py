import streamlit as st
import google.generativeai as genai

# 1. הגדרות דף ועיצוב RTL מלא (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# הזרקת CSS להצמדה לימין של כל רכיבי הדף
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3, div {
        direction: RTL;
        text-align: right;
    }
    /* תיקון ספציפי לשדות קלט */
    input {
        direction: RTL !important;
        text-align: right !important;
    }
    /* עיצוב כפתור */
    div.stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. הגדרת ה-API
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # שימוש במודל היציב ביותר ב-SDK
    model = genai.GenerativeModel('gemini-1.5-flash')

# 3. ממשק המשתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו מצרכים וקבלו מתכון כשר (מעוצב לימין):")

ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, תפוחי אדמה...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        try:
            with st.spinner('השף מפיק מתכון...'):
                response = model.generate_content(f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון שמצאתי:")
                # הצגת המתכון בתוך תיבה מעוצבת ומוצמדת לימין
                st.markdown(f"""
                <div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            if "429" in str(e):
                st.error("הגענו למכסה המקסימלית (שגיאה 429). גוגל מגבילה את המפתח בגרסה החינמית. נסה שוב בעוד דקה.")
            else:
                st.error(f"חלה שגיאה: {e}")
    else:
        st.warning("נא להזין מצרכים.")
