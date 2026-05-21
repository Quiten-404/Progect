from fastapi import FastAPI
app = FastAPI()

@app.get("/test")
def test():
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
    