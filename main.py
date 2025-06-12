import os
import aiohttp
import asyncio
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from agent_tasks import (
    handle_task_a1,
    handle_task_a2_format_md,
    handle_task_a3_count_weekday,
    handle_task_a4_sort_contacts,
    handle_task_a5_logs_recent,
    handle_task_a6_md_index,
    handle_task_a10_sum_gold,
    # async handlers:
    handle_task_a7_extract_email,
    handle_task_a8_extract_card,
    handle_task_a9_similar_comments,
    # Phase B
    handle_task_b3_fetch_api,
    handle_task_b4_clone_and_commit,
    handle_task_b5_run_sql,
    handle_task_b6_scrape,
    handle_task_b7_compress_resize,
    handle_task_b8_transcribe,
    handle_task_b9_md_to_html,
    handle_task_b10_filter_csv,
)

app = FastAPI()

# Root endpoints for GET and POST to avoid 404/405 and JSON parse errors on /
@app.get("/")
async def root_get():
    return JSONResponse(content={"answer": "ok"})

@app.post("/")
async def root_post():
    return JSONResponse(content={"answer": "ok"})

# CORS (optional, for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Always use /data as the root for all file operations
DATA_DIR = os.path.abspath("/data")

# --- Utility functions ---
def safe_path(path: str) -> str:
    """Ensure the path is within /data and normalized."""
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(DATA_DIR):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    return abs_path

async def call_llm(prompt: str, files: Optional[dict] = None) -> str:
    """Call GPT-4o-Mini via AI Proxy with a concise prompt."""
    token = os.environ.get("AIPROXY_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="AIPROXY_TOKEN not set.")
    url = "https://api.aiproxy.io/v1/completions"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.0,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=500, detail=f"LLM call failed: {await resp.text()}")
            data = await resp.json()
            return data.get("choices", [{}])[0].get("text", "")

# --- Endpoints ---
@app.post("/run")
async def run_task(request: Request, task: Optional[str] = None):
    # Parse task from query or body
    if not task:
        try:
            data = await request.json()
            task = data.get("task")
        except Exception:
            task = None
    if not task:
        raise HTTPException(status_code=400, detail="Task description required.")

    # Step 1: Use LLM to parse the task and determine the required action
    try:
        llm_prompt = (
            "You are an automation agent. Parse this task and return a JSON with 'action', 'inputs', and 'output_path' fields. "
            "If the task is to run datagen.py, set action to 'run_datagen', and extract the email as 'user_email'. "
            f"Task: {task}"
        )
        llm_response = await call_llm(llm_prompt)
        import json
        try:
            parsed = json.loads(llm_response.strip())
        except Exception:
            raise HTTPException(status_code=400, detail=f"LLM could not parse task: {llm_response}")
        action = parsed.get("action")
        inputs = parsed.get("inputs", {})
        output_path = parsed.get("output_path")

        # Dispatch to the correct handler
        if action == "run_datagen":
            user_email = inputs.get("user_email")
            if not user_email:
                raise HTTPException(status_code=400, detail="user_email missing for datagen task")
            result = await asyncio.to_thread(handle_task_a1, user_email)
            return {"status": "ok", "result": result}
        elif action == "format_markdown":
            md_path = inputs.get("md_path")
            prettier_version = inputs.get("prettier_version", "3.4.2")
            result = await asyncio.to_thread(handle_task_a2_format_md, md_path, prettier_version)
            return {"status": "ok", "result": result}
        elif action == "count_weekday":
            dates_path = inputs.get("dates_path")
            weekday = inputs.get("weekday")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_a3_count_weekday, dates_path, weekday, output_path)
            return {"status": "ok", "result": result}
        elif action == "sort_contacts":
            input_path = inputs.get("input_path")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_a4_sort_contacts, input_path, output_path)
            return {"status": "ok", "result": result}
        elif action == "logs_recent":
            logs_dir = inputs.get("logs_dir")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_a5_logs_recent, logs_dir, output_path)
            return {"status": "ok", "result": result}
        elif action == "md_index":
            docs_dir = inputs.get("docs_dir")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_a6_md_index, docs_dir, output_path)
            return {"status": "ok", "result": result}
        elif action == "extract_email":
            email_path = inputs.get("email_path")
            output_path = output_path or inputs.get("output_path")
            result = await handle_task_a7_extract_email(call_llm, email_path, output_path)
            return {"status": "ok", "result": result}
        elif action == "extract_card":
            img_path = inputs.get("img_path")
            output_path = output_path or inputs.get("output_path")
            result = await handle_task_a8_extract_card(call_llm, img_path, output_path)
            return {"status": "ok", "result": result}
        elif action == "similar_comments":
            comments_path = inputs.get("comments_path")
            output_path = output_path or inputs.get("output_path")
            result = await handle_task_a9_similar_comments(call_llm, comments_path, output_path)
            return {"status": "ok", "result": result}
        elif action == "sum_gold":
            db_path = inputs.get("db_path")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_a10_sum_gold, db_path, output_path)
            return {"status": "ok", "result": result}
        # Phase B handlers
        elif action == "fetch_api":
            api_url = inputs.get("api_url")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_b3_fetch_api, api_url, output_path)
            return {"status": "ok", "result": result}
        elif action == "clone_and_commit":
            repo_url = inputs.get("repo_url")
            commit_msg = inputs.get("commit_msg")
            file_path = inputs.get("file_path")
            file_content = inputs.get("file_content")
            result = await asyncio.to_thread(handle_task_b4_clone_and_commit, repo_url, commit_msg, file_path, file_content)
            return {"status": "ok", "result": result}
        elif action == "run_sql":
            db_path = inputs.get("db_path")
            sql = inputs.get("sql")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_b5_run_sql, db_path, sql, output_path)
            return {"status": "ok", "result": result}
        elif action == "scrape":
            url = inputs.get("url")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_b6_scrape, url, output_path)
            return {"status": "ok", "result": result}
        elif action == "compress_resize":
            img_path = inputs.get("img_path")
            output_path = output_path or inputs.get("output_path")
            size = tuple(inputs.get("size", (256, 256)))
            result = await asyncio.to_thread(handle_task_b7_compress_resize, img_path, output_path, size)
            return {"status": "ok", "result": result}
        elif action == "transcribe":
            mp3_path = inputs.get("mp3_path")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_b8_transcribe, mp3_path, output_path)
            return {"status": "ok", "result": result}
        elif action == "md_to_html":
            md_path = inputs.get("md_path")
            output_path = output_path or inputs.get("output_path")
            result = await asyncio.to_thread(handle_task_b9_md_to_html, md_path, output_path)
            return {"status": "ok", "result": result}
        elif action == "filter_csv":
            csv_path = inputs.get("csv_path")
            filter_expr = inputs.get("filter_expr")
            result = await asyncio.to_thread(handle_task_b10_filter_csv, csv_path, filter_expr)
            return {"status": "ok", "result": result}
        return {"status": "unhandled", "llm_response": llm_response, "parsed": parsed}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/read")
def read_file(path: str):
    try:
        abs_path = safe_path(path)
        if not os.path.isfile(abs_path):
            raise HTTPException(status_code=404, detail="File not found.")
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return PlainTextResponse(content, status_code=200)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")