import streamlit as st
import google.generativeai as genai

# הגדרות דף ועיצוב RTL (הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""<style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3 {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# הגדרת ה-API
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # שימוש במודל היציב ביותר למניעת שגיאות 404
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🍲 שף כשר - תיקון סופי")
ingredients = st.text_input("מה נבשל?", placeholder="הכנס מצרכים כאן...")

if st.button("צור מתכון כשר"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        try:
            with st.spinner('השף מכין את המתכון...'):
                response = model.generate_content(f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                st.success("הנה המתכון:")
                st.markdown(f'<div style="direction: RTL; text-align: right; background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">{response.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            if "429" in str(e):
                st.error("הגענו למכסה המקסימלית (Quota). גוגל מגבילה את המפתח בגרסה החינמית, נסה שוב בעוד דקה.")
            else:
                st.error(f"שגיאה: {e}")
