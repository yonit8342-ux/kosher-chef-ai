import streamlit as st
import google.generativeai as genai
import time

# 1. עיצוב RTL מלא (אנטילקס)
st.set_page_config(page_title="שף כשר AI - גרסת על", page_icon="🍲")

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

# 2. הגדרות API
api_key = st.secrets.get("GEMINI_KEY")

# רשימת המודלים לניסיון לפי סדר עדיפות
MODELS_TO_TRY = [
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-2.0-flash-lite-001'
]

st.title("🍲 שף כשר - סורק מודלים חכם")
st.write("המערכת תנסה את כל המודלים הזמינים עד למציאת מתכון.")

ingredients = st.text_input("מה המצרכים?", placeholder="למשל: דג, לימון, פטרוזיליה...")

if st.button("צור מתכון כשר (נסה הכל)"):
    if not api_key:
        st.error("חסר מפתח API ב-Secrets!")
    elif ingredients:
        success = False
        genai.configure(api_key=api_key)
        
        # יצירת סטטוס ויזואלי לסריקה
        with st.status("מחפש מודל פנוי...") as status:
            for model_name in MODELS_TO_TRY:
                try:
                    status.write(f"בודק את מודל: {model_name}...")
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        f"אתה שף כשר. כתוב מתכון כשר וטעים בעברית עבור: {ingredients}",
                        generation_config={"max_output_tokens": 1000}
                    )
                    
                    if response.text:
                        status.update(label=f"נמצא מודל פנוי! ({model_name})", state="complete")
                        st.success(f"המתכון נוצר בהצלחה:")
                        st.markdown(f"""
                        <div style="direction: RTL; text-align: right; background-color: #f1f3f4; padding: 20px; border-radius: 10px; border: 1px solid #34a853;">
                        {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                        success = True
                        break
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str:
                        status.write(f"❌ {model_name} עמוס (Quota).")
                    elif "404" in error_str:
                        status.write(f"❌ {model_name} לא נתמך כרגע.")
                    else:
                        status.write(f"⚠️ שגיאה ב-{model_name}: {error_str[:50]}...")
                    continue # עובר למודל הבא ברשימה
            
            if not success:
                status.update(label="כל המודלים נכשלו", state="error")
                st.error("לצערי כל המודלים עמוסים כרגע. גוגל מגבילה את המפתח שלך. נסה שוב בעוד 5 דקות.")
    else:
        st.warning("נא להזין מצרכים.")
