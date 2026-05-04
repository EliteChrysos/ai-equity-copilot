import os
import tempfile

from functools import lru_cache
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai import get_ai_analysis


# this function reads the file from sreamlit
def load_uploaded_documents(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        try:
            if file_extension == ".pdf":
                loader = PyPDFLoader(temp_file_path)
                loaded_docs = loader.load()

            elif file_extension in [".txt", ".md"]:
                loader = TextLoader(temp_file_path, encoding="utf-8")
                loaded_docs = loader.load()

            else:
                continue

            for doc in loaded_docs:
                # this stores the file name
                doc.metadata["source"] = uploaded_file.name

                if "page" in doc.metadata:
                    # this stores file page number
                    doc.metadata["page"] = int(doc.metadata["page"]) + 1

            documents.extend(loaded_docs)

        finally:
            os.remove(temp_file_path)

    return documents


def split_documents(documents):
    # Annual reports are too long to send to claude all at once
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)
    return chunks

@lru_cache(maxsize=1)
def get_embeddings():
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )


def build_vector_store(uploaded_files):
    documents = load_uploaded_documents(uploaded_files)

    if not documents:
        return None, 0

    chunks = split_documents(documents)

    # embeddings converts the text to numbers that represent meaning
    embeddings = get_embeddings()

    # FAISS - search engine , when user asks question, it finds most relevant chunk
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store, len(chunks)


def format_retrieved_docs(docs):
    context_parts = []
    sources = []

    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Uploaded document")
        page = doc.metadata.get("page", "N/A")

        context_parts.append(
            f"""
[Source {index}: {source}, page {page}]
{doc.page_content}
"""
        )

        sources.append({
            "Source": source,
            "Page": page,
            "Preview": doc.page_content[:400]
        })

    context = "\n\n".join(context_parts)

    return context, sources


# this retrieves chunk, build prompt, and asks claude to ans using only these chunks
def answer_question_with_rag(question, vector_store, k=5):
    retrieved_docs = vector_store.similarity_search(question, k=k)

    context, sources = format_retrieved_docs(retrieved_docs)

    prompt = f"""
You are an equity research assistant.

Answer the user's question using only the retrieved document context below.

Rules:
- Use only the provided context.
- Do not invent facts.
- If the answer is not found in the context, say: "The uploaded documents do not provide enough information to answer this."
- Cite sources using this format: [filename, page number].
- Be clear and concise.

User Question:
{question}

Retrieved Context:
{context}

Final Answer:
"""

    answer = get_ai_analysis(prompt)

    return answer, sources