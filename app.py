import streamlit as st
import google.generativeai as genai

# 1. עיצוב אנטילקס (RTL - הצמדה לימין)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲")
st.markdown("""
    <style>
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3, div {
        direction: RTL;
        text-align: right;
    }
    input { direction: RTL !important; text-align: right !important; }
    div.stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. הגדרת המפתח והמודל
api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # שימוש בשם המודל המדויק שעבד בעבר
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🍲 שף כשר - הגרסה המקורית")
ingredients = st.text_input("מה המצרכים?", placeholder="למשל: דג, שום, שמן זית...")

if st.button("בשל לי מתכון!"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        try:
            with st.spinner('השף בעבודה...'):
                # פנייה למודל ליצירת תוכן
                response = model.generate_content(f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}")
                
                if response.text:
                    st.success("הנה המתכון:")
                    st.markdown(f"""
                    <div style="direction: RTL; text-align: right; background-color: #f1f3f4; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                    {response.text}
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("שגיאה 429: המכסה היומית נגמרה. נסה שוב בעוד דקה או החלף מפתח.")
            elif "404" in error_msg:
                st.error("שגיאה 404: המודל לא נמצא. וודא שקובץ ה-requirements מעודכן.")
            else:
                st.error(f"חלה שגיאה: {error_msg}")
    else:
        st.warning("נא להזין מצרכים.")
