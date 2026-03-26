from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fmv_functions import get_fmv

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>Infinite Giving FMV Calculator</title>
        <style>
            body {
                font-family: 'Helvetica', sans-serif;
                background-color: #f9fafb;
                color: #111827;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 50px;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                width: 400px;
                text-align: center;
            }
            input[type=text], input[type=date] {
                width: 80%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 6px;
                border: 1px solid #d1d5db;
            }
            input[type=submit] {
                background-color: #6366f1;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                margin-top: 10px;
            }
            input[type=submit]:hover {
                background-color: #4f46e5;
            }
            h1 {
                color: #4f46e5;
                margin-bottom: 20px;
            }
            .logo {
                width: 120px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img class="logo" src="https://media.licdn.com/dms/image/v2/D4E0BAQGbPCneStvFWA/company-logo_200_200/B4EZYVri5.GYAI-/0/1744120459243/infinite_giving_logo?e=2147483647&v=beta&t=jeA4JjajxPeOld2QDnroyVJ6x2EsrWeCz_9q17ZoQhk" alt="Infinite Giving Logo">
            <h1>FMV Calculator</h1>
            <form action="/fmv" method="post">
                <input type="text" name="ticker" placeholder="Enter Ticker (e.g. AAPL)"><br>
                <input type="date" name="date"><br>
                <input type="submit" value="Calculate FMV">
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/fmv", response_class=HTMLResponse)
def fmv_form(ticker: str = Form(...), date: str = Form(...)):
    result = get_fmv(ticker, date)
    if not result:
        return f"""
        <html>
            <body style="font-family: Helvetica, sans-serif; background-color:#f9fafb; display:flex; justify-content:center; padding:50px;">
                <div style="background-color:white; padding:40px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.1); width:400px; text-align:center;">
                    <h2 style="color:#4f46e5;">No Data Found</h2>
                    <p>No FMV data available for {ticker.upper()} on {date}. Please check your ticker and date.</p>
                    <a href="/" style="color:#6366f1; text-decoration:none;">Calculate Another</a>
                </div>
            </body>
        </html>
        """
    
    return f"""
    <html>
        <head>
            <title>FMV Result</title>
            <style>
                body {{
                    font-family: 'Helvetica', sans-serif;
                    background-color: #f9fafb;
                    display: flex;
                    justify-content: center;
                    padding: 50px;
                }}
                .container {{
                    background-color: white;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    width: 400px;
                    text-align: center;
                }}
                h2 {{
                    color: #4f46e5;
                }}
                a {{
                    color: #6366f1;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>FMV Result</h2>
                <p><b>Ticker:</b> {result['ticker']}</p>
                <p><b>Date Used:</b> {result['date_used']}</p>
                <p><b>High:</b> {result['high']}</p>
                <p><b>Low:</b> {result['low']}</p>
                <p><b>FMV:</b> {result['fmv']}</p>
                <br>
                <a href="/">Calculate Another</a>
            </div>
        </body>
    </html>
    """
