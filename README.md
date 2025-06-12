# LLM-based Automation Agent

This project is an automation agent for DataWorks Solutions, designed to process plain-English tasks using a Large Language Model (LLM) and expose a verifiable API.

## Features
- **POST /run?task=...**: Accepts a plain-English task, parses and executes it, and returns the result.
- **GET /read?path=...**: Returns the content of a specified file for verification.
- **Safe Operations**: Never deletes files or accesses data outside `/data`.
- **LLM Integration**: Uses GPT-4o-Mini via AI Proxy for task parsing and execution.
- **Dockerized**: Easily deployable as a container.

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the API server:
   ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Build and run with Docker:
   ```sh
   docker build -t llm-agent .
   docker run --rm -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 llm-agent
   ```

## License
MIT License (see LICENSE file)
