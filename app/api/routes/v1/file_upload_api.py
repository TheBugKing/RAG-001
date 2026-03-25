from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/file")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        print(file_content[:1000])
        file.filename = file.filename.encode("utf-8").decode("utf-8")
        
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=500)


