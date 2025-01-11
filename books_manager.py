import streamlit as st
import json
import os

def load_books():
    with open("books.json", "r", encoding="utf-8") as file:
        return json.load(file)

def show_books_list():
    st.subheader("📚 قائمة الكتب والملخصات")
    books = load_books()

    # CSS للبطاقات مع تأثيرات تفاعلية
    st.markdown("""
        <style>
            .book-card {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                text-align: center;
                background-color: #f9f9f9;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s;
                position: relative;
                overflow: hidden;
                cursor: pointer;
            }
            .book-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                background-color: #f0f0f0;
            }
            .book-title {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 15px;
                color: #333;
            }
            .book-button {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                cursor: pointer;
                margin: 5px;
                width: 100%;
                transition: background-color 0.3s;
            }
            .book-button:hover {
                background-color: #2980b9;
            }
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.7);
                transform: scale(0);
                animation: ripple-animation 0.6s linear;
                pointer-events: none;
            }
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            .book-card-0 { background-color: #f8d7da; }
            .book-card-1 { background-color: #d4edda; }
            .book-card-2 { background-color: #d1ecf1; }
            .book-card-3 { background-color: #fff3cd; }
            .book-card-4 { background-color: #f5d0c5; }
            .book-card-5 { background-color: #d6d8db; }
        </style>
    """, unsafe_allow_html=True)

    # JavaScript لإضافة تأثير التموج (Ripple Effect)
    st.markdown("""
        <script>
            function createRipple(event) {
                const button = event.currentTarget;
                const circle = document.createElement("span");
                const diameter = Math.max(button.clientWidth, button.clientHeight);
                const radius = diameter / 2;
                circle.style.width = circle.style.height = `${diameter}px`;
                circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
                circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
                circle.classList.add("ripple");
                const ripple = button.getElementsByClassName("ripple")[0];
                if (ripple) {
                    ripple.remove();
                }
                button.appendChild(circle);
            }
            document.addEventListener("click", function(event) {
                if (event.target.classList.contains("book-card")) {
                    createRipple(event);
                }
            });
        </script>
    """, unsafe_allow_html=True)

    # عرض البطاقات بتنسيق شبكي
    cols = st.columns(3)
    for idx, book in enumerate(books):
        with cols[idx % 3]:
            # تحديد لون البطاقة بناءً على الفهرس
            card_class = f"book-card book-card-{idx % 6}"  # 6 ألوان مختلفة
            with st.container():
                st.markdown(f"""
                <div class="{card_class}">
                    <p class="book-title">{book['name']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # استخدام أزرار Streamlit بدلاً من HTML buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📖 عرض الكتاب", key=f"book_{idx}"):
                        st.session_state.selected_page = "book_content"
                        st.session_state.selected_book = book['name']
                        st.rerun()
                with col2:
                    if st.button("📄 عرض الملخص", key=f"summary_{idx}"):
                        st.session_state.selected_page = "summary_content"
                        st.session_state.selected_book = book['name']
                        st.rerun()

def display_file(file_path, file_type):
    """عرض الملف بغض النظر عن نوع الامتداد الفعلي"""
    if file_path.startswith("http"):  # إذا كان الرابط من Google Drive
        if "drive.google.com" in file_path:
            st.markdown(f'<iframe src="{file_path}" width="100%" height="800px"></iframe>', unsafe_allow_html=True)
        else:
            st.error("❌ الرابط غير مدعوم. يرجى استخدام رابط Google Drive.")
    elif os.path.exists(file_path):  # إذا كان الملف محليًا
        # التحقق من الامتداد الفعلي للملف
        actual_extension = os.path.splitext(file_path)[1].lower()
        
        # إذا كان الملف html، نعرضه كـ html
        if actual_extension == '.html' or actual_extension == '.htm':
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                display_html = f"""
                <div style="width: 100%; height: 800px; overflow: auto; border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #fff;">
                    {html_content}
                </div>
                """
                st.components.v1.html(display_html, height=800, scrolling=True)
    else:
        st.error(f"❌ الملف غير موجود: {file_path}")

def show_book_content(book_name):
    books = load_books()
    book = next((b for b in books if b['name'] == book_name), None)
    
    if book:
        st.subheader(f"📖 {book['name']}")
        
        # التعامل مع الكتب المتعددة
        if isinstance(book['book_file'], list):
            for idx, file in enumerate(book['book_file']):
                st.subheader(f"📖 الجزء {idx + 1}")
                # استخدام file_type للجزء المحدد إذا كان متاحاً، وإلا استخدام الامتداد الفعلي
                current_type = book['file_type'][idx] if isinstance(book['file_type'], list) else book['file_type']
                display_file(file, current_type)
        else:
            display_file(book['book_file'], book['file_type'])
        
        if st.button("رجوع إلى قائمة الكتب"):
            st.session_state.selected_page = "📚 الكتب الملخصة"
            st.session_state.selected_book = None
            st.rerun()

def show_summary_content(book_name):
    books = load_books()
    book = next((b for b in books if b['name'] == book_name), None)
    
    if book:
        st.subheader(f"📄 ملخص {book['name']}")
        
        # التعامل مع الملخصات المتعددة
        if isinstance(book['summary_file'], list):
            for idx, file in enumerate(book['summary_file']):
                st.subheader(f"📄 ملخص الجزء {idx + 1}")
                # استخدام file_type للجزء المحدد إذا كان متاحاً، وإلا استخدام الامتداد الفعلي
                current_type = book['file_type'][idx] if isinstance(book['file_type'], list) else book['file_type']
                display_file(file, current_type)
        else:
            display_file(book['summary_file'], book['file_type'])
        
        if st.button("رجوع إلى قائمة الكتب"):
            st.session_state.selected_page = "📚 الكتب الملخصة"
            st.session_state.selected_book = None
            st.rerun()