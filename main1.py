import os
from groq import Groq
from lxml import etree
from langchain.vectorstores import Chroma

from langchain.docstore.document import Document

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.schema import HumanMessage
 
# ---------------- CONFIG ----------------

XML_FILE_PATH = "AirshoppingRQ.xml"

VECTOR_DB_DIR = "vector_store"

EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

GROQ_API_KEY = "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"  # <<< Replace with your key

GROQ_MODEL = "gemma2-9b-it"
 
# ---------------- INIT ----------------

client = Groq(api_key=GROQ_API_KEY)

embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


from lxml import etree

def chunk_xml_with_sampled_children(element, max_length=300):
    chunks = []
 
    xml_str = etree.tostring(element, pretty_print=True).decode()
    if len(xml_str.strip()) <= max_length:
        chunks.append(xml_str)
    else:
        seen_tags = set()
        for child in element:
            if child.tag not in seen_tags:
                seen_tags.add(child.tag)
                chunks.extend(chunk_xml_with_sampled_children(child, max_length=max_length))
        if not list(element):
            chunks.append(xml_str)
 
    return chunks
 
def load_xml_chunks(xml_path, max_length=600):
    tree = etree.parse(xml_path)
    root = tree.getroot()
 
    chunks = []
    for child in root:
        chunks.extend(chunk_xml_with_sampled_children(child, max_length=max_length))
 
    print(f"✅ Total {len(chunks)} XML chunks created (sampled, max {max_length} chars each).")
    return chunks
 
# ---------------- VECTOR DB ----------------

def create_vector_db(chunks, persist_dir):

    print(f"🔄 Creating vector store for {len(chunks)} XML chunks...")

    docs = [Document(page_content=chunk) for chunk in chunks]
 
    vectordb = Chroma.from_documents(

        documents=docs,

        embedding=embedding,

        persist_directory=persist_dir

    )

    vectordb.persist()

    return vectordb
 
 
def load_vector_db(persist_dir):

    return Chroma(

        persist_directory=persist_dir,

        embedding_function=embedding

    )
 
 
# ---------------- GROQ LLM CALL ----------------

def ask_llm(context, user_query):

    print("💬 Asking Groq LLM for refined answer...")

    prompt = (
        "You are an XML schema expert. Based on the following XML snippets, "
        "return the complete parent XML block that best answers the user's question.\n\n"
        f"XML Context:\n{context}\n\n"
        f"User Question: {user_query}\n\n"
        "Respond with only the full XML block (including its parent tags) that contains the relevant elements. "
        "Do not provide explanations or descriptions. Output valid XML only."
    )
 
    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[{"role": "user", "content": prompt}]

    )

    return response.choices[0].message.content
 
 
# ---------------- MAIN ----------------

if __name__ == "__main__":

    # Step 1: Chunk XML

    if not os.path.exists(VECTOR_DB_DIR) or not os.listdir(VECTOR_DB_DIR):

        chunks = load_xml_chunks(XML_FILE_PATH)

        for chunk in chunks:
            print("\n---------------------------------------------------------\n")
            print(chunk)

        vectordb = create_vector_db(chunks, VECTOR_DB_DIR)

    else:

        vectordb = load_vector_db(VECTOR_DB_DIR)
 
    while True:

        user_query = input("\nAsk a schema question (or type 'exit'): ")

        if user_query.lower() == 'exit':

            break
 
        # Step 2: Retrieve Top Matches

        results = vectordb.similarity_search(user_query, k=3)

        # print(results)
        # for i in results:
        #     print(i.page_content)

        combined_context = "\n---\n".join([res.page_content for res in results])
 
        # Step 3: LLM Answer Refinement

        answer = ask_llm(combined_context, user_query)
 
        # Step 4: Output

        print("\n📌 LLM Answer:\n", answer)

 