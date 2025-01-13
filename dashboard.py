import streamlit as st

# يجب أن يكون st.set_page_config() أول أمر يتم تنفيذه
st.set_page_config(layout="wide")

# استيراد المكتبات الأخرى بعد st.set_page_config()
import os
from html_viewer import display_html  # استيراد الدالة لعرض HTML
from pdf_viewer import display_pdf  # استيراد الدالة لعرض PDF
from books_manager import show_books_list, show_book_content, show_summary_content  # استيراد الدوال الجديدة


# التحقق من كلمة المرور
def check_password():
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        password_input = st.text_input("أدخل كلمة المرور:", type="password")
        if password_input == st.secrets["password"]:
            st.session_state.password_correct = True
        else:
            st.error("كلمة المرور غير صحيحة.")
            st.stop()
    return st.session_state.password_correct

if not check_password():
    st.stop()


# Custom CSS for RTL layout, Arabic font, and Tahoma font
st.markdown(
    """
    <style>
        /* RTL and Arabic Font Styling */
        body, [class*="css"], h1, h2, h3, h4, h5, h6, p, div, span, a, button, label, input, textarea {
            direction: rtl;
            text-align: right;
            font-family: Tahoma, Arial, sans-serif !important;
        }

        /* Title Styling */
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
        }

        /* Ensure scrollable iframe */
        iframe {
            overflow: auto;
        }

        /* Remove Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* زيادة حجم النص في الشريط الجانبي */
        div[data-testid="stSidebar"] .stButton button, 
        div[data-testid="stSidebar"] .stMarkdown, 
        div[data-testid="stSidebar"] .stExpander label {
            font-size: 24px !important;  # حجم الخط
            font-weight: bold !important;  # سمك الخط
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Full-width Banner with Image using use_container_width
st.image("images/banner_2.png", use_container_width=True)  # تم تغيير الصورة إلى banner_2.png

# Sidebar with Toggle Lists using st.expander and Updated Menu Items
st.sidebar.title("🔍 التنقل")

# State to control the dynamic workspace
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "🌸 بداية القصة والمشروع"
if 'selected_book' not in st.session_state:
    st.session_state.selected_book = None

# Sidebar Options with Expandable Sections
with st.sidebar.expander("🌸 بداية القصة والمشروع"):
    if st.button("عرض الصفحة", key="home"):
        st.session_state.selected_page = "🌸 بداية القصة والمشروع"
        st.session_state.selected_book = None

# 🔎 البحث Section with Multiple Choices
with st.sidebar.expander("🔎 البحث"):
    if st.button("اعرض البحث", key="view_html"):
        st.session_state.selected_page = "🔎 اعرض البحث"
        st.session_state.selected_book = None
    if st.button("اعرض البحث بصيغة PDF", key="view_pdf"):
        st.session_state.selected_page = "🔎 اعرض البحث بصيغة PDF"
        st.session_state.selected_book = None

# 📖 النظرية Section with Multiple Choices
with st.sidebar.expander("📖 النظرية"):
    if st.button("اعرض النظرية", key="view_theory_html"):
        st.session_state.selected_page = "📖 اعرض النظرية"
        st.session_state.selected_book = None
    if st.button("اعرض النظرية بصيغة PDF", key="view_theory_pdf"):
        st.session_state.selected_page = "📖 اعرض النظرية بصيغة PDF"
        st.session_state.selected_book = None

with st.sidebar.expander("📚 الكتب الملخصة"):
    if st.button("عرض الصفحة", key="summarized_books"):
        st.session_state.selected_page = "📚 الكتب الملخصة"
        st.session_state.selected_book = None

with st.sidebar.expander("📦 الكتب المستخرج النصوص منها"):
    if st.button("عرض الصفحة", key="extracted_books"):
        st.session_state.selected_page = "📦 الكتب المستخرج النصوص منها"
        st.session_state.selected_book = None

# 🧑‍🔬 الباحثة Section
with st.sidebar.expander("🧑‍🔬 الباحثة"):
    if st.button("عرض الصفحة", key="researcher"):
        st.session_state.selected_page = "🧑‍🔬 الباحثة"
        st.session_state.selected_book = None

with st.sidebar.expander("📬 تواصل معنا"):
    if st.button("عرض الصفحة", key="contact_us"):
        st.session_state.selected_page = "📬 تواصل معنا"
        st.session_state.selected_book = None

# 📌 Main Workspace Content Based on Sidebar Selection (Fixed)

# ✅ عرض قصة المشروع
if st.session_state.selected_page == "🌸 بداية القصة والمشروع":
    st.subheader("🌸 بداية القصة والمشروع")
    story_file_path = "pages/story_3.html"
    if os.path.exists(story_file_path):
        display_html(story_file_path)  # استدعاء الدالة لعرض ملف HTML
    else:
        st.error("❌ ملف قصة المشروع غير موجود. تأكد من اسم الملف أو مساره.")

# ✅ عرض البحث بصيغة HTML
elif st.session_state.selected_page == "🔎 اعرض البحث":
    st.subheader("🔎 اعرض البحث")
    research_file_path = "pages/البحث.html"  # المسار النسبي لملف البحث
    if os.path.exists(research_file_path):
        display_html(research_file_path)  # استدعاء الدالة لعرض ملف HTML
    else:
        st.error("❌ ملف البحث غير موجود. تأكد من اسم الملف أو مساره.")

# ✅ عرض البحث بصيغة PDF
elif st.session_state.selected_page == "🔎 اعرض البحث بصيغة PDF":
    st.subheader("🔎 اعرض البحث بصيغة PDF")
    
    # رابط Google Drive للبحث
    research_pdf_link = "https://drive.google.com/file/d/1kB4uegNL4K28FxYyevCHMO4uDDRwKGY7/preview"
    
    # عرض ملف PDF باستخدام Google Drive Viewer
    st.markdown(f'<iframe src="{research_pdf_link}" width="100%" height="800px"></iframe>', unsafe_allow_html=True)
    
    # زر تحميل ملف PDF
    st.markdown(f'<a href="https://drive.google.com/uc?export=download&id=1kB4uegNL4K28FxYyevCHMO4uDDRwKGY7" download="البحث.pdf">📥 حمل ملف PDF</a>', unsafe_allow_html=True)

# ✅ عرض النظرية بصيغة HTML
elif st.session_state.selected_page == "📖 اعرض النظرية":
    st.subheader("📖 اعرض النظرية")
    theory_html_path = "pages/النظرية.html"
    if os.path.exists(theory_html_path):
        display_html(theory_html_path)  # استدعاء الدالة لعرض ملف HTML
    else:
        st.error("❌ ملف النظرية غير موجود. تأكد من اسم الملف أو مساره.")

# ✅ عرض النظرية بصيغة PDF
elif st.session_state.selected_page == "📖 اعرض النظرية بصيغة PDF":
    st.subheader("📖 اعرض النظرية بصيغة PDF")
    
    # رابط Google Drive للنظرية
    theory_pdf_link = "https://drive.google.com/file/d/1IBiMocZK6jB3UdRi6S4apRN9AqO3Sp5O/preview"
    
    # عرض ملف PDF باستخدام Google Drive Viewer
    st.markdown(f'<iframe src="{theory_pdf_link}" width="100%" height="800px"></iframe>', unsafe_allow_html=True)
    
    # زر تحميل ملف PDF
    st.markdown(f'<a href="https://drive.google.com/uc?export=download&id=1IBiMocZK6jB3UdRi6S4apRN9AqO3Sp5O" download="النظرية.pdf">📥 حمل ملف PDF</a>', unsafe_allow_html=True)

# ✅ عرض الكتب الملخصة
elif st.session_state.selected_page == "📚 الكتب الملخصة":
    show_books_list()

# ✅ عرض محتوى الكتاب
elif st.session_state.selected_page == "book_content":
    if st.session_state.selected_book:
        show_book_content(st.session_state.selected_book)
    else:
        st.error("❌ لم يتم تحديد كتاب.")

# ✅ عرض ملخص الكتاب
elif st.session_state.selected_page == "summary_content":
    if st.session_state.selected_book:
        show_summary_content(st.session_state.selected_book)
    else:
        st.error("❌ لم يتم تحديد كتاب.")

# ✅ عرض صورة عند الضغط على "الكتب المستخرج النصوص منها"
elif st.session_state.selected_page == "📦 الكتب المستخرج النصوص منها":
    st.subheader("📦 الكتب المستخرج النصوص منها")
    image_path = r"images\soon.png"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.error("❌ ملف الصورة غير موجود. تأكد من اسم الملف أو مساره.")

# ✅ عرض معلومات الباحثة
elif st.session_state.selected_page == "🧑‍🔬 الباحثة":
    st.subheader("🧑‍🔬 الباحثة")
    st.markdown("""
        <div style="text-align: right; font-family: Tahoma;">
            <h3>اسم الطالبة: رنين محمدخير العيادي</h3>
            <h3>التخصص:دكتوراة تفسير وعلوم القرآن</h3>
            <h3>الجامعة: الجامعة الأردنية</h3>
            <h3>البريد الإلكتروني: mraneen57@gmail.com</h3>
        </div>
    """, unsafe_allow_html=True)

# ✅ عرض فورم التواصل عند الضغط على "تواصل معنا"
elif st.session_state.selected_page == "📬 تواصل معنا":
    st.subheader("📬 تواصل معنا")
    st.markdown("""
        <div style="width: 100%; height: 600px; overflow: auto; border: 1px solid #ccc;">
            <iframe
              id="JotFormIFrame-250081220623038"
              title="مشروع من كل زهرة رحيق"
              onload="window.parent.scrollTo(0,0)"
              allowtransparency="true"
              allow="geolocation; microphone; camera; fullscreen"
              src="https://form.jotform.com/250081220623038"
              frameborder="0"
              style="width: 100%; height: 1000px; border: none;"
              scrolling="yes"
            >
            </iframe>
            <script src='https://cdn.jotfor.ms/s/umd/latest/for-form-embed-handler.js'></script>
            <script>window.jotformEmbedHandler("iframe[id='JotFormIFrame-250081220623038']", "https://form.jotform.com/")</script>
        </div>
    """, unsafe_allow_html=True)

# Footer Section
st.markdown(
    """
    <hr>
    <p style='text-align: center; font-family: Tahoma;'>صُنع المشروع بكل ❤️ لدعم الأبحاث في مسألة الإعجاز القرآني</p>
    """,
    unsafe_allow_html=True
)