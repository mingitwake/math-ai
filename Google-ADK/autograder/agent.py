from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor
from dotenv import load_dotenv
from . import prompt
import os

load_dotenv()

MODEL = "azure/o3-mini"

calculator_agent = Agent(
    name="calculator_agent",
    model=LiteLlm(MODEL),
    code_executor=BuiltInCodeExecutor(),
    instruction=prompt.CALCULATOR_PROMPT,
    description="Agent executes Python code to perform calculations."
)

root_agent = Agent(
    name="autograder_agent",
    model=LiteLlm(MODEL),
    description="Agent grades student-submitted math work from images and provides feedback.",
    instruction=prompt.AUTOGRADER_PROMPT,
    tools=[
        # AgentTool(agent=calculator_agent) ##  Gemini code execution tool is not supported for model azure/o3-mini
    ] 
)

# session_service = InMemorySessionService()
# session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
# runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# def call_agent(query):
#     content = types.Content(role='user', parts=[types.Part(text=query)])
#     events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

#     for event in events:
#         if event.is_final_response():
#             final_response = event.content.parts[0].text
#             print("Agent Response: ", final_response)
