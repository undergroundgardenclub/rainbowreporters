from fastapi import FastAPI
import os
import json
import uvicorn
import os

app = FastAPI()

@app.get("/")
def read_root():
  return "howdy"

@app.get("/data/listdir")
def read_json():
  data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
  data_files = os.listdir(data_dir)
  return data_files

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=3000)
