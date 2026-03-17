import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="שף כשר AI", page_icon="🍲")

# עיצוב RTL
st.markdown("""<style>
    .main { direction: RTL; text-align: right; }
    .stTextInput>div>div>input { direction: RTL; text-align: right; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# שימוש במפתח (וודא שהחלפת למפתח חדש ב-Secrets או בקוד)
try:
    # מנסה למשוך מה-Secrets, אם אין - לוקח מהקוד (למצבי חירום)
    api_key = st.secrets.get("GEMINI_KEY", "כאן_שמים_מפתח_חדש_אם_אין_סיקרטס")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"שגיאה בהגדרת המפתח: {e}")

st.title("🍲 שף בינה מלאכותית כשר")
ingredients = st.text_input("מה נבשל?", placeholder="למשל: עוף, בצל...")

if st.button("צור מתכון"):
    if ingredients:
        placeholder = st.empty()
        placeholder.info("השף בודק את המצרכים... (זה אמור לקחת עד 5 שניות)")
        
        try:
            # הוספת הגבלת זמן ודרישה לתשובה קצרה כדי שירוץ מהר
            response = model.generate_content(
                f"כתוב מתכון כשר, קצר וטעים בעברית עבור: {ingredients}. תענה רק את המתכון.",
                generation_config={"timeout": 10}
            )
            
            if response.text:
                placeholder.empty()
                st.success("הנה המתכון:")
                st.markdown(f'<div style="direction: RTL; text-align: right;">{response.text}</div>', unsafe_allow_html=True)
            else:
                placeholder.error("המודל החזיר תשובה ריקה. נסה שוב.")
        except Exception as e:
            placeholder.empty()
            st.error("חלה שגיאה בחיבור.")
            if "API_KEY_INVALID" in str(e) or "403" in str(e):
                st.warning("המפתח נחסם שוב (Leaked). עליך להנפיק חדש ולשים ב-Secrets.")
            else:
                st.code(str(e))
    else:
        st.warning("הכנס מצרכים קודם.")
