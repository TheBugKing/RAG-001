from fastapi import APIRouter, BackgroundTasks
from app.db import get_vector_store
from fastapi.responses import JSONResponse
import asyncio

router = APIRouter(prefix="/api/v1/test")

@router.get("/")
async def test():
    try:
        collection = get_vector_store(collection_name="test")
        collection.insert(
            ids=["1"],
            embeddings=[[0.1, 0.2, 0.3]],
            metadatas=[{"name": "test", "document_id": "1"}],
            documents=["test"],
        )
        result = collection.get(
            ids=["1"],
        )
        result["embeddings"] = result["embeddings"].tolist()
        print(result)
        return JSONResponse(content={"message": result})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=500)

def run_indexing_job() -> None:
    for i in range(9000):
        print(i)
        asyncio.sleep(200)

@router.post("/background")
def index_background(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_indexing_job)
    return {"status": "queued"}