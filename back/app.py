from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def generate_poem():
    return {"poem": "Roses are red, violets are blue, this is a placeholder poem, just for you!"}



# poetry run uvicorn app:app --port 5000 --reload