import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd

# If using Windows, set tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("📘 EduTrack AI – Institutional Document Analyzer")
st.write("Upload institutional documents to check completeness and calculate performance score.")

# Required documents
required_docs = [
    "Affiliation Certificate",
    "Faculty List",
    "Infrastructure Report",
    "Accreditation Certificate",
    "Fee Structure",
    "Student Enrollment Data"
]

# Upload files
uploaded_files = st.file_uploader("Upload Documents", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    extracted_docs = []
    count_present = 0

    st.subheader("📄 Extracted Text from Documents")
    for file in uploaded_files:
        st.write(f"**Document:** {file.name}")
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        st.text_area("Extracted Text", text, height=150)
        extracted_docs.append(text)

        # Check required documents
        for req in required_docs:
            if req.lower() in text.lower():
                count_present += 1

    # Document sufficiency
    sufficiency = (count_present / len(required_docs)) * 100
    st.subheader("📊 Document Sufficiency")
    st.metric("Sufficiency Score", f"{sufficiency:.2f}%")

    # Simple performance score
    performance_score = min(100, sufficiency + 10)
    st.subheader("📈 Institution Performance Indicator (IPI)")
    st.metric("IPI Score", f"{performance_score:.2f}")

    # Required documents table
    st.subheader("📋 Document Checklist")
    df = pd.DataFrame({
        "Document": required_docs,
        "Status": ["Present" if req.lower() in " ".join(extracted_docs).lower() else "Missing" for req in required_docs]
    })
    st.table(df)
