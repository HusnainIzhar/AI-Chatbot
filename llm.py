from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import logging
from langchain.chains import ConversationChain, RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import (
    PyPDFLoader,
)
from langchain_core.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from prompts import  template
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

#llm init
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
llm = ChatGroq(
    temperature=0,
    groq_api_key="",
    model_name="llama3-groq-8b-8192-tool-use-preview"
)
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
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        ).split_documents(data)
        
        if not chunks:
            logging.error("No chunks created from the data.")
            return None
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        logging.error("An error occurred in chunk_embedding function: %s", e, exc_info=True)
        return None

def llm_init(chunks):
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
        print('qa is ',qa)
        return qa

    except Exception as e:
        logging.error("An error occurred in ollama_llm function: %s", e, exc_info=True)
        return None


def pdf_chat(is_file, question):
    file = pdf_loader(is_file)
    chunks = chunks_embeddings(file)
    qa = llm_init(chunks=chunks)
    query = qa({"query": question})["result"]
    return query


def handle_chat(file, question):
    if file:
        return pdf_chat(file, question)
    else:
        return conversation.predict(input=question)
