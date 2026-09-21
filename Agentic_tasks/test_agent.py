import os
import sys

BMO_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BMO_ROOT not in sys.path:
    sys.path.insert(0, BMO_ROOT)

from langchain_core.messages import HumanMessage
from Agent_BMO.graph import bmo_graph


result = bmo_graph.invoke({
    "messages": [
        HumanMessage(
            content="""Remember that I need to update my API module.
            also remind me to wipe shreya's shit"""
            
        )
    ]
})

print(result["messages"][-1].content)