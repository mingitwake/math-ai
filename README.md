## Math-AI

#### Google's ADK Implementation

Artifacts used during Google's ADK Workshop. 

Installation
```
# Create Virtual Environment
python -m venv .venv

# Activate
# macOS/Linux: source .venv/bin/activate
# Windows CMD: .venv\Scripts\activate.bat

pip install google-adk litellm crewai "crewai[tools]"
```

Create a .env file for the credentials
```
.env
    GOOGLE_GENAI_USE_VERTEXAI=FALSE
    GOOGLE_API_KEY="..."
    AZURE_API_KEY="..."
    AZURE_API_BASE="..."
    AZURE_API_VERSION="..."
```

The project structure should look like this:
```
math-ai/
    .venv
    Google-ADK/
        .env
        autograder/
            __init__.py
            agent.py
            prompt
    app/..
    pix2text/..
```

#### Other Dependencies
```
# Activate (if not already activated in Terminal)
# macOS/Linux: source .venv/bin/activate
# Windows CMD: .venv\Scripts\activate.bat

pip install pix2text -i https://mirrors.aliyun.com/pypi/simple
pip install fastapi uvicorn
```

#### Testing
In a new Terminal, activate the virtual environment and navigate to "Google-ADK":
```
math-ai/
    .venv
    Google-ADK/ <-- Here
        .env
        autograder/
            __init__.py
            agent.py
            prompt
    app/..
    pix2text/..
```
```
adk api_server
```
In a new Terminal, activate the virtual environment and navigate to "math-ai":
```
math-ai/  <-- Here
    .venv
    Google-ADK/
        .env
        autograder/
            __init__.py
            agent.py
            prompt
    app/
        main.py
    pix2text/..
```
```
uvicorn app.main:app --reload --port 9000
curl http://localhost:9000/docs
```
