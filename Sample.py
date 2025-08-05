import os

from lxml import etree

from langchain.vectorstores import Chroma

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.docstore.document import Document
 
# ---------- CONFIG ----------

XML_PATH = "AirshoppingRQ.xml"  # ✅ Change to your XML file

PERSIST_DIR = "chroma_xml_store"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
 
# ---------- STEP 1: LOAD XML AS STRING ----------

def load_full_xml(xml_path):

    tree = etree.parse(xml_path)

    root = tree.getroot()

    xml_str = etree.tostring(root, pretty_print=True).decode()

    print(f"✅ Loaded XML with {len(xml_str)} characters.")

    return xml_str
 
 
# ---------- STEP 2: CREATE OR LOAD VECTOR DB ----------

def create_or_load_vdb(xml_str: str, persist_dir: str):

    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
 
    if not os.path.exists(persist_dir) or not os.listdir(persist_dir):

        print("📦 Creating new Chroma vector store...")

        document = Document(page_content=xml_str)

        vectordb = Chroma.from_documents([document], embedding, persist_directory=persist_dir)

        vectordb.persist()

    else:

        print("📂 Loading existing Chroma vector store...")

        vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding)
 
    return vectordb
 
 
# ---------- STEP 3: RETRIEVE ENTIRE DOCUMENT ----------

def retrieve_full_document_as_string(vectordb):

    results = vectordb.similarity_search("retrieve entire xml document", k=1)

    if results:

        return results[0].page_content

    return None
 
 
# ---------- MAIN ----------

if __name__ == "__main__":

    # Step 1: Read full XML

    xml_string = load_full_xml(XML_PATH)
 
    # Step 2: Store into Chroma

    vectordb = create_or_load_vdb(xml_string, PERSIST_DIR)
 
    # Step 3: Retrieve entire document back

    retrieved_xml = retrieve_full_document_as_string(vectordb)
 
    if retrieved_xml:

        print("\n✅ Retrieved XML from vector store:\n")

        print(retrieved_xml[:2000])  # limit print

    else:

        print("❌ No document found in vector DB.")

 