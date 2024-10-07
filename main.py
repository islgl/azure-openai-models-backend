import os

from fastapi import FastAPI, HTTPException
from typing import Optional
from crawler import get_latest_version
from api_response import ApiResponse
from models import fetch_available_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 设置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名的跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（GET, POST, PUT, OPTIONS 等）
    allow_headers=["*"],  # 允许所有头部
)


@app.get("/api/versions", response_model=ApiResponse)
async def get_api_versions():
    url = 'https://learn.microsoft.com/en-us/azure/ai-services/openai/reference'
    data = {}
    try:
        data = get_latest_version(url)
        return ApiResponse.success(code=200, data=data, message='Successfully fetched Azure OpenAI API versions')
    except HTTPException as e:
        return ApiResponse.failure(code=e.status_code, message=str(e), data=data)
    except Exception as e:
        return ApiResponse.failure(code=500, message=str(e), data=data)


@app.get("/api/models", response_model=ApiResponse)
async def get_models(api_version: Optional[str] = None):
    data = []

    if api_version is None:
        return ApiResponse.failure(code=400, message='The api version cannot be empty', data=data)

    azure_openai_api_url = os.getenv('AZURE_OPENAI_API_URL')
    azure_openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')

    if not azure_openai_api_url or not azure_openai_api_key:
        return ApiResponse.failure(code=500, message='The Azure OpenAI API URL or API key is not set', data=data)

    try:
        data = fetch_available_models(azure_openai_api_url, api_version, azure_openai_api_key)
        return ApiResponse.success(code=200, data=data, message='Successfully fetched available Azure OpenAI models')
    except HTTPException as e:
        return ApiResponse.failure(code=e.status_code, message=str(e), data=data)
    except Exception as e:
        return ApiResponse.failure(code=500, message=str(e), data=data)
