from langchain_ollama import OllamaEmbeddings #Take text and convert to vector
from langchain_chroma import Chroma #Vector Store
from langchain_core.documents import Document #gonna create documents and pass these to our chroma database
import os
import pandas as pd #library to easily read csv files

CSV_PATH = os.environ.get("REVIEWS_CSV", "data/sample_reviews.csv")
df = pd.read_csv(CSV_PATH)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db" #folder to store database
add_documents = not os.path.exists(db_location) #checks to see if database exists and if it does then itll process to go to csv file and vectorise

if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
            id=str(i)
        ) #page_content is what we will be vectorising and looking up & metadata is just additional information along with the doc but we wont be quering
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="store_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)