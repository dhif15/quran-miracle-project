import streamlit as st

def display_html(file_path):
    """
    دالة لعرض ملف HTML في صندوق ثابت مع شريط تمرير.
    """
    try:
        # قراءة ملف HTML
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # إنشاء صندوق ثابت مع شريط تمرير
        html_box = f"""
        <div style="width: 100%; height: 600px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
            {html_content}
        </div>
        """

        # عرض HTML في Streamlit
        st.components.v1.html(html_box, height=600)

    except FileNotFoundError:
        st.error("ملف HTML غير موجود. يرجى التأكد من أن الملف موجود في نفس مسار العمل.")