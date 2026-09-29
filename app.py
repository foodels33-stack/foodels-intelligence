import streamlit as st
import pandas as pd

# הגדרת תצורת עמוד
st.set_page_config(
    page_title="פודלס - מערכת מודיעין עסקי",
    page_icon="🧠",
    layout="wide"
)

# CSS מותאם למובייל ולעברית בלי לשבור את המבנה של Streamlit
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif;
    }
    
    /* יישור טקסט לימין באזור המרכזי */
    [data-testid="stMainBlockContainer"] {
        direction: rtl;
        text-align: right;
    }
    
    /* יישור טקסט בסרגל הצד */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    
    /* עיצוב כפתורים */
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

api_key = st.sidebar.text_input("מפתח API (Gemini / OpenAI):", type="password")
st.sidebar.markdown("---")
st.sidebar.info("המערכת מנטרת מתחרים בבאר שבע, מודעות פייסבוק/אינסטגרם, וביקורות גוגל בזמן אמת.")

# כותרת ראשית
st.title("🎯 מערכת מודיעין תחרותי - פודלס")

# חלוקה לכרטיסיות עבודה
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 תובנות וקמפיינים", 
    "👁️ ניטור מודעות Meta", 
    "⭐ ביקורות גוגל", 
    "📈 טרנדים"
])

# --- כרטיסיה 1: מחולל קמפיינים ותובנות ---
with tab1:
    st.header("מחולל הצעות ערך וקמפיינים")
    st.write("המערכת מנתחת את נתוני המודיעין שנאספו ומפיקה המלצות לפעולה מידית.")
    
    focus_area = st.selectbox("בחר מוקד אסטרטגי:", [
        "מענה לחולשת מתחרה (משלוחים/שירות)",
        "קידום מזון רפואי/טיפולי",
        "מבצע מחיר אגרסיבי",
        "חיזוק מותג פרטי/בלעדי"
    ])
    
    target_audience = st.selectbox("קהל יעד:", [
        "בעלי כלבים בבאר שבע והסביבה",
        "בעלי חתולים (ציוד ומזון)",
        "לקוחות שנוטשים מתחרים",
        "קהל כללי בשכונת רמות"
    ])
        
    if st.button("גזור תובנות והפק רעיון לקמפיין ✨"):
        if not api_key:
            st.warning("אנא הזן מפתח API בתפריט הצד כדי להפעיל את מנוע ה-AI.")
        else:
            st.success("המודיעין עובד! הנה הצעה לקמפיין ממוקד:")
            st.markdown("""
            > **קמפיין מוצע:** "למה לחכות 3 ימים למשלוח?"  
            > **הטריגר המודיעיני:** זוהו 12 תלונות בשבוע האחרון על איחורי משלוחים אצל מתחרה X בבאר שבע.  
            > **המסר:** "בפודלס משלוח מגיע באותו היום עד פתח הבית בבאר שבע! מזמינים עכשיו – הציוד אצלכם בערב."  
            > **Call to Action:** להזמנה מהירה בוואטסאפ / באתר.
            """)

# --- כרטיסיה 2: ניטור מודעות מתחרים ---
with tab2:
    st.header("מעקב מודעות (Meta Ad Library)")
    st.caption("סריקת קמפיינים ממומנים של חנויות חיות באזור הדרום")
    
    ads_data = pd.DataFrame({
        "מתחרה": ["חנות X", "חנות Y", "רשת Z"],
        "סוג המבצע": ["15% הנחה על שק שני", "משלוח חינם מ-200 ש״ח", "מתנה בכל קנייה"],
        "תאריך זיהוי": ["2026-09-28", "2026-09-27", "2026-09-25"],
        "סטטוס": ["פעיל", "פעיל", "הסתיים"]
    })
    
    st.dataframe(ads_data, use_container_width=True)

# --- כרטיסיה 3: ניתוח ביקורות גוגל ---
with tab3:
    st.header("סורק ביקורות גוגל")
    st.write("זיהוי נקודות תורפה אצל מתחרים בבאר שבע.")
    
    competitor_name = st.text_input("שם חנות/מתחרה לסריקה:", "חנות חיות באר שבע")
    
    if st.button("סרוק ביקורות אחרונות 🔍"):
        st.info(f"סורק ביקורות עבור {competitor_name}...")
        st.error("⚠️ מופע נקודת תורפה: 35% מהביקורות השליליות בחודש האחרון ציינו 'חוסר במענה טלפוני'.")
        st.success("💡 הזדמנות עבור פודלס: להבליט שירות לקוחות אישי ומהיר בטלפון/בוואטסאפ.")

# --- כרטיסיה 4: טרנדים ושיח ---
with tab4:
    st.header("טרנדים בשיח החברתי")
    st.write("מילות מפתח ומוצרים שמתחילים לצבור פופולריות.")
    
    st.metric(label="דרישה למזון היפואלרגני", value="+24%", delta="עלייה החודש")
    st.metric(label="חיפוש צעצועים אינטראקטיביים לחתולים", value="+18%", delta="עלייה החודש")
