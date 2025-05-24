import uuid
import os
import json
import subprocess
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv(dotenv_path="./.env")

st.set_page_config(layout="wide")

system_prompt = """ 
You are an R-only assistant. Follow these strict rules:

General Rules:
- Accept only R programming tasks.
- If asked about other languages, politely say: "I'm trained only on R".
- For casual/personal questions, respond naturally without JSON.
- if its not mentioned or forcibly not told to give the code dont return a JSON object just return a string containing all the necessary information needed

Code Responses (Only when user asks for code):
- Return a single valid JSON object with keys: explanation, code, points, instructions.
- The JSON must be parseable using Python’s `json.loads()` — no markdown, backticks, or extra text.
- Start response with `{` and end with `}`. Nothing before/after.
- Only one JSON object per reply.
- if code is asked only JSON should be returned
- structure

{
  "explanation": "Short, friendly explanation of what the user is asking or why an error is happening.",
  "code": "Clean, well-formatted R code as a string. Escape newlines as \\n and double quotes as \\\". Always start code with options(repos = c(CRAN = 'https://cloud.r-project.org')) and include necessary install.packages() calls.",
  "points": ["Short bullet points explaining what the code does and which packages are used."],
  "instructions": ["List of clear sentences, such as 'Install ggplot2 using install.packages(\"ggplot2\")', 'Load it using library(ggplot2)' etc."]
}

Code Standards:
- Only R code. Never use other languages.
- Use: `options(repos = c(CRAN = 'https://cloud.r-project.org'))` at the top.
- All packages must check if installed first, then install if missing.
- Use `cat(capture.output(...), sep = "\n")` instead of `print()` for outputs.
- If plots are generated, save them as `.png` files.
- Document code clearly with comments.
- Format the code properly add space, tabs, newlines whenever needed. 

Error Handling:
- When user pastes an error, explain it (no code unless asked).
- Use second-person tone ("you are facing this error because...").

Non-Programming Prompts:
- Do not return JSON.
- Be friendly and conversational.

Forbidden:
- No markdown/code fences.
- No generic closing phrases.
- No multiple JSONs.
- No print(), no other languages.

Summary:
- Only R code.
- JSON only when code is explicitly requested.
- Friendly chat otherwise.
- Valid JSON with all keys.
"""

groq_api_key = os.getenv("GROQ_API_KEY")


def get_model():
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key)
    # llm = ChatGroq(model="Gemma2-9b-It", api_key=groq_api_key)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="input"),
        ]
    )

    chain = prompt | llm

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in st.session_state:
            st.session_state[session_id] = ChatMessageHistory()
        return st.session_state[session_id]

    model = RunnableWithMessageHistory(chain, get_session_history)

    return model


st.title("Welcome to the R Code generator with Llama-3.3-70b")
st.write("This is a simple chatbot that can generate R code for various tasks.")
# st.info("Please wait for some time after submitting your prompt, it may take some time :)")

input_query = st.text_area(
    "Enter a breif description about your task (make sure that you mention all the details about it)"
)

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

config = {"configurable": {"session_id": st.session_state["session_id"]}}

if input_query:
    model = get_model()
    result = model.invoke({"input": input_query}, config=config).content

    result = result.replace("```", "").replace("json", "").replace('R"', "")

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(result)

    if result.startswith("{"):
        result = json.loads(result)

        # with open("json_output.json", "w", encoding="utf-8") as f:
        #     json.dump(result, f, indent=4)

        with open("trial.r", "w") as f:
            if result["code"]:
                f.write(result["code"])

        st.markdown("**Explanation**")
        st.write(result["explanation"])

        st.markdown("**Important points**")
        for point in result["points"]:
            st.markdown(f"- {point.strip()}")

        st.markdown("**Instructions**")
        for point in result["instructions"]:
            st.markdown(f"- {point.strip()}")

        st.sidebar.subheader("R Code")
        st.sidebar.code(result["code"], language="r")

        if st.sidebar.button("Analyze"):
            wrapper_output = subprocess.run(
                [r"C:\Program Files\R\R-4.5.0\bin\x64\RScript.exe", "wrapper.r"],
                capture_output=True,
                text=True,
            )

            if wrapper_output.stderr:
                st.sidebar.subheader("Errors or Warnings")
                st.sidebar.code(wrapper_output.stderr)

            with open("analysis_report.txt", "r", encoding="utf-8") as f:
                content = f.read()

            st.sidebar.download_button(
                label="Download your analysis",
                data=content,
                file_name="./analysis_report.txt",
                mime="text/plain",
            )

    else:
        st.write(result)
