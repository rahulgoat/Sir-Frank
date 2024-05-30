import nest_asyncio
from typing import List

import streamlit as st
from phi.assistant import Assistant
from phi.document import Document
from phi.document.reader.pdf import PDFReader
from phi.document.reader.website import WebsiteReader
from phi.utils.log import logger

from assistant import get_auto_rag_assistant  # type: ignore
from assistant import get_case_research_agent


nest_asyncio.apply()
st.set_page_config(
    page_title="Sir Frank",
    page_icon=":black_heart:",
)
st.title("Autonomous RAG")
st.markdown("##### :orange_heart: built using [phidata](https://github.com/phidatahq/phidata)")

