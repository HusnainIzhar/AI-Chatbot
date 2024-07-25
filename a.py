from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    UnstructuredExcelLoader,
    UnstructuredImageLoader,
    UnstructuredPowerPointLoader,
)
import logging
import ollama




def pdf_loader(file):
    try:
        return PyPDFLoader(file).load_and_split()
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


def ppt_loader(file):
    try:
        return UnstructuredPowerPointLoader(file).load_and_split()
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


def excel_loader(file):
    try:
        return UnstructuredExcelLoader(file).load_and_split()
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


def img_loader(file):
    try:
        return UnstructuredImageLoader(file).load()
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


def url_loader(url):
    try:
        return WebBaseLoader(url).load_and_split()
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import ollama
import logging

def chunks_embeddings(data):
    try:
        print(data)
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        ).split_documents(data)
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        logging.error("An error occured in chunk_embedding fn: %s", e, exc_info=True)


def ollama_llm(question, context):
    try:
        formatted_prompt = f"Question: {question}\n\nContext: {context}"
        response = ollama.chat(
            model="llama3", messages=[{"role": "user", "content": formatted_prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        logging.error("An error occured in chunk_embedding fn: %s", e, exc_info=True)


# rag chain


def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def rag_chain(question, retriever):
    retrieved_docs = retriever.invoke(question)
    formatted_context = combine_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)
