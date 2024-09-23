from fastapi import FastAPI, Request, HTTPException
from smuggle_shield_ai import SmuggleShieldAI


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/smuggle-shield/analyze-page")
async def analyze_page(request: Request):
    body = await request.json()
    page_source = body.get("page_source")

    if not page_source:
        raise HTTPException(status_code=400, detail="page_source is required")

    smuggle_shield = SmuggleShieldAI()

    result = smuggle_shield.analyze_page(page_source)

    return result


@app.post("/smuggle-shield/analyze-headers")
async def analyze_headers(request: Request):
    body = await request.json()
    headers = body.get("headers")

    if not headers:
        raise HTTPException(status_code=400, detail="headers is required")

    smuggle_shield = SmuggleShieldAI()

    result = smuggle_shield.analyze_headers(headers)

    return result
