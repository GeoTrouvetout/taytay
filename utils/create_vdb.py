import chromadb
from langchain_community.document_loaders import PyPDFLoader
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("Taylor_Swift.pdf")
pages = [doc.page_content for doc in loader.load()]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

documents = text_splitter.create_documents(pages)


# from langchain_openai import OpenAIEmbeddings
# embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
from langchain_chroma import Chroma

client = chromadb.PersistentClient(path="./chroma-data")

vectorstore = Chroma(
    collection_name="taylor_swift_wiki",
    client=client,
    embedding_function=embedding_model,
)

vectorstore.add_documents(documents=documents)


retriever = vectorstore.as_retriever()

# res = retriever.invoke("quelle est la date de naissance de Taylor Swift?")
