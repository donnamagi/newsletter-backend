from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.process import ProcessService
import asyncio

router = APIRouter(prefix="/process", tags=["process"])

class ProcessingRequest(BaseModel):
  url: str

class ContentRequest(BaseModel):
  content: str

class SummaryRequest(BaseModel):
  summary: str

def get_process_service():
  return ProcessService()

@router.post("/")
async def get_all(request: ProcessingRequest, service: ProcessService = Depends(get_process_service)):

  content = await service.get_content(request.url)
  summary = await service.get_summary(content)

  keywords_task = asyncio.create_task(service.get_keywords(summary))
  embedding_task = asyncio.create_task(service.get_embedding(summary))
  keywords, embedding = await asyncio.gather(keywords_task, embedding_task)

  return {"summary": summary, "keywords": keywords, "embedding": embedding}

@router.post("/summary")
def get_summary(request: ContentRequest, service: ProcessService = Depends(get_process_service)):
  summary = service.get_summary(request.content)
  return {"summary": summary}

@router.post("/keywords")
def get_keywords(request: SummaryRequest, service: ProcessService = Depends(get_process_service)):
  keywords = service.get_keywords(request.summary)
  return {"keywords": keywords}

@router.post("/embedding")
def get_embedding(request: SummaryRequest, service: ProcessService = Depends(get_process_service)):
  embedding = service.get_embedding(request.summary)
  return {"embedding": embedding}
