import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from handlers import rag_chain,chunk_embeddings_handler, pdf_loader

def main():
    file = pdf_loader("fizza.pdf")
    chunks = chunk_embeddings_handler(file)
    retriever = chunks.as_retriever()
    result = rag_chain("what is this pdf about", retriver=retriever)
    return result

main()