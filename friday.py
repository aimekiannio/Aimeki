import os
import streamlit as st
from pypdf import PdfReader
import chromadb
from google import genai
from google.genai import types

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(page_title="aimeki - MBOSE AI Mentor", layout="wide")

# ----------------------------------------------------
# Pure Chrome / Pitch Black Y2K CSS Injection
# ----------------------------------------------------
st.markdown("""
    <style>
    /* Pitch Black Base Background */
    .stApp {
        background-color: #000000 !important;
        color: #e0e0e0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Metallic Chrome Title */
    h1 {
        background: linear-gradient(180deg, #ffffff 0%, #d8d8d8 35%, #707070 50%, #ffffff 85%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: 3px;
        border-bottom: 1px solid #333333;
        padding-bottom: 12px;
    }

    /* Pitch Black Sidebar with Sharp Chrome Border */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #444444 !important;
    }

    /* Liquid Chrome Metallic Buttons */
    .stButton > button {
        background: linear-gradient(180deg, #ffffff 0%, #b0b0b0 45%, #4a4a4a 50%, #262626 85%, #888888 100%);
        color: #000000 !important;
        font-weight: 800;
        border: 1px solid #ffffff !important;
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        transition: all 0.15s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(180deg, #ffffff 0%, #d5d5d5 45%, #666666 50%, #3a3a3a 85%, #aaaaaa 100%);
        box-shadow: 0 0 18px rgba(255, 255, 255, 0.6);
        transform: scale(1.01);
    }

    /* High-Contrast Inputs */
    input, textarea, div[data-baseweb="select"] {
        background-color: #080808 !important;
        color: #ffffff !important;
        border: 1px solid #555555 !important;
        border-radius: 2px !important;
    }
    
    input:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 8px rgba(255, 255, 255, 0.4) !important;
    }

    /* Liquid Chrome Edge Chat Cards */
    .stChatMessage {
        background: #050505 !important;
        border: 1px solid #333333 !important;
        border-left: 3px solid #ffffff !important;
        border-radius: 2px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
    }

    /* Selectbox Dropdown Options */
    div[data-baseweb="popover"] {
        background-color: #050505 !important;
        border: 1px solid #555555 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ aimeki: MBOSE Class 11 & 12 Academic Mentor")

# ----------------------------------------------------
# Sidebar Security Setup
# ----------------------------------------------------
APP_PASSCODE = "aimekithegoat"

# Fetch API key directly from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

st.sidebar.header("🔐 Access Control")
user_passcode = st.sidebar.text_input("Enter App Passcode:", type="password")

if user_passcode != APP_PASSCODE:
    st.warning("🔒 Access Locked: Please enter the correct App Passcode in the sidebar to proceed.")
elif not api_key:
    st.error("⚠️ API Key missing! Add GEMINI_API_KEY to your Streamlit App Secrets.")
else:
    client = genai.Client(api_key=api_key)

    chroma_client = chromadb.PersistentClient(path="./mbose_scratch_db")
    collection = chroma_client.get_or_create_collection(name="mbose_materials")

    # ----------------------------------------------------
    # Sidebar Controls & MBOSE Configuration
    # ----------------------------------------------------
    st.sidebar.header("🎯 Exam Answer Format")
    mark_scheme = st.sidebar.selectbox(
        "Select Answer Weightage:",
        [
            "2-Mark Question (Concise & Direct)", 
            "3-Mark Question (Structured Points)", 
            "5-Mark Question (Detailed with Steps/Diagram Refs)"
        ]
    )

    st.sidebar.header("📂 Material Upload")
    uploaded_file = st.sidebar.file_uploader("Upload Class 11/12 PDF", type=["pdf"])

    # ----------------------------------------------------
    # Helper Functions
    # ----------------------------------------------------
    def extract_text_from_pdf(pdf_file):
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    def chunk_text(text, chunk_size=1000, overlap=150):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    def get_embedding(text):
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embedding.values

    # ----------------------------------------------------
    # Document Upload & Vectorization
    # ----------------------------------------------------
    if uploaded_file and st.sidebar.button("Process & Store Material"):
        with st.spinner("Friday is processing your PDF material..."):
            raw_text = extract_text_from_pdf(uploaded_file)
            text_chunks = chunk_text(raw_text)
            
            documents_to_add = []
            embeddings_to_add = []
            ids_to_add = []

            for index, chunk in enumerate(text_chunks):
                doc_id = f"{uploaded_file.name}_chunk_{index}"
                vector = get_embedding(chunk)
                
                documents_to_add.append(chunk)
                embeddings_to_add.append(vector)
                ids_to_add.append(doc_id)

            if documents_to_add:
                collection.add(
                    documents=documents_to_add,
                    embeddings=embeddings_to_add,
                    ids=ids_to_add
                )
                st.sidebar.success(f"Friday stored {len(text_chunks)} chunks from {uploaded_file.name}!")

    if st.sidebar.button("Clear Vector Database"):
        chroma_client.delete_collection(name="mbose_materials")
        collection = chroma_client.get_or_create_collection(name="mbose_materials")
        st.sidebar.warning("Vector database cleared.")

    # ----------------------------------------------------
    # Chat & Academic Retrieval Interface
    # ----------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_query := st.chat_input("Ask Friday a question based on your uploaded MBOSE material..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            query_vector = get_embedding(user_query)

            results = collection.query(
                query_embeddings=[query_vector],
                n_results=4
            )
            
            retrieved_chunks = results["documents"][0] if results["documents"] else []
            context = "\n\n---\n\n".join(retrieved_chunks)

            full_prompt = f"""You are Friday, an academic AI mentor dedicated strictly to Class 11 and 12 MBOSE (Meghalaya Board) and NCERT courses.
Your goal is to help the student master board exam questions according to the official marking scheme.

Format requested by student: {mark_scheme}

Instructions:
1. Answer the question using ONLY the provided retrieved context below.
2. Adapt the detail level based on the selected mark scheme:
   - 2-Mark: Precise 2-3 sentence definition or direct solution with key terms highlighted.
   - 3-Mark: 3 distinct numbered/bulleted key points or short step-by-step derivation.
   - 5-Mark: Comprehensive board answer with introduction, bulleted points, formula/derivation steps, and summary.
3. If the answer cannot be found in the context, state clearly that the uploaded documents do not contain this information.

Context:
{context}

Question:
{user_query}
"""

            def stream_response():
                response = client.models.generate_content_stream(
                    model="gemini-3.6-flash",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text

            full_response = st.write_stream(stream_response())
            st.session_state.messages.append({"role": "assistant", "content": full_response})