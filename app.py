from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import pandas as pd
import uuid
import os

app = FastAPI()

# dummy models
MODELS = [
    {"modelId": "1", "modelName": "DEV_Model"},
    {"modelId": "2", "modelName": "UAT_Model"},
    {"modelId": "3", "modelName": "PROD_Model"}
]


@app.get("/models")
def get_models():
    return MODELS


@app.post("/compare")
def compare_models(payload: dict, request: Request):
    source = payload.get("sourceModelId")
    target = payload.get("targetModelId")

    # dummy comparison data
    data = [
        {
            "Object": "Module",
            "Name": "Sales",
            "Source": "Exists",
            "Target": "Modified"
        },
        {
            "Object": "List",
            "Name": "Region",
            "Source": "Exists",
            "Target": "Missing"
        }
    ]

    df = pd.DataFrame(data)

    # generate unique file name
    file_id = str(uuid.uuid4())
    file_name = f"comparison_{file_id}.xlsx"
    file_path = os.path.join(".", file_name)

    df.to_excel(file_path, index=False)

    # dynamic URL (works on localhost and Render)
    file_url = str(request.base_url) + f"download/{file_name}"

    return {
        "status": "success",
        "fileUrl": file_url
    }


@app.get("/download/{file_name}")
def download_file(file_name: str):
    file_path = os.path.join(".", file_name)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
