from pypdf import PdfReader
from langchain_community.embeddings import SentenceTransformerEmbeddings
#from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from utils import clean_text, paraphrase_text, is_relevant

# Import the override script
import override_sqlite

# Now you can import other modules that use sqlite3
import sqlite3

# Your code here
conn = sqlite3.connect('db1.db')
print("SQLite version:", sqlite3.sqlite_version)


# Ensure your API key is correct
api_key = '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'

# Headers for Hugging Face API
headers = {"Authorization": f"Bearer {api_key}"}
# Load the PDF document
pdf_path = "data/Course_exercices - SABSQ3-Big Data Engineer 2021-BigSQL.pdf"

pdf_document = PdfReader(pdf_path)
#pdf_document = fitz.open(pdf_path)
#print(pdf_document)   #Debugging Statement


# Extract text from each page and store in a list with metadata
documents = []
for page_num in range(len(pdf_document.pages)):
    page = pdf_document.pages[page_num]
    page_text = page.extract_text()
    page_text = clean_text(page_text)  # Clean the extracted text
    documents.append(Document(page_content=page_text, metadata={"source": pdf_path, "page": page_num + 1}))

# Split each document into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#text_splitter = SentenceSplitter(language='en')
docs = text_splitter.split_documents(documents)


embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#print("Shape", embedding_function.shape)  #Debugging statement


# Load it into Chroma
db1 = Chroma.from_documents(docs, embedding_function)



# Query example test
# List of queries to process
queries = [
    "What is Db2 Big SQL?",
    "What is Data poisoning?",
    "Why Hadoop?"
]

# Process each query
for query in queries:
    results = db1.similarity_search(query)

    # Extract and process all results
    if results:
        for result in results:
            extracted_paragraph = result.page_content
            source = result.metadata.get("source")
            page = result.metadata.get("page")

            if is_relevant(query, extracted_paragraph, headers):
                # Summarize the extracted paragraph
                summarized = paraphrase_text(extracted_paragraph)

                print("-"*100)
                print("Submitted Question: ", query)
                print("-"*100)
                print(f"Answer: {summarized}\n")
                print("-"*100)
                print(f"Extracted Paragraph: {extracted_paragraph}\n")
                print("-"*100)
                print(f"Source: {source}\n")
                print(f"Page: {page}\n")
                print("-"*100)
                break  # Stop after the first relevant result
            else:
                print("-"*100)
                print(f"Submitted Question: , {query}")
                print("-"*100)
                print(f"Answer not found for question: {query}")
                break  # Stop after the first non-relevant result
    else:
        print(f"No results found for question: {query}")