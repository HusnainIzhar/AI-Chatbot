from langchain_community.document_loaders import WebBaseLoader
import bs4

def url_loader(url):
    load = WebBaseLoader(web_paths = (url), bs_kwargs=dict(parse_only = bs4.SoupStrainer(class_ = ("post-content",'post-title','post-header'))))
    return load.load_and_split()

    a = url_loader("https:emarkrealty.com")
    print(a)