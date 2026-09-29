import pandas as pd
import requests
import streamlit as st

# הגדרת תצורת עמוד
st.set_page_config(
    page_title="פודלס - מודיעין שוק וטרנדים חינם", page_icon="📡", layout="wide"
)

# CSS מותאם למובייל ולעברית (RTL)
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


# פונקציה לשליפת מגמות והשלמות חיפוש אמיתיות מגוגל בחינם (ללא API)
@st.cache_data(ttl=3600)
def get_google_suggestions(query):
  try:
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}&hl=he"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
      data = response.json()
      return data[1] if len(data) > 1 else []
  except Exception:
    pass
  return []


# תפריט צד (Sidebar)
st.sidebar.title("📡 רדאר פודלס")
st.sidebar.subheader("מודיעין עורפי חינמי")
st.sidebar.success("✅ מערכת ניטור חיפוש פעילה")
st.sidebar.markdown("---")
st.sidebar.info(
    "שליפת מילות מפתח וביקושים אמיתיים היישר ממנוע החיפוש של גוגל, ללא עלות וללא"
    " כרטיס אשראי."
)

# כותרת ראשית
st.title("📡 רדאר מודיעין וטרנדים - פודלס (באר שבע)")

tab1, tab2, tab3 = st.tabs([
    "🔍 בדיקת מילות מפתח חיות בגוגל",
    "📊 השוואת מוצרים מבוקשים בדרום",
    "🎯 מחולל קמפיינים בהתאמה לביקושים",
])

# --- כרטיסיה 1: בדיקת מילות מפתח חיות מגוגל ---
with tab1:
  st.header("🔍 חיפוש חי במנוע של גוגל (בזמן אמת)")
  st.write(
      "בדוק מה אנשים באמת מקלידים ומחפשים עכשיו בגוגל סביב מוצרי חיות מחמד,"
      " מזון וציוד."
  )

  search_term = st.text_input(
      "הקלד נושא לחיפוש (למשל: אוכל לכלבים, חול לחתולים, חטיפים):",
      "אוכל לכלבים",
  )

  if st.button("שלוף את מה שאנשים מחפשים בגוגל 🚀"):
    with st.spinner("שואב נתונים חיים מגוגל..."):
      suggestions = get_google_suggestions(search_term)

    if suggestions:
      st.success(
          f"✅ נמצאו {len(suggestions)} חיפושים פופולריים שאנשים מבצעים עכשיו:"
      )
      for i, item in enumerate(suggestions, 1):
        st.markdown(f"**{i}.** 🔎 `{item}`")
      st.info(
          "💡 **תובנה לפודלס:** כדאי לשלב את הביטויים האלו בתיאורים, בפוסטים"
          " שאתה מוציא, או לתת מענה מדויק ללקוחות שמגיעים לחנות ברחוב נחום"
          " שריג."
      )
    else:
      st.warning(
          "לא נמצאו תוצאות כרגע, נסה מילת חיפוש אחרת (למשל: 'חתולים',"
          " 'ציוד לכלבים')."
      )

# --- כרטיסיה 2: השוואת מוצרים מבוקשים ---
with tab2:
  st.header("📊 מגמות חיפוש חמות בדרום לפי קטגוריות")
  st.write(
      "ניתוח מהיר של מה שבעלי חיות מחמד בבאר שבע מקלידים בדרך כלל כשהם צריכים"
      " מענה דחוף."
  )

  category_choice = st.selectbox("בחר קטגוריה לניתוח ביקושים:", [
      "מזון יבש רפואי והיפואלרגני",
      "ציוד ופתרונות לחתולים (חול/שירותים)",
      "חטיפי אילוף ומוצרי פינוק",
  ])

  if st.button("הצג תמונת מצב ביקושים 📈"):
    if "מזון יבש" in category_choice:
      queries = [
          "אוכל היפואלרגני לכלב באר שבע",
          "אוכל רפואי לחתולים",
          "שק אוכל גדול לכלב משלוח חינם",
      ]
    elif "ציוד ופתרונות לחתולים" in category_choice:
      queries = [
          "חול מתגבש לחתולים מומלץ",
          "חול שלא עושה אבק",
          "אוכל לחתולים רגישים",
      ]
    else:
      queries = [
          "חטיפי אילוף לכלבים",
          "עצמות לכלבים במחיר טוב",
          "צעצועי השחתה לכלבים",
      ]

    st.success("🎯 הביטויים המובילים שמובילים קונים לחנויות כרגע:")
    for q in queries:
      sub_sug = get_google_suggestions(q)
      st.markdown(f"📌 **מונח מרכזי:** `{q}`")
      if sub_sug:
        st.caption(
            f"   חיפושים נלווים של אנשים: {', '.join(sub_sug[:3])}"
            if len(sub_sug) >= 3
            else f"   חיפושים נלווים: {', '.join(sub_sug)}"
        )

# --- כרטיסיה 3: מחולל קמפיינים ---
with tab3:
  st.header("🎯 מחולל קמפיינים מבוסס ביקושי אמת")
  st.write(
      "צור פוסטים ושיווק ממוקד המבוסס על מה שצרכנים באמת מחפשים ומבקשים בפתרונות"
      " מיידיים."
  )

  campaign_type = st.selectbox("בחר את סוג המסר השיווקי:", [
      "מבצע משיכה לתושבי רמות (איסוף מהיר בלי עומסים)",
      "פתרון מהיר למזון רגיש / היפואלרגני",
      "חבילת סטרטר והתאמה אישית לגורים חדשים",
  ])

  if st.button("צור טקסט פרסומי מוכן ✨"):
    st.success("📋 הפוסט שלך מוכן לפרסום:")

    if "רמות" in campaign_type:
      st.markdown("""
            🐾 **תושבי שכונת רמות והסביבה!** 🐾  
            מחפשים את האוכל והציוד לחיות המחמד שלכם בלי לנסוע רחוק, בלי לעמוד בפקקים ובלי לחכות למשלוחים שמתעכבים?  
            קפצו אלינו ל**פודלס** ברחוב נחום שריג 33. חונים ממש ליד, נכנסים, מקבלים שירות אישי ויוצאים בשתי דקות!  
            📞 דברו איתנו: 054-5652422 / 08-6655443. מחכים לכם! ❤️
            """)
    elif "רגיש" in campaign_type:
      st.markdown("""
            🥩 **הכלב רגיש באוכל או מתגרד? אל תנחשו לבד!** 🥩  
            רבים מחפשים פתרונות תזונה מתקדמים ומזון היפואלרגני שבאמת עוזר. בואו להתייעץ איתנו בפודלס (נחום שריג 33, רמות, באר שבע) ונמצא יחד את המזון המדויק שהחבר הפרוותי שלכם צריך.  
            📞 התקשרו או קפצו לחנות: 054-5652422 / 08-6655443. נתראה! 🐕
            """)
    else:
      st.markdown("""
            🎉 **מזל טוב על הגור החדש במשפחה!** 🎉  
            מתלבטים איזה חטיפי אילוף או איזה ציוד באמת צריך בהתחלה? אנחנו בפודלס (שכונת רמות, נחום שריג 33) הכנו עבורכם ערכות התחלה חכמות ומותאמות אישית לגורים.  
            📞 קפצו להכיר אותנו: 054-5652422 / 08-6655443. מחכים לכם ולפרוותי החדש! 🐶🐱
            """)
