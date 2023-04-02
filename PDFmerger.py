import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

st.set_page_config(page_title="Akash's PDF Merger", page_icon=":page_facing_up:", layout="wide") 

st.title("Akash's PDF Merger :page_facing_up:")
st.write("---")

# Screen 1 - Number of files user wants to merge
with st.container():
    st.write('##')
    left_column, right_column = st.columns((1,3))
    with left_column:
        num_files = st.selectbox("Select the number of PDF files to merge", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=1)
    with right_column:
        st.empty()

# Screen 2 - Upload files
with st.container():
    st.write('##')
    left_column, right_column = st.columns((1,1))
    with left_column:
        file_list = []
        for i in range(num_files):
            file = st.file_uploader(f"Upload File {i+1}", type=["pdf"])
            if file:
                file_list.append(file)

# Screen 3 - Show uploaded files
        if file_list:
            st.write('##')
            st.write("Files being merged:")
            for i, file in enumerate(file_list):
                st.write(f"{i+1}. {file.name}")
    with right_column:
        st.empty()

    # Merge PDFs
    st.write("---")
    st.write('##')
    if st.button("Merge PDFs"):
        # Initialize merger
        merger = PdfWriter()

        # Add uploaded files to merger
        for file in file_list:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                merger.add_page(page)

        # Show loading animation
        with st.spinner("Merging PDFs..."):
            # Merge files
            merged_pdf = BytesIO()
            merger.write(merged_pdf)

        # Show success message
        st.write("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("PDF Merge Successful!")
        with col2:
            st.empty()
        with col3:
            st.empty()

        # Download merged PDF
        st.write('##')
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf.getvalue(),
            file_name=f"Merged {num_files} PDF files.pdf",
        )

        # Back button
        st.write('##')
        if st.button("Back"):
            file_list.clear()
            st.experimental_rerun()
