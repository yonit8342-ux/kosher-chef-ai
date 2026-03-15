import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח האישי שלך
GOOGLE_API_KEY = "AIzaSyAwRvhLE2Aft8KSNiCqNol_nmVHOh1Y1TY"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. הגדרות דף
st.set_page_config(page_title="שף בינה מלאכותית", page_icon="🍲")

# 3. עיצוב יישור לימין (RTL)
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, div[data-testid="stMarkdownContainer"] {
        direction: RTL;
        text-align: right;
    }
    input {
        direction: RTL !important;
        text-align: right !important;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- תוכן האתר ---
st.title("🍲 שף בינה מלאכותית")
st.write("שלום! כתבו את המצרכים שיש לכם בבית, והשף יבנה לכם מתכון כשר וטעים.")

ingredients = st.text_input("מה יש לנו במטבח?", placeholder="למשל: תפוחי אדמה, פטריות, בצל...")

if st.button("צור מתכון עכשיו"):
    if ingredients:
        with st.spinner('השף מתחבר לשרת היציב...'):
            try:
                # שימוש במודל Gemini 1.5 Flash - בגרסה היציבה
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"צור מתכון כשר, פשוט וטעים בעברית המבוסס על המצרכים הבאים: {ingredients}. כתוב את המתכון עם רשימת מצרכים מסודרת והוראות הכנה בשלבים."
                
                # יצירת התוכן
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("הנה המתכון שלך:")
                    st.markdown("---")
                    st.write(response.text)
                else:
                    st.error("לא התקבל תוכן. נסה שוב.")
                    
            except Exception as e:
                # אם עדיין יש שגיאת 404, זה אומר שהספרייה צריכה עדכון
                st.error("השף נתקל בקושי בחיבור לשרת גוגל.")
                if "404" in str(e):
                    st.warning("שרת גוגל עדיין מפנה לגרסה ישנה. נסו שוב בעוד דקה.")
                else:
                    st.caption(f"פרטים טכניים: {str(e)}")
    else:
        st.warning("נא להזין לפחות מצרך אחד.")

st.markdown("---")
st.caption("השף הדיגיטלי מוכן | המדידה פעילה")
