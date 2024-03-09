import streamlit as st
from dotenv import dotenv_values
from sqlalchemy import create_engine
from langchain.openai import AzureOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_experimental.sql_database import SQLDatabase

# Load configuration from .env file
config = dotenv_values(".env")

# Initialize Azure OpenAI Client
llm = AzureOpenAI(
  model=config["AZURE_OPENAI_DEPLOYMENT"],
  deployment_name=config["AZURE_OPENAI_DEPLOYMENT"],
  api_key=config["AZURE_OPENAI_API_KEY"],
  api_version=config["AZURE_OPENAI_API_VERSION"],
  azure_endpoint=config["AZURE_OPENAI_ENDPOINT"],
  temperature=0
)

# Set Up Database Connection
engine = create_engine(config["SQL_CONNECTION_STRING"])
database = SQLDatabase(engine, schema="dbo")

# Initialize SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm, database, verbose=True, use_query_checker=True)

# Streamlit User Interface
st.title('SQL Query via Natural Language')
query = st.text_input('Enter your natural language query:', '')

if st.button('Execute'):
    if query:
        try:
            result = db_chain.run(query)
            st.write('Result:', result)
        except Exception as e:
            st.write('Error:', str(e))
    else:
        st.write("Please enter a query.")
