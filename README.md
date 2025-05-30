# Financial Document Q&A System

This Streamlit application provides a user-friendly interface to query information from SEC 10-K filings using a Neo4j knowledge graph and OpenAI's language models.

## Features

- Interactive question-answering interface
- Powered by Neo4j graph database and OpenAI's language models
- Provides answers based on multiple companies' SEC 10-K filings
- Example questions included for easy testing

## Prerequisites

- Python 3.8 or higher
- Neo4j database with the knowledge graph already set up
- OpenAI API key
- Environment variables configured

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   NEO4J_URI=your_neo4j_uri
   NEO4J_USERNAME=your_neo4j_username
   NEO4J_PASSWORD=your_neo4j_password
   NEO4J_DATABASE=your_neo4j_database
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Enter your question in the text input field
2. The system will search the knowledge graph and provide an answer based on the relevant information from the SEC filings
3. Example questions are provided to help you get started

## Example Questions

- What is Netflix's primary business?
- Where is Apple headquartered?
- What are the top risks mentioned in Johnson & Johnson's 10-K?
- Where are the primary suppliers for Tesla?
- How is ExxonMobil addressing climate change and the energy transition?

## Note

Make sure your Neo4j database is properly set up with the knowledge graph containing the SEC filing data before running the application. 