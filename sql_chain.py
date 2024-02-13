# from langchain_community.llms import OpenAI
# from langchain_openai import OpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_experimental.sql import SQLDatabaseChain
from sql_db_factory import *
API_KEY = os.getenv('OPENAI_API_KEY')


def setup_sql_chain():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=API_KEY, streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    db_engine = sql_db_factory()
    # toolkit = SQLDatabaseToolkit(db=db_engine, llm=llm)
    sql_chain = SQLDatabaseChain.from_llm(llm, db_engine, verbose=True) 
        # return_intermediate_steps=True,  # Enable if you want to see intermediate steps
        # use_query_checker=True,  
        # verbose = True, 
        # toolkit=toolkit)
    return sql_chain

# Usage
# sql_chain = setup_sql_chain()
# sql_chain, toolkit = setup_sql_chain()
