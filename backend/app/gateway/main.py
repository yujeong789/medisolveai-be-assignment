from fastapi import FastAPI

app = FastAPI(title="Medisolve Gateway API")

@app.get("/")
def test_connection():
    return {"message": "This is Gateway API documentation."}