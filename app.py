import streamlit as st
import google.generativeai as genai

# הגדרת המפתח שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# הגדרות דף ויישור לימין
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL; text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍲 שף בינה מלאכותית")
st.write("הזינו מצרכים והשף יבנה לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, עוף, בצל...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף מתחבר לשרת...'):
            try:
                # שימוש בשם המודל בלבד (זה יפנה לגרסה היציבה אוטומטית)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"צור מתכון כשר ופשוט בעברית עבור: {ingredients}")
                
                if response.text:
                    st.success("הנה המתכון שלך:")
                    st.markdown("---")
                    st.write(response.text)
            except Exception as e:
                st.error("התחברות נכשלה.")
                st.caption(f"פרטי שגיאה: {str(e)}")
    else:
        st.warning("נא להזין מצרכים.")
