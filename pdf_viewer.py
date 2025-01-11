import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import base64

def display_pdf(file_path):
    """
    دالة لعرض ملف PDF في صندوق ثابت مع شريط تمرير.
    """
    try:
        # قراءة ملف PDF
        pdf_document = fitz.open(file_path)
        
        # عرض عدد الصفحات
        num_pages = pdf_document.page_count
        st.sidebar.write(f"عدد الصفحات: {num_pages}")

        # إنشاء HTML لعرض الصور في صندوق ثابت مع شريط تمرير
        html_content = """
        <div style="width: 100%; height: 600px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
        """

        for page_num in range(num_pages):
            # تحميل الصفحة الحالية
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(dpi=200)  # يمكنك تغيير الدقة هنا
            
            # تحويل الصفحة إلى صورة
            img = Image.open(io.BytesIO(pix.tobytes()))
            
            # تحويل الصورة إلى base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # إضافة الصورة إلى HTML
            html_content += f'<img src="data:image/png;base64,{img_base64}" style="width: 100%; margin-bottom: 20px;" alt="الصفحة {page_num + 1}">'

        # إغلاق div
        html_content += "</div>"

        # عرض HTML في Streamlit
        st.components.v1.html(html_content, height=600)

    except FileNotFoundError:
        st.error("ملف PDF غير موجود. يرجى التأكد من أن الملف موجود في نفس مسار العمل.")