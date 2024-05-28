import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langsmith import traceable
from langchain_community.tools.shell.tool import ShellTool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
import subprocess
from typing import Optional
from collections import deque
from dotenv import load_dotenv
load_dotenv()

ROOT_DIR = "./"
VALID_FILE_TYPES = {"py", "txt", "md", "ipynb"}
memory = deque(maxlen=10) 


# TODO: need to experiment with fine tuning the model with sample queries for better results

@tool
def get_fulfillment_db_schema() -> str:
    """Use this function in order to write better fulfillment SQL in the reports. The fullfilment database
    is used to get data about the status of orders that are picked and packed for all customers and acrross all stores"""
     
    file1 = open("./fulfillment.sql", "r") 
    return file1.read()

@tool 
def get_subscription_db_schema() -> str:
    """Use this function in order to write better User, Subsciption, and Orders related  SQL in the reports. The subscription database
    is used to get data about users, their subscruptions and orders."""
     
    file1 = open("./subscription.sql", "r") 
    return file1.read()

def get_logistics_db_schema() -> str:
    """Use this function in order to write better fulfillment SQL in the reports. The fullfilment database
    is used to get data about the status of orders that are picked and packed for all customers and acrross all stores"""
     
    file1 = open("./fulfillment.sql", "r") 
    return file1.read()

@tool
def document_the_report(report_name) -> str:
    """this tool shall get called every time a to update the README file in the Reports directory. """
     
    file1 = open("./fulfillment.sql", "r") 
    return file1.read()

@tool
def create_directory(directory: str) -> str:
    """
    Create a new writable directory with the given directory name if it does not exist.
    If the directory exists, it ensures the directory is writable.

    Parameters:
    directory (str): The name of the directory to create.

    Returns:
    str: Success or error message.
    """
    if ".." in directory:
        return f"Cannot make a directory with '..' in path"
    try:
        os.makedirs(directory, exist_ok=True)
        subprocess.run(["chmod", "u+w", directory], check=True)
        return f"Directory successfully '{directory}' created and set as writeable."
    except subprocess.CalledProcessError as e:
        return f"Failed to create or set writable directory '{directory}': {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@tool
def find_file(filename: str, path: str) -> Optional[str]:
    """
    Recursively searches for a file in the given path.
    Returns string of full path to file, or None if file not found.
    """
    # TODO handle multiple matches
    for root, dirs, files in os.walk(path):
        if filename in files:
            return os.path.join(root, filename)
    return None


@tool
def create_file(filename: str, content: str = "", directory=""):
    """Creates a new file and content in the specified directory."""
    # Validate file type
    try:
        file_stem, file_type = filename.split(".")
        assert file_type in VALID_FILE_TYPES
    except:
        return f"Invalid filename {filename} - must end with a valid file type: {VALID_FILE_TYPES}"
    directory_path = os.path.join(ROOT_DIR, directory)
    file_path = os.path.join(directory_path, filename)
    if not os.path.exists(file_path):
        try:
            with open(file_path, "w")as file:
                file.write(content)
            print(f"File '{filename}' created successfully at: '{file_path}'.")
            return f"File '{filename}' created successfully at: '{file_path}'."
        except Exception as e:
            print(f"Failed to create file '{filename}' at: '{file_path}': {str(e)}")
            return f"Failed to create file '{filename}' at: '{file_path}': {str(e)}"
    else:
        print(f"File '{filename}' already exists at: '{file_path}'.")
        return f"File '{filename}' already exists at: '{file_path}'."


@tool
def update_file(filename: str, content: str, directory: str = ""):
    """Updates, appends, or modifies an existing file with new content."""
    if directory:
        file_path = os.path.join(ROOT_DIR, directory, filename)
    else:
        file_path = find_file(filename, ROOT_DIR)

    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "a") as file:
                file.write(content)
            return f"File '{filename}' updated successfully at: '{file_path}'"
        except Exception as e:
            return f"Failed to update file '{filename}' at: '{file_path}' - {str(e)}"
    else:
        return f"File '{filename}' not found at: '{file_path}'"

# create_react_app_with_vite,
# List of tools to use
tools = [
    ShellTool(ask_human_input=True),
    create_directory,
    get_fulfillment_db_schema,
    get_subscription_db_schema,
    find_file,
    create_file,
    update_file
    # Add more tools if needed
]


# Configure the language model
llm = ChatOpenAI(model="gpt-4o", temperature=0)


# Set up the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a data analyst that generates jupyter notebook reports to measure the health of various parts of the CookUnity business.
                Reports should be created in the Reports directory and should be named with the format 'report_<date>.ipynb'.
                If a project is not set up in the reports directory, please add requirements.txt file and the proper libraries needed to generate the data, including but not limited to graphing libraries, sql client etc..
                if a project is already set up, feel free to add more libraries to requirements.txt file as needed.
            """,
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# Bind the tools to the language model
llm_with_tools = llm.bind_tools(tools)


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# Main loop to prompt the user
while True:
    user_prompt = input("Prompt: ")

    # Add user prompt to memory
    memory.append(f"user: {user_prompt}")
    
    # Compile context from memory
    context = "\n".join(memory)
    
    # Get agent's response
    response = list(agent_executor.stream({"input": context}))
    
    # Extract the agent's message from the response and add it to memory
    print(response[-1])
    agent_message = response[-1]['output']  # Adjust based on your response structure
    memory.append(f"ai_assistant: {agent_message}")
    
    # Print agent's response
    print(agent_message)