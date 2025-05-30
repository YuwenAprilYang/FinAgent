import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQAWithSourcesChain
import textwrap

# Load environment variables
load_dotenv()

# Neo4j configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE") 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Constants
VECTOR_INDEX_NAME = 'form_10k_chunks'
VECTOR_NODE_LABEL = 'TextChunk'
VECTOR_SOURCE_PROPERTY = 'text'
VECTOR_EMBEDDING_PROPERTY = 'textEmbedding'

# Initialize the vector store
@st.cache_resource
def initialize_vector_store():
    vector_store = Neo4jVector.from_existing_graph(
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        index_name=VECTOR_INDEX_NAME,
        node_label=VECTOR_NODE_LABEL,
        text_node_properties=[VECTOR_SOURCE_PROPERTY],
        embedding_node_property=VECTOR_EMBEDDING_PROPERTY,
    )
    return vector_store

# Initialize the QA chain
@st.cache_resource
def initialize_qa_chain(_vector_store):
    retriever = _vector_store.as_retriever()
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
        chain_type="stuff",
        retriever=retriever
    )
    return qa_chain

# Function to get answer from the QA chain
def get_answer(question):
    response = qa_chain({"question": question}, return_only_outputs=True)
    return response["answer"]

# Set up the Streamlit interface
st.set_page_config(
    page_title="Financial Document Q&A System",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Document Q&A System")
st.markdown("""
This application allows you to ask questions about companies based on their SEC 10-K filings.
The system uses a knowledge graph built from multiple companies' filings to provide accurate and contextual answers.
""")

# Initialize the vector store and QA chain
try:
    vector_store = initialize_vector_store()
    qa_chain = initialize_qa_chain(vector_store)
except Exception as e:
    st.error(f"Error initializing the system: {str(e)}")
    st.stop()

# Create a text input for the question
question = st.text_input("Enter your question about any company:", 
                        placeholder="e.g., What is Apple's business model? or What risks are mentioned by Tesla?")

# Add some example questions
st.markdown("""
### Example Questions:
- What is Netflix's primary business?
- Where is Apple headquartered?
- What are the top risks mentioned in Johnson & Johnson's 10-K?
- Where are the primary suppliers for Tesla?
- How is ExxonMobil addressing climate change and the energy transition?
""")

# Process the question when submitted
if question:
    with st.spinner("Searching for relevant information..."):
        try:
            answer = get_answer(question)
            st.markdown("### Answer:")
            st.write(textwrap.fill(answer, width=80))
        except Exception as e:
            st.error(f"Error getting answer: {str(e)}")

# Add a footer
st.markdown("---")
st.markdown("Built with Streamlit, Neo4j, and OpenAI") 