# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai

# 1. עיצוב RTL (ימין לשמאל)
st.set_page_config(page_title="שף כשר AI", page_icon="🍲", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: RTL;
        unicode-bidi: embed;
    }
    .main, .stTextInput, .stButton, .stMarkdown, p, h1, h2, h3, div {
        direction: RTL;
        text-align: right;
    }
    input, textarea { 
        direction: RTL !important; 
        text-align: right !important;
    }
    div.stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    .recipe-container {
        background-color: #f1f3f4;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. הגדרת המפתח והמודל
api_key = st.secrets.get("GEMINI_KEY")

# בדוק את קיום המפתח
if not api_key:
    st.error("❌ חסר מפתח API ב-Secrets!")
    st.stop()

# הגדר את המודל
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ שגיאה בהגדרת המודל: {str(e)}")
    st.stop()

st.title("🍲 שף כשר - מתכונים אוטומטיים")

# קלט מהמשתמש
ingredients = st.text_input(
    "מה המצרכים?", 
    placeholder="למשל: דג, שום, שמן זית, תמונה..."
)

# כפתור הפעלה
if st.button("🍳 בשל לי מתכון!"):
    # בדיקות תקינות
    if not ingredients.strip():
        st.warning("⚠️ נא להזין מצרכים לפחות.")
    elif len(ingredients) > 500:
        st.warning("⚠️ המצרכים ארוכים מדי. נא להקצר ל-500 תווים או פחות.")
    else:
        try:
            with st.spinner('👨‍🍳 השף בעבודה...'):
                # יצירת הנחיה טובה יותר
                prompt = f"""אתה שף כשר מנוסה ומחובר מאוד. 
כתוב מתכון כשר, טעים, פשוט וקל להכנה בעברית.

המצרכים: {ingredients}

כתוב את המתכון בפורמט הבא:
חומרים:
(רשום את כל החומרים הדרושים)

הוראות הכנה:
(רשום שלב אחר שלב)

טיפים:
(הוסף טיפים שימושיים או חלופות)"""
                
                response = model.generate_content(prompt)
                
                # בדיקת תקינות התשובה
                if response.text and response.text.strip():
                    st.success("✅ הנה המתכון המעולה:")
                    st.markdown(f"""
                    <div class="recipe-container">
                    {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ לא הצלחנו ליצור מתכון. נא לנסות שוב עם מצרכים אחרים.")
                    
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("❌ שגיאה 429: המכסה היומית נגמרה. נסה שוב בעוד דקות או החלף מפתח.")
            elif "404" in error_msg:
                st.error("❌ שגיאה 404: המודל לא נמצא. וודא שה-requirements מעודכן.")
            elif "401" in error_msg or "403" in error_msg:
                st.error("❌ שגיאה בהרשאה: בדוק את מפתח ה-API שלך.")
            else:
                st.error(f"❌ חלה שגיאה: {error_msg}")

# Footer
st.markdown("---")
st.markdown("💚 **שף כשר AI** - הגרסה המשופרת | מופעל ע\"י Gemini 1.5 Flash")
