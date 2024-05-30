from typing import Optional

from phi.assistant import Assistant
from phi.knowledge import AssistantKnowledge
from phi.llm.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.embedder.openai import OpenAIEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


def get_auto_rag_assistant(
    llm_model: str = "gpt-4-turbo",
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Assistant:
    """Get an Auto RAG Assistant."""

    return Assistant(
        name="Sir Frank",
        run_id=run_id,
        user_id=user_id,
        llm=OpenAIChat(model=llm_model),
        storage=PgAssistantStorage(table_name="auto_rag_assistant_openai", db_url=db_url),
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=db_url,
                collection="auto_rag_documents_openai",
                embedder=OpenAIEmbedder(model="text-embedding-3-small", dimensions=1536),
            ),
            # 3 references are added to the prompt
            num_documents=3,
        ),
        description="You are a helpful Assistant called 'Frank' designed to assist lawyers in their legal tasks efficiently.",
        instructions=[
            "Given a legal query or task, first ALWAYS search your knowledge base using the `search_knowledge_base` tool to see if you have relevant legal documents, case laws, statutes, or regulations.",
            "If you don't find relevant information in your knowledge base, use the `duckduckgo_search` tool to search the internet for additional legal resources and information.",
            "If you need to reference the chat history for context or previous interactions, use the `read_chat_history` tool.",
            "If the user's question or task is unclear, ask clarifying questions to gather more specific information.",
            "Carefully read the information you have gathered, ensuring it is accurate and relevant to the legal query or task, and provide a clear and concise answer or action plan to the user.",
            "Do not use phrases like 'based on my knowledge' or 'depending on the information'. Instead, provide definitive and actionable insights or recommendations based on the gathered information.",
            "When drafting or reviewing legal documents, ensure they adhere to relevant legal standards and best practices.",
            "Always maintain confidentiality and compliance with data privacy regulations when handling legal documents and client information.",
            "After analyzing the initial query, call the secondary assistant David to perform detailed case research using the DuckDuckGo search."
        ],

        # Show tool calls in the chat
        show_tool_calls=True,
        # This setting gives the LLM a tool to search the knowledge base for information
        search_knowledge=True,
        # This setting gives the LLM a tool to get chat history
        read_chat_history=True,
        tools=[DuckDuckGo()],
        # This setting tells the LLM to format messages in markdown
        markdown=True,
        # Adds chat history to messages
        add_chat_history_to_messages=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )



def get_case_research_agent(
    llm_model: str = "gpt-4-turbo",
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Assistant:
    """Get a Case Research Agent."""

    return Assistant(
        name="case_research_agent",
        run_id=run_id,
        user_id=user_id,
        llm=OpenAIChat(model=llm_model),
        storage=PgAssistantStorage(table_name="case_research_agent_openai", db_url=db_url),
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=db_url,
                collection="case_research_documents_openai",
                embedder=OpenAIEmbedder(model="text-embedding-3-small", dimensions=1536),
            ),
            # 3 references are added to the prompt
            num_documents=3,
        ),
        description="You are a helpful Assistant called 'David' designed to perform detailed case research for legal queries.",
        instructions=[
            "Given a legal query, perform a detailed analysis to understand the case.",
            "Use the `duckduckgo_search` tool to find relevant case laws, statutes, regulations, and legal opinions on the internet.",
            "If the users question is unclear, ask clarifying questions to get more information.",
            "Carefully read the information you have gathered and provide a clear and concise summary of your findings.",
            "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
            "Ensure all provided information is relevant and accurate to the legal query.",
        ],
        # Show tool calls in the chat
        show_tool_calls=True,
        # This setting gives the LLM a tool to search the knowledge base for information
        search_knowledge=True,
        # This setting gives the LLM a tool to get chat history
        read_chat_history=True,
        tools=[DuckDuckGo(timeout = 5)],
        # This setting tells the LLM to format messages in markdown
        markdown=True,
        # Adds chat history to messages
        add_chat_history_to_messages=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )
