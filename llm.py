from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
import ollama
import logging
from langchain.chains import ConversationChain, RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    UnstructuredExcelLoader,
    UnstructuredImageLoader,
    UnstructuredPowerPointLoader,
)
from langchain_core.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from prompts import document_template, template


PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
llm = ChatOllama(model="llama3")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True, prompt=PROMPT)


# PDF RAG
def pdf_loader(file):
    try:
        return PyPDFLoader(file).load_and_split()
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)


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


def ollama_llm(chunks):
    try:
        template = "Context: {context}\nQuestion: {question}\nAnswer:"
        parser = StrOutputParser()
        chain = llm | parser
        PROMPT = PromptTemplate(
            input_variables=["context", "question"], template=template
        )
        chain_type_kwargs = {"prompt": PROMPT}

        qa = RetrievalQA.from_chain_type(
            llm=chain,
            chain_type="stuff",
            retriever=chunks.as_retriever(search_kwargs={"k": 1}),
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
        )

        return qa

    except Exception as e:
        logging.error("An error occurred in ollama_llm function: %s", e, exc_info=True)
        return None


def pdf_chat(is_file, question):
    file = pdf_loader(is_file)
    chunks = chunks_embeddings(file)
    qa = ollama_llm(chunks=chunks)
    query = qa({"query": question})["result"]
    return query


def handle_chat(file, question):
    if file:

        return pdf_chat(file, question)
    else:

        return conversation.predict(input=question)