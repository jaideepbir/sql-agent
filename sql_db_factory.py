from langchain.sql_database import SQLDatabase
import os
###----------------------------------------------------------------
###TEMPORARY IMPORT statement
from langchain.llms.openai import OpenAI
# from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
# from langchain import SQLDatabase
# from langchain import SQLDatabaseChain
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_experimental.sql import SQLDatabaseChain


###----------------------------------------------------------------

#from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from config import SNOWFLAKE, MYSQL, cfg

from log_init import logger

#cfg.selected_db == MYSQL

def sql_db_factory() -> SQLDatabase:
    if cfg.selected_db == SNOWFLAKE:
        snowflake_config = cfg.snow_flake_config
        schema = snowflake_config.snowflake_schema
        engine = create_engine(
            URL(
                account=snowflake_config.snowflake_account,
                user=snowflake_config.snowflake_user,
                password=snowflake_config.snowflake_password,
                database=snowflake_config.snowflake_database,
                schema=schema,
                warehouse=snowflake_config.snowflake_warehouse,
                host=snowflake_config.snowflake_host,
            )
        )
        return SQLDatabase(engine=engine, schema=schema)
    elif cfg.selected_db == MYSQL:
        return SQLDatabase.from_uri(cfg.db_uri, view_support=True)
    else:
        raise Exception(f"Could not create sql database factory: {cfg.selected_db}")


if __name__ == "__main__":
    logger.info("sql_db_factory")
    sql_database = sql_db_factory()
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # model=OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API")) #"gpt-3.5-turbo"
    QUERY = """
        Given an input question, first create a syntactically correct mysql query to run, then look at the results of the query and return the answer.
        Use the following format:

        Question: Question here
        SQLQuery: SQL Query to run
        SQLResult: Result of the SQLQuery
        Answer: Final answer here

        {question}
    """
    # db_chain = SQLDatabaseChain(llm=model, database=sql_database, verbose=True)
    # print (db_chain)
    

    logger.info("sql_database %s", sql_database)
