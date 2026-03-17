import streamlit as st
import google.generativeai as genai

# 1. הגדרות דף ועיצוב RTL (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

st.markdown("""
    <style>
    /* הצמדה לימין של כל רכיבי הדף */
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL;
        text-align: right;
    }
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

# 2. הגדרת המפתח והמודל
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # שימוש בשם המודל המדויק למניעת שגיאת 404
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🍲 שף כשר - פתרון שגיאת 404")
st.write("הזינו מצרכים לקבלת מתכון כשר (מעוצב לימין):")

ingredients = st.text_input("מה נבשל היום?", placeholder="למשל: עוף, תפוחי אדמה...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        try:
            with st.spinner('מתחבר לשרת גוגל...'):
                # שליחת הבקשה למודל
                response = model.generate_content(f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון שמצאתי:")
                # הצגת המתכון בתיבה מוצמדת לימין
                st.markdown(f"""
                <div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            # טיפול בשגיאות מכסה (429) או שגיאות אחרות
            error_msg = str(e)
            if "429" in error_msg:
                st.error("הגענו למכסה המקסימלית. גוגל מגבילה את המפתח בגרסה החינמית. נסה שוב בעוד דקה.")
            elif "404" in error_msg:
                st.error("שגיאה 404: המודל לא נמצא. וודא שמותקנת הגרסה העדכנית של google-generativeai.")
            else:
                st.error(f"חלה שגיאה: {e}")
    else:
        st.warning("נא להזין מצרכים.")
