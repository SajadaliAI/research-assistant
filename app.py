import os
import certifi
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults

# ==================================================
# LOAD ENV VARIABLES
# ==================================================

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .hero {
        text-align: center;
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(135deg,#1f4e79,#3b82f6);
        color: white;
        margin-bottom: 20px;
    }

    .response-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #3b82f6;
        color: black;
        font-size: 16px;
    }

    .footer {
        text-align: center;
        color: gray;
        margin-top: 40px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# HERO SECTION
# ==================================================

st.markdown(
    """
    <div class="hero">
        <h1>🤖 Agentic AI Assistant</h1>
        <p>Powered by Gemini 2.5 Flash + Tavily Search + LangChain</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("⚙️ Agent Settings")

    st.success("Gemini Connected")

    st.markdown("---")

    st.markdown("""
### Features

✅ Gemini 2.5 Flash

✅ Tavily Search

✅ ReAct Agent

✅ LangChain

✅ Streamlit UI
""")

# ==================================================
# API KEY CHECK
# ==================================================

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

if not TAVILY_API_KEY:
    st.error("TAVILY_API_KEY not found in .env file")
    st.stop()

# ==================================================
# SEARCH TOOL
# ==================================================

search_tool = TavilySearchResults(
    max_results=3
)

# ==================================================
# LLM
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY
)

# ==================================================
# PROMPT
# ==================================================

prompt = hub.pull("hwchase17/react")

# ==================================================
# TOOLS
# ==================================================

tools = [search_tool]

# ==================================================
# AGENT
# ==================================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ==================================================
# EXECUTOR
# ==================================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ==================================================
# USER INPUT
# ==================================================

user_query = st.text_input(
    "Ask Anything",
    placeholder="Example: What is the capital of Pakistan?"
)

# ==================================================
# BUTTON
# ==================================================

col1, col2 = st.columns([1, 5])

with col1:
    run_button = st.button(
        "🚀 Run",
        use_container_width=True
    )

# ==================================================
# RUN AGENT
# ==================================================

if run_button:

    if user_query:

        with st.spinner("🧠 Agent is thinking..."):

            try:

                response = agent_executor.invoke(
                    {"input": user_query}
                )

                st.success("✅ Response Generated")

                st.markdown("### 🤖 Final Response")

                st.markdown(
                    f"""
                    <div class="response-box">
                    {response['output']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(f"❌ Error: {str(e)}")

    else:

        st.warning("⚠️ Please enter a query")

# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        Made with ❤️ using Streamlit, Gemini, Tavily & LangChain
    </div>
    """,
    unsafe_allow_html=True
)
