from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    UnstructuredExcelLoader,
    UnstructuredImageLoader,
    UnstructuredPowerPointLoader,
)
import logging


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
