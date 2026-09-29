import streamlit as st
import pandas as pd
import google.generativeai as genai

# הגדרת תצורת עמוד
st.set_page_config(
    page_title="פודלס - מערכת מודיעין עסקי",
    page_icon="🧠",
    layout="wide"
)

# CSS מותאם למובייל ולעברית (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif;
    }
    [data-testid="stMainBlockContainer"], [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B00;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# תפריט צד (Sidebar)
st.sidebar.title("🧠 פודלס מודיעין")
st.sidebar.subheader("מרכז שליטה")

# בדיקה וטעינה מתוך ה-Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("🔑 מפתח API מחובר מ-Secrets")
else:
    api_key = st.sidebar.text_input("מפתח API (Gemini):", type="password")

st.sidebar.markdown("---")
st.sidebar.info("המערכת מנטרת מתחרים בבאר שבע ומפיקה תובנות AI בזמן אמת.")

# כותרת ראשית
st.title("🎯 מערכת מודיעין תחרותי - פודלס")

tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 תובנות וקמפיינים", 
    "👁️ ניטור מודעות Meta", 
    "⭐ ביקורות גוגל", 
    "📈 טרנדים"
])

# --- כרטיסיה 1: מחולל קמפיינים מבוסס AI ---
with tab1:
    st.header("מחולל הצעות ערך וקמפיינים")
    st.write("בחר מיקוד, וה-AI ייצר עבורך קמפיין שיווקי מלא לפודלס.")
    
    focus_area = st.selectbox("בחר מוקד אסטרטגי:", [
        "מענה לחולשת מתחרה (עיכוב במשלוחים)",
        "קידום מזון רפואי/טיפולי",
        "מבצע מחיר אגרסיבי למשיכת לקוחות חדשים",
        "חיזוק המותג ושירות הלקוחות האישי"
    ])
    
    target_audience = st.selectbox("קהל יעד:", [
        "בעלי כלבים בבאר שבע והסביבה",
        "בעלי חתולים",
        "לקוחות שנוטשים מתחרים באזור",
        "סטודנטים וצעירים בשכונת רמות"
    ])
        
    if st.button("גזור תובנות והפק רעיון לקמפיין ✨"):
        if not api_key:
            st.warning("⚠️ לא נמצא מפתח API. ודא שהגדרת GEMINI_API_KEY ב-Secrets ב-Streamlit.")
        else:
            try:
                # חיבור ל-Gemini API עם דגם מודל עדכני
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # הפרומפט המודיעיני ל-AI
                prompt = f"""
                אתה מומחה שיווק וקופירייטר שעובד עבור חנות חיות בשם 'פודלס' בבאר שבע (שכונת רמות).
                צור רעיון לקמפיין שיווקי ממוקד וקצר על בסיס הנתונים הבאים:
                מוקד אסטרטגי: {focus_area}
                קהל יעד: {target_audience}
                
                הצג את התשובה בעברית קלילה ושיווקית, עם אמוג'ים, במבנה הבא:
                🎯 **כותרת קליטה לקמפיין**
                📝 **טקסט לפוסט/סטורי (כולל הומור קל)**
                💡 **הצעה לפעולה (Call to Action) להזמנה מהירה**
                """
                
                with st.spinner('ה-AI מנתח ומייצר קמפיין... 🧠'):
                    response = model.generate_content(prompt)
                    
                st.success("✅ הקמפיין מוכן!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"שגיאה בחיבור ל-API. ודא שהמפתח ב-Secrets תקין. שגיאה: {e}")

# --- שאר הכרטיסיות ---
with tab2:
    st.header("מעקב מודעות (Meta Ad Library)")
    st.info("כאן יופיעו בהמשך נתונים חיים מסריקת מודעות פייסבוק.")

with tab3:
    st.header("סורק ביקורות גוגל")
    st.info("כאן יופיע בהמשך ניתוח חי של ביקורות מתחרים.")

with tab4:
    st.header("טרנדים בשיח החברתי")
    st.info("כאן יופיעו מגמות חיפוש חמות בעולם החיות.")
