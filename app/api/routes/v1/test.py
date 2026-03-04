from fastapi import APIRouter
from app.db import get_vector_store
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/api/v1/test")

@router.get("/")
async def test():
    try:
        collection = next(get_vector_store(collection_name="test"))
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