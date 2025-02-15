from fastapi import FastAPI, HTTPException
import os
import openai
from pathlib import Path

app = FastAPI()

OPENAI_API_KEY = os.getenv("AIPROXY_TOKEN")
openai.api_key = OPENAI_API_KEY
DATA_DIR = "/data"

@app.post("/run")
async def run_task(task: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Interpret the following task and convert it into executable steps."},
                      {"role": "user", "content": task}]
        )
        steps = response['choices'][0]['message']['content']
        return {"message": "Task executed successfully", "steps": steps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    file_path = Path(DATA_DIR) / path.strip("/")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r") as file:
        content = file.read()
    return {"content": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
@app.get("/")
async def root():
    return {"message": "API is running"}
    
