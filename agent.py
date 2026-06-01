import os
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

TOOLBOX_URL = os.getenv("TOOLBOX_URL", "https://travel-toolbox-5mzydhd2wa-uc.a.run.app")
toolbox = ToolboxSyncClient(TOOLBOX_URL)
tools = toolbox.load_toolset('my_first_toolset')

root_agent = Agent(
    name="hotel_agent",
    model="gemini-2.5-flash",
    description="Agent to answer questions about hotels in a city or hotels by name.",
    instruction="You are a helpful agent who can answer user questions about hotels in a specific city or hotels by name. Use the tools to answer the question.",
    tools=tools,
)
