import os

from lxml import etree

from langchain.vectorstores import Chroma

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.docstore.document import Document
 
# -------- CONFIG --------

XML_FOLDER = "xml files"            # Folder containing your XML files

PERSIST_DIR = "chroma_full_xml_db" # Folder to persist Chroma DB

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
 
# -------- LOAD ALL XML FILES AS DOCUMENTS --------

def load_all_xml_documents(folder_path):

    documents = []

    for file_name in os.listdir(folder_path):

        if file_name.endswith(".xml"):

            file_path = os.path.join(folder_path, file_name)

            try:

                tree = etree.parse(file_path)

                root = tree.getroot()

                xml_str = etree.tostring(root, pretty_print=True).decode()

                documents.append(Document(

                    page_content=xml_str,

                    metadata={"file_name": file_name}

                ))

                print(f"✅ Loaded: {file_name}")

            except Exception as e:

                print(f"❌ Failed to load {file_name}: {e}")

    return documents
 
# -------- CREATE OR LOAD VECTOR STORE --------

def create_or_load_vdb(documents, persist_dir):

    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
 
    if not os.path.exists(persist_dir) or not os.listdir(persist_dir):

        print("📦 Creating new Chroma DB with embedded XML files...")

        vectordb = Chroma.from_documents(documents, embedding, persist_directory=persist_dir)

        vectordb.persist()

    else:

        print("📂 Loading existing Chroma DB...")

        vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding)
 
    return vectordb
 
# -------- SEARCH AND RETURN TOP MATCH --------

def search_top_match(vectordb, user_story, acceptance_criteria):

    query = f"{user_story}\n{acceptance_criteria}"

    results = vectordb.similarity_search(query, k=1)  # only top 1

    return results
 
# -------- MAIN --------

if __name__ == "__main__":

    # 1. Load XML files

    docs = load_all_xml_documents(XML_FOLDER)
 
    # 2. Embed or load vector DB

    vectordb = create_or_load_vdb(docs, PERSIST_DIR)
 
    # 3. Provide your user story + acceptance criteria here:

    user_story = "As a travel search engine, I want to build an AirShopping request to fetch flight options for given origin and destination airports and travel dates."
    acceptance_criteria = "The request must contain OriginDepCriteria and DestArrivalCriteria.The PaxList must include multiple passenger types like ADT, CHD."
 
    # 4. Search for top matching XML file

    results = search_top_match(vectordb, user_story, acceptance_criteria)
 
    # 5. Print the matched XML file only

    if results:

        doc = results[0]

        print(f"\n📄 Most Relevant XML File: {doc.metadata['file_name']}\n")

        print(doc.page_content)

    else:

        print("❌ No relevant XML file found for the given user story and acceptance criteria.")

 