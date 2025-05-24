# Automated R Code Generation Assistant

## Overview

This project is an intelligent assistant that helps you generate R code for tasks like data analysis, visualization, and more. Powered by **Llama-3.3-70b** model through **Groq API**, it ensures that all solutions are delivered in R, and provides friendly, clear explanations and step-by-step instructions. With built-in code analysis and performance feedback, you can be sure the R code you receive is clean, efficient, and ready to use.

## Features

- **R-Only Code Generation:** No matter what you ask, all code output is in R—perfect for R users and learners.
- **Conversational Chatbot Interface:** Interact naturally through a simple web UI, describing your needs in plain English.
- **Automatic Code Review:** Every generated script is automatically checked for style issues, executed, and analyzed for performance (including execution time and memory usage).
- **Structured and Clear Output:** Code results come with explanations, bullet-point highlights, and step-by-step instructions, all neatly organized.
- **Session-Based Chat:** Your conversation is kept organized and context-aware, even over multiple prompts.
- **Downloadable Reports:** Get a detailed, ready-to-share report of your code’s analysis with just one click.

## How It Works

1. **Describe Your Task:** Type what you want to do in R.
2. **AI Generates R Code:** The assistant (powered by Llama-3.3-70b via Groq API) interprets your request and creates an R script, following best practices and strict R-only rules.
3. **Review and Understand:** You receive the code, a friendly explanation, key points about what it does, and easy-to-follow setup instructions.
4. **Automatic Analysis:** The code is checked for common issues, executed in a safe environment, and the results (success, warnings, performance) are summarized.
5. **Download and Use:** Download a handy analysis report.

## Technologies Used

- **Python:** The main logic and user interface (Streamlit).
- **R:** For code generation, linting, and running scripts.
- **Streamlit:** The interactive web UI.
- **LangChain & Groq API:** Language model orchestration and AI backend.
- **dotenv:** Securely manages your API keys.
- **R Packages:** `lintr` and `pryr` for code checking and performance analysis.

## Setup and Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hrishikeshChandi/automated-code-generation-for-r.git
   cd automated-code-generation-for-r
   ```

2. **Install required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API keys:**

   - Copy the `.env` file and fill in your keys:
     ```
     LANGCHAIN_API_KEY=your_langchain_api_key
     LANGCHAIN_PROJECT=project_name
     GROQ_API_KEY=your_groq_api_key
     ```

4. **Ensure R is installed:**

   - Install R if you haven’t already.
   - The necessary R packages (`lintr`, `pryr`) are installed automatically when you run an analysis.

5. **Start the assistant:**

   ```bash
   streamlit run main.py
   ```

## Project Structure

```
.
├── main.py             # The main app (Streamlit, Python)
├── wrapper.r           # R script for code linting and analysis
├── requirements.txt    # Python dependencies
├── .env                # Your API keys (not tracked in git)
├── trial.r             # Generated R code (temporary, during use)
├── output.txt          # AI model’s raw output (temporary)
├── analysis_report.txt # Detailed analysis of your R code
```

## Results

- **Instant R code:** Get ready-to-run, well-documented R scripts for your tasks.
- **Confidence in quality:** Every script is checked for errors, warnings, and best practices automatically.
- **Easy to understand:** Each result comes with clear explanations and instructions.
- **Takeaways:** Download full reports and code for your records or sharing.

## Notes

- The assistant only produces R code—requests for other languages will be politely redirected or converted to R.
- Make sure your R installation path matches what’s in `main.py` (edit if needed for your system).
- The assistant only outputs code when you explicitly ask for it.
- API keys are required for full functionality—your data is managed securely.

## License

This project is licensed under the MIT License.
