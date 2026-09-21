import os
import json

from dotenv import load_dotenv
load_dotenv()

from groq import Groq

from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from Agent_BMO.tools import save_note, get_notes


# ---------------------------------------------------------
# BMO's state
# ---------------------------------------------------------

class BMOState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---------------------------------------------------------
# Groq
# ---------------------------------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------------------------------------------------
# BMO's tools
# ---------------------------------------------------------

def remember(note: str):

    return save_note(note)


def show_notes():

    return get_notes()


# ---------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": (
                "Save a task, reminder, plan, or piece of information "
                "that the user wants BMO to remember for later."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {
                        "type": "string",
                        "description": "The exact thing BMO should remember."
                    }
                },
                "required": ["note"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "show_notes",
            "description": (
                "Retrieve the user's saved pending tasks and notes. "
                "Use this when the user asks what they need to do, "
                "what they asked BMO to remember, their pending tasks, "
                "reminders, saved notes, or anything similar."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# ---------------------------------------------------------
# Execute a tool
# ---------------------------------------------------------

def execute_tool(tool_call):

    name = tool_call["function"]["name"]

    arguments = json.loads(
        tool_call["function"]["arguments"]
    )

    if name == "remember":

        return remember(
            arguments["note"]
        )

    if name == "show_notes":

        return show_notes()

    return "Unknown tool."


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------

def agent(state: BMOState):

    user_message = state["messages"][-1].content

    messages = [
        {
            "role": "system",
            "content": (
                "You are BMO, a friendly personal assistant. "
                "You have persistent memory tools.\n\n"

                "IMPORTANT MEMORY RULES:\n"

                "1. If the user says remember, remind me, "
                "don't let me forget, I need to do, "
                "I have to do, or gives you a future task, "
                "use the remember tool.\n"

                "2. If the user asks what they need to do, "
                "what they asked you to remember, "
                "what tasks are pending, their reminders, "
                "their saved notes, or similar, "
                "use the show_notes tool.\n"

                "3. Do not ask unnecessary clarification "
                "when the user's request can be answered "
                "using your memory.\n"

                "4. After using a memory tool, answer the user "
                "naturally and briefly."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]


    # -----------------------------------------------------
    # First LLM call
    # -----------------------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=messages,

        tools=tools,

        tool_choice="auto",

        temperature=0.2,

        max_completion_tokens=300
    )

    assistant_message = response.choices[0].message


    # -----------------------------------------------------
    # If BMO wants to use a tool
    # -----------------------------------------------------

    if assistant_message.tool_calls:

        # Add assistant's tool-call message
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in assistant_message.tool_calls
                ]
            }
        )


        # Execute every requested tool
        for tool_call in assistant_message.tool_calls:

            result = execute_tool(
                {
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )


        # -------------------------------------------------
        # Give the tool result back to BMO
        # -------------------------------------------------

        final_response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=messages,

            temperature=0.2,

            max_completion_tokens=300
        )

        final_text = (
            final_response
            .choices[0]
            .message
            .content
        )

        return {
            "messages": [
                AIMessage(
                    content=final_text
                )
            ]
        }


    # -----------------------------------------------------
    # Normal conversation
    # -----------------------------------------------------

    return {
        "messages": [
            AIMessage(
                content=assistant_message.content
            )
        ]
    }


# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------

graph_builder = StateGraph(BMOState)

graph_builder.add_node(
    "agent",
    agent
)

graph_builder.add_edge(
    START,
    "agent"
)

graph_builder.add_edge(
    "agent",
    END
)

bmo_graph = graph_builder.compile()