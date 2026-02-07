
from langchain.agents import agent_types, initialize_agent, create_structured_chat_agent, AgentType, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Replicate
from langchain_core.tools import tool
from langchain import hub

from dotenv import load_dotenv
import streamlit as st
import requests
import os
import json

def parse_input(input_str):
  parts = input_str.split(";")
  return dict(part.split("=") for part in parts)

@tool
def multiply(input: str):
  """
  Multiply too numbers.
  input format: 'a=123;b=123'
  """
  try:
    # parts e input.strip().split(" and")
    # a, b = int(parts[0]), int(parts[1])
    input_dict = parse_input(input)
    a = float(input_dict["a"])
    b = float(input_dict["b"])
    return str(a * b)
  except Exception as e:
    return f"Something went wrong with the tool: {e}"

@tool
def cat_fact(input):
  """
  def unique and random cat fact
  """
  try:
    response = request.get("https://catfact.ninja/fact?max_length=200")

    return str(response.json()['fact'])
  except Exception as e:
    return f"Something went wrong with the tool: {e}"

@tool
def get_weather(input: str) -> str:
  """
  Get current weather for given latitude & longitude

  User & search tool to get the city coordiantes first before using this tool to get accu

  input format: 'lat=-6.2;long=106.8'
  """

  try:
    # parts e input.strip().split(" and")
    # lat, lon = parts[0], parts[1]
    input_dict = parse_input(input)
    lat = float(input_dict["lat"])
    lon = float(input_dict["long"])
    response = request.get(f"https://api.open-meteo.com/v1/forecast?latitude=-7.8014&longitude=110.3647&hourly=temperature_2m")
    result = response.json()
    return str(result)
  except Exception as e:
    return f"Something went wrong with the tool: {e}"


def build_agent():
  ### Build Agen dulu bosku
  load_dotenv()
  # search_token = os.environ['SEARCH_TOKEN']

  llm = Replicate(model="anthropic/claude-3.5-haiku")

  system_message = """
  Kamu adalah agent yang bisa menghitung. Jawab dalam bahasa indonesia
  kamu punya kepribadian seperti Jokowi. Ngomongnya kaya orang lemes. Obrolan simpel pun tiba2 ada poin pelajrannya
  """

  memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
  )

  tools = [
    multiply,
    cat_fact,
    get_weather,
  ]

  # This is the correct conversational agent
  agent_executor = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "system_message": system_message
    },
    max_iterations=10,
    handle_parsing_errors=True,
  )

  return agent_executor
