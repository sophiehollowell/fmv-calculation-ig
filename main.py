from fastapi import FastAPI
from fmv_functions import get_fmv

app = FastAPI(title="FMV API")

@app.get("/")
def root():
    return {"message": "FMV API is running"}

@app.get("/fmv")
def fmv_api(ticker: str, date: str):
    """
    Example call: /fmv?ticker=AAPL&date=2024-03-01
    """
    result = get_fmv(ticker, date)
    if not result:
        return {"error": "No data found or invalid ticker/date"}
    return result