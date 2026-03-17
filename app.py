import streamlit as st
import google.generativeai as genai

# 1. עיצוב RTL והצמדה לימין
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL;
        text-align: right;
    }
    input {
        direction: RTL !important;
        text-align: right !important;
    }
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
    # שימוש במודל 2.0-flash - המודל הכי עדכני ומהיר
    model = genai.GenerativeModel('gemini-2.0-flash')

# 3. ממשק המשתמש
st.title("🍲 שף בינה מלאכותית כשר")
st.write("הזינו מצרכים לקבלת מתכון כשר (מעוצב לימין):")

ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, אורז, פפריקה...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        try:
            with st.spinner('השף מפיק מתכון...'):
                response = model.generate_content(f"אתה שף כשר מומחה. כתוב מתכון כשר, ברור וטעים בעברית עבור המצרכים הבאים: {ingredients}")
                st.success("הנה המתכון המבוקש:")
                st.markdown(f"""
                <div style="direction: RTL; text-align: right; background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            if "429" in str(e):
                st.error("המכסה היומית נגמרה. גוגל מגבילה את המודל הזה בגרסה החינמית, נסה שוב בעוד כמה דקות.")
            else:
                st.error(f"חלה שגיאה: {e}")
    else:
        st.warning("נא להזין מצרכים.")
