import streamlit as st
import google.generativeai as genai

# הגדרת המפתח של גוגל
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

st.title("🍲 שף בינה מלאכותית - פתרון סופי")
st.write("הזינו מצרכים וקבלו מתכון כשר וטעים!")

# תיבת קלט
ingredients = st.text_input("מה המצרכים שיש לך?", "חזה עוף, בצל, סילאן")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('מתחבר לשרת...'):
            try:
                # שימוש בשם המדויק שהופיע ברשימה שלך
                model = genai.GenerativeModel('models/gemini-flash-latest')
                
                prompt = f"יש לי את המצרכים הבאים: {ingredients}. תכתוב לי בבקשה מתכון כשר, טעים ופשוט להכנה בשפה העברית."
                
                response = model.generate_content(prompt)
                
                st.success("הנה המתכון:")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                # אבחון נוסף במקרה של שגיאה
                st.error("חלה שגיאה בחיבור.")
                st.code(str(e))
    else:
        st.warning("נא להזין מצרכים.")

st.markdown("---")
st.caption("מבוסס על מודל Gemini Flash")
