"""
this is the entry point for the FastAPI application.
"""


from dotenv import load_dotenv
load_dotenv(override=True)
from fastapi import FastAPI, Response


########################################################
# Initialize the environment variables
########################################################
load_dotenv(override=True)


########################################################
# Initialize the FastAPI application
########################################################
app = FastAPI()

@app.get("/")
def health_check():
    return Response(status_code=200, content={"message": "OK"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)