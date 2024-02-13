import chainlit as cl
from typing import Dict, Optional
from sql_agent_server import SQLDatabaseAgent
from langchain.agents.agent_types import AgentType
# from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI
import pandas as pd
from dotenv import load_dotenv
from dotenv import dotenv_values
import os
import plotly.graph_objects as go


if os.path.exists(".env"):
    load_dotenv(override = True)
    config = dotenv_values(".env")

# agent = SQLDatabaseAgent(enable_tracing=True)
# file_path = "../uk_data_csv/2018-19-4.csv"

# df = pd.read_csv(file_path)
# print (df)



agent = SQLDatabaseAgent(max_iterations=3, enable_tracing=True)
# csv_agent = create_csv_agent(
#     ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
#     file_path,
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS
#     # return_intermediate_results=True
# )
# callback = cl.LangchainCallbackHandler(stream_final_answer=True)
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.step
async def tool():
    # Simulate a running task
    await cl.sleep(2)

    return "Response from the tool!"

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_user: cl.User,
) -> Optional[cl.User]:
  return default_user

@cl.on_chat_start
async def start():
    # image = cl.Image(path="logo_light.png", name="SQL-Chat", display="inline")
    # await cl.Message(
    #     content="This message has an image!",
    #     elements=[image],
    # ).send()
    fig = go.Figure(
        data=[go.Bar(y=[2, 1, 3])],
        layout_title_text="An example figure",
    )
    elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

    await cl.Message(content="This message has a chart", elements=elements).send()


    cl.user_session.set("SQLAgent", agent)
    # cl.user_session.set("CSVAgent", csv_agent)


@cl.on_message
async def main(message):
    SQLAgent = cl.user_session.get("SQLAgent")

    if not cl.user_session.get("CSVAgent"):
        files = [file for file in message.elements if "text/csv" in file.mime]
        print ("Uploaded files: ", files)
        if len(files) > 0:
            for file in files:
                if "text/csv" in file.mime:
                    df = pd.read_csv(file.path)
                    csv_agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
                    csv_result = csv_agent.run( message.content)
                    cl.user_session.set("CSVAgent", csv_agent)
                    await cl.Message(csv_result).send()


    elif cl.user_session.get("CSVAgent"):
        csv_agent = cl.user_session.get("CSVAgent")
        csv_result = csv_agent.run( message.content)
        await cl.Message(csv_result).send()
        
    # if csv_result:
        
    
    if any(word in message.content for word in ["database", "table", "schema"]):
        SQLresult = SQLAgent.process_query(message.content)#, callbacks=[cl.LangchainCallbackHandler()])
        await cl.Message(SQLresult['result']).send()
        
    if "show" and "table" in message.content:
        fig = await show_table()
        display_table=[cl.Plotly(name="chart", figure=fig, display="inline")]
        await cl.Message(content="This message has a chart", elements=display_table).send()



@cl.step
async def show_table():
    fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                    cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                        ])
    # fig.show()
    # elements = 
    return fig


    # SQLresult = SQLAgent.process_query(message.content)#, callbacks=[cl.LangchainCallbackHandler()])
    # await cl.Message(SQLresult['result']).send()

    # response_message = agent.process_query(message.content) 
    # await cl.Message(response_message).send()


# Run your Chainlit app
if __name__ == "__main__":
    cl.run()