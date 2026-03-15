import streamlit as st
import google.generativeai as genai

# הגדרת המפתח שייצרת
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# כותרת ועיצוב RTL
st.markdown("<h1 style='text-align: right;'>🍲 שף בינה מלאכותית</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right;'>הזינו מצרכים והשף יבנה לכם מתכון כשר.</p>", unsafe_allow_html=True)

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, בצל, עוף...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('מתחבר לשרת גוגל...'):
            try:
                # שימוש בגרסה היציבה בלבד
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"צור מתכון כשר ופשוט בעברית עבור: {ingredients}")
                
                if response.text:
                    st.success("הנה המתכון שלך:")
                    st.write(response.text)
            except Exception as e:
                st.error("השף נתקל בבעיה.")
                st.caption(f"פרטי שגיאה: {str(e)}")
