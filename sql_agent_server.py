from langchain.agents import create_openai_tools_agent
from sql_chain   import setup_sql_chain


class SQLDatabaseAgent:
    def __init__(self, max_iterations=3, enable_tracing=True):
        self.sql_chain = setup_sql_chain()
        self.max_iterations = max_iterations
        self.enable_tracing = enable_tracing


    def process_query(self, query):
        return self.sql_chain.invoke({"query":query})
        # return self.sql_chain.invoke({"query": query})

# Usage
# agent = SQLDatabaseAgent()
# agent_executor = create_sql_agent(llm=llm, toolkit=agent, verbose=True)
# response = agent.process_query("SELECT COUNT(*) FROM messages;")