#  🤖 AI-Powered DOC/PDF → Summary Agent with FastAPI & Docker
This AI project converts **DOC/PDF documents** into clean transcripts and summaries using  **LLM Agent** with **FastAPI**, and deployment in **Docker** and log metedata (JSON) in **TinyDB**.  

**What’s next?**

**Integration with ChromaDB for vector storage, building a Q&A Agent, developing an Orchestration Agent, and deploying on AWS EC2 for scalable cloud hosting.**

**LLM Model: "openai/gpt-oss-20b"** from **Grok**
**Core Frameworks:**: Langchain, Langgraph

```mermaid
flowchart TD

    %% Nodes with unique styles and relevant icons
    A["📄 DOC / PDF Upload"]:::upload --> 
    B["📝 Transcript Extraction<br/>and Cleaning"]:::process -->
    C["🧾 Metadata Log<br/>in TinyDB (JSON)"]:::log -->
    D["🧠 Summary Agent<br/>Clean Transcript from log of Metadata & LLM Model "]:::agent -->
    E["🚀 FastAPI Deployment<br/>Agent, Endpoint & Routes"]:::api -->
    F["🐳 Docker Deployment<br/>Full Project"]:::docker -->
    G["🔁 Push to GitHub"]:::github 
   

    %% Custom styles
    classDef upload fill:#D6EAF8,stroke:#2980B9,stroke-width:2px,color:#1B4F72;
    classDef process fill:#FCF3CF,stroke:#B7950B,stroke-width:2px,color:#7D6608;
    classDef log fill:#FADBD8,stroke:#C0392B,stroke-width:2px,color:#922B21;
    classDef agent fill:#D5F5E3,stroke:#27AE60,stroke-width:2px,color:#1E8449;
    classDef api fill:#E8DAEF,stroke:#8E44AD,stroke-width:2px,color:#5B2C6F;
    classDef docker fill:#D1F2EB,stroke:#16A085,stroke-width:2px,color:#0E6251;
    classDef github fill:#EBEDEF,stroke:#566573,stroke-width:2px,color:#2C3E50;


```
## 📂 Create Directories & Services

### 🖥️ Ubuntu Terminal Commands

##### Create directory and change directory
```sh
mkdir endpoints schemas services agents
```
```sh
cd agents
```
```sh
cd ..
```

##### Create Nano file Write Out and Exit: `Ctrl + O  >> Enter  >>  Ctrl + X`
```sh
nano main.py
```
##### Create blank files with touch under agents directory
```sh
touch  summary_agent.py 
```
## 🐍 Python Virtual Environment (pyenv + venv)
```sh
pyenv shell 3.10.8
```
```sh
python -m venv agentsenv
```

##### check the list already install
```sh
pip list
conda list
```
#####  Freeze and prepare requirement.txt all installed libraries
```sh
pip freeze > requirements.txt
```
##### Install requiremnets.txt
```sh
pip install -r requirements.txt
```

## 📝 Edit .py files

- enpoints
- agents
- services
- schemas

```sh
nano endpoints/health.py
```
## 💡 Prepare Endpoints and main.py


#### 🚀 Run FastAPI App (main.py)
```sh
uvicorn main:app --reload
```
## 📁 Project Structure

![alt text](screenshots/workflow.png)


**⚠️Note:** Due to time constraint, Iconstraints, I could not complete:

- ChromaDB Integration
- Q&A Agent
- Orchestrator Agent
These require additional research and time to integrate.

## 🐳 Install Docker and Docekr Envo Setup

**📌 Link to Git Repo:** https://github.com/Shibli-Nomani/Multimodal-AI-Inference-APIs-using-FastAPI

## 🐳 Create Docker-Compose.yml and DockerFile
- Python version will based on the version I work. But I use the slim on here (`python:3.10.8-slim`)
- I listed all directories explicitly (agents, endpoints, schemas, services, models, utils, web, logs) so nothing gets missed.

## Docker Command

Go to Ubuntu Terminal and apply those command.
![alt text](screenshots/image-01.png)

```sh
docker build -t ai-powered-text-summarization . 
```
``
```sh
docker run -d -p 8000:8000 ai-powered-text-summarization
```
## 📤 Output Results

### 🧑‍⚕️ Health  
![alt text](screenshots/image-02.png)

### 📜 Transcript

![alt text](screenshots/image-03.png)
![alt text](screenshots/image-04.png)

### 🧹 Clean the Transcript 
![alt text](screenshots/image-05.png)

### 📁 Logs 
It has real text, size, status, transcript length, transcript, upload time, clean transcript and clean transcript length.

![alt text](screenshots/image-06.png)
![alt text](screenshots/image-07.png)

### 📝 Summary

![alt text](screenshots/image-08.png)
![alt text](screenshots/image-09.png)

## ❌ Add .gitigore before pushing to Github
add list of files and folders which are going to ignore while pushing to github.

## 🐙 Git Initiate, Git Push and Commit
```sh
git init
```
