import streamlit as st
import google.generativeai as genai

# הגדרת המפתח של גוגל
GOOGLE_API_KEY = "AIzaSyDl0NKD7aRmNGUmVKQQAxUpDdCgEo3RSjU"
genai.configure(api_key=GOOGLE_API_KEY)

# הגדרת דף (חייב להופיע ראשון)
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# הזרקת קוד CSS ליישור לימין (RTL) לכל האתר
st.markdown("""
    <style>
    /* יישור הטקסט והכיוון לימין */
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL;
        text-align: right;
    }
    
    /* יישור תיבת הקלט */
    input {
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* התאמת הכותרות */
    h1, h2, h3 {
        direction: RTL;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# כותרת האתר
st.title("🍲 שף בינה מלאכותית")
st.write("הזינו מצרכים וקבלו מתכון כשר וטעים!")

# תיבת קלט מהמשתמש
ingredients = st.text_input("מה המצרכים שיש לך?", "תפוחי אדמה, שמן, מלח")

if st.button("צור מתכון"):
    if ingredients:
        with st.spinner('השף בעבודה...'):
            try:
                # שימוש במודל היציב ביותר
                model = genai.GenerativeModel('models/gemini-flash-latest')
                
                # יצירת הבקשה
                prompt = f"יש לי את המצרכים הבאים: {ingredients}. תכתוב לי בבקשה מתכון כשר, טעים ופשוט להכנה בשפה העברית."
                
                response = model.generate_content(prompt)
                
                st.success("הנה המתכון המנצח:")
                st.markdown("---")
                # הצגת התוצאה
                st.write(response.text)
                
            except Exception as e:
                if "429" in str(e):
                    st.error("יותר מדי בקשות. בבקשה המתינו דקה ונסו שוב.")
                else:
                    st.error("חלה שגיאה בחיבור.")
                    st.code(str(e))
    else:
        st.warning("נא להזין מצרכים.")

st.markdown("---")
st.caption("נוצר על ידי השף הדיגיטלי | Gemini Flash")
st.markdown(f"![Views](https://hits.dwyl.com/yonit8342-ux/kosher-chef-ai.svg)")
