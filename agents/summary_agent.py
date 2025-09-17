# services/agents.py
from langgraph.prebuilt import create_react_agent
from services.tools import transcript_summarizer
from services.models.summary_model import summarymodel

llm_model = summarymodel

def summary_agent(state: dict) -> dict:
    messages = state.get("messages", [])
    if not messages:
        file_id = state.get("file_id")
        if not file_id:
            raise ValueError("file_id missing in state")
        messages = [{"role": "user", "content": f"Please summarize the transcript for file: {file_id}"}]

    # Pass the original tool, no wrapper
    agent = create_react_agent(llm_model, [transcript_summarizer])

    # Pass llm_model via invoke so the tool receives it
    result = agent.invoke({"messages": messages, "llm": llm_model})

    state["answer"] = result["messages"][-1].content
    return state
