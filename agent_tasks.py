# --- Phase B: Business Task Stubs ---
def handle_task_b3_fetch_api(api_url: str, output_path: str) -> str:
    import requests
    abs_out = os.path.abspath(output_path)
    if not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    resp = requests.get(api_url)
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return f"Fetched {api_url} to {output_path}"

def handle_task_b4_clone_and_commit(repo_url: str, commit_msg: str, file_path: str, file_content: str) -> str:
    import tempfile, shutil, git
    temp_dir = tempfile.mkdtemp(dir="/data")
    repo = git.Repo.clone_from(repo_url, temp_dir)
    abs_file = os.path.join(temp_dir, file_path)
    os.makedirs(os.path.dirname(abs_file), exist_ok=True)
    with open(abs_file, "w", encoding="utf-8") as f:
        f.write(file_content)
    repo.git.add(A=True)
    repo.index.commit(commit_msg)
    shutil.rmtree(temp_dir)
    return f"Committed to {repo_url}"

def handle_task_b5_run_sql(db_path: str, sql: str, output_path: str) -> str:
    import sqlite3
    abs_db = os.path.abspath(db_path)
    abs_out = os.path.abspath(output_path)
    if not abs_db.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    conn = sqlite3.connect(abs_db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    import json
    with open(abs_out, "w", encoding="utf-8") as f:
        json.dump(rows, f)
    return f"Ran SQL and wrote to {output_path}"

def handle_task_b6_scrape(url: str, output_path: str) -> str:
    import requests
    abs_out = os.path.abspath(output_path)
    if not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    resp = requests.get(url)
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return f"Scraped {url} to {output_path}"

def handle_task_b7_compress_resize(img_path: str, output_path: str, size: tuple) -> str:
    from PIL import Image
    abs_in = os.path.abspath(img_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    with Image.open(abs_in) as img:
        img = img.resize(size)
        img.save(abs_out)
    return f"Resized/compressed image to {output_path}"

def handle_task_b8_transcribe(mp3_path: str, output_path: str) -> str:
    # Stub: Would use a speech-to-text API or library
    abs_in = os.path.abspath(mp3_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    # Not implemented
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write("Transcription not implemented.")
    return f"Stub transcription to {output_path}"

def handle_task_b9_md_to_html(md_path: str, output_path: str) -> str:
    import markdown
    abs_in = os.path.abspath(md_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    with open(abs_in, "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read())
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(html)
    return f"Converted markdown to HTML at {output_path}"

def handle_task_b10_filter_csv(csv_path: str, filter_expr: str) -> list:
    import pandas as pd
    abs_in = os.path.abspath(csv_path)
    if not abs_in.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    df = pd.read_csv(abs_in)
    filtered = df.query(filter_expr)
    return filtered.to_dict(orient="records")
async def handle_task_a7_extract_email(llm_func, email_path: str, output_path: str) -> str:
    abs_in = os.path.abspath(email_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    with open(abs_in, "r", encoding="utf-8") as f:
        content = f.read()
    prompt = f"Extract the sender's email address from this email message. Only output the email address.\n\n{content}"
    email = (await llm_func(prompt)).strip()
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(email)
    return f"Extracted sender email to {output_path}"

async def handle_task_a8_extract_card(llm_func, img_path: str, output_path: str) -> str:
    abs_in = os.path.abspath(img_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    with open(abs_in, "rb") as f:
        img_bytes = f.read()
    import base64
    img_b64 = base64.b64encode(img_bytes).decode()
    prompt = "Extract the credit card number from this image. Only output the number, no spaces."
    card = (await llm_func(prompt + f"\n\n[image base64: {img_b64[:100]}...]")).strip()
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(card)
    return f"Extracted card number to {output_path}"

async def handle_task_a9_similar_comments(llm_func, comments_path: str, output_path: str) -> str:
    abs_in = os.path.abspath(comments_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    with open(abs_in, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f if line.strip()]
    prompt = f"Find the most similar pair of comments from this list. Output only the two comments, one per line.\n\n" + "\n".join(comments)
    result = (await llm_func(prompt)).strip()
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(result)
    return f"Wrote most similar comments to {output_path}"

def handle_task_a10_sum_gold(db_path: str, output_path: str) -> str:
    import sqlite3
    abs_db = os.path.abspath(db_path)
    abs_out = os.path.abspath(output_path)
    if not abs_db.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    conn = sqlite3.connect(abs_db)
    cur = conn.cursor()
    cur.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total = cur.fetchone()[0] or 0
    conn.close()
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(str(total))
    return f"Wrote total gold sales to {output_path}"
import os
import subprocess
from fastapi import HTTPException


import json
def handle_task_a2_format_md(md_path: str, prettier_version: str = "3.4.2") -> str:
    """
    Format the contents of a markdown file using prettier, updating the file in-place.
    """
    abs_path = os.path.abspath(md_path)
    if not abs_path.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    # Install prettier if not present or wrong version
    try:
        result = subprocess.run(["npx", "prettier", "--version"], capture_output=True, text=True)
        if prettier_version not in result.stdout:
            raise Exception()
    except Exception:
        # Install the required version
        subprocess.run(["npm", "install", f"prettier@{prettier_version}"], cwd="/data", check=True)
    # Format the file
    try:
        subprocess.run(["npx", "prettier", "--write", abs_path], check=True)
        return f"Formatted {md_path} with prettier@{prettier_version}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to format markdown: {e}")

def handle_task_a3_count_weekday(dates_path: str, weekday: str, output_path: str) -> str:
    import datetime
    abs_dates = os.path.abspath(dates_path)
    abs_out = os.path.abspath(output_path)
    if not abs_dates.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    count = 0
    with open(abs_dates, "r", encoding="utf-8") as f:
        for line in f:
            try:
                dt = datetime.datetime.strptime(line.strip(), "%Y-%m-%d")
                if dt.strftime("%A").lower() == weekday.lower():
                    count += 1
            except Exception:
                continue
    with open(abs_out, "w", encoding="utf-8") as f:
        f.write(str(count))
    return f"Counted {count} {weekday}s in {dates_path} and wrote to {output_path}"

def handle_task_a4_sort_contacts(input_path: str, output_path: str) -> str:
    abs_in = os.path.abspath(input_path)
    abs_out = os.path.abspath(output_path)
    if not abs_in.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    with open(abs_in, "r", encoding="utf-8") as f:
        contacts = json.load(f)
    contacts.sort(key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))
    with open(abs_out, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    return f"Sorted contacts and wrote to {output_path}"

def handle_task_a5_logs_recent(logs_dir: str, output_path: str) -> str:
    import glob
    abs_logs = os.path.abspath(logs_dir)
    abs_out = os.path.abspath(output_path)
    if not abs_logs.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    log_files = sorted(glob.glob(os.path.join(abs_logs, "*.log")), key=os.path.getmtime, reverse=True)[:10]
    lines = []
    for f in log_files:
        with open(f, "r", encoding="utf-8") as file:
            first = file.readline().strip()
            lines.append(first)
    with open(abs_out, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))
    return f"Wrote first lines of 10 most recent logs to {output_path}"

def handle_task_a6_md_index(docs_dir: str, output_path: str) -> str:
    import glob
    abs_docs = os.path.abspath(docs_dir)
    abs_out = os.path.abspath(output_path)
    if not abs_docs.startswith("/data") or not abs_out.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access outside /data is forbidden.")
    index = {}
    for md_file in glob.glob(os.path.join(abs_docs, "**", "*.md"), recursive=True):
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    index[os.path.relpath(md_file, abs_docs)] = line[2:].strip()
                    break
    with open(abs_out, "w", encoding="utf-8") as out:
        json.dump(index, out, ensure_ascii=False, indent=2)
    return f"Created index at {output_path}"

async def handle_task_a1(user_email: str) -> str:
    """
    Task A1: Install uv (if required) and run datagen.py with user_email as the only argument.
    Downloads datagen.py if not present.
    """
    data_dir = "/data"
    datagen_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    datagen_path = os.path.join(data_dir, "datagen.py")
    # Download datagen.py if not present
    if not os.path.exists(datagen_path):
        import urllib.request
        try:
            urllib.request.urlretrieve(datagen_url, datagen_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download datagen.py: {e}")
    # Install uv if not present
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except Exception:
        # Try to install uv
        try:
            subprocess.run(["pip", "install", "uv"], check=True)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to install uv: {e}")
    # Run datagen.py with user_email
    try:
        result = subprocess.run(["python", datagen_path, user_email], capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run datagen.py: {e}")
