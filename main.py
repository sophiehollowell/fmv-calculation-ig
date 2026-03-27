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
                <textarea name="bulk_input" rows="6" style="width: 90%;" placeholder="Enter one per line:&#10;AAPL, 2024-03-01&#10;TSLA, 2024-03-02"></textarea><br>
                <input type="submit" value="Calculate FMV">
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/fmv", response_class=HTMLResponse)
def fmv_form(bulk_input: str = Form(...)):
    
    if not bulk_input.strip():
        return """
        <html>
            <body style="font-family: Helvetica; text-align:center; padding:50px;">
                <h3>No input provided.</h3>
                <p>Please enter at least one ticker and date.</p>
                <a href="/">Calculate Another</a>
            </body>
        </html>
        """

    rows = bulk_input.strip().split("\n")
    results = []

    for row in rows:
        try:
            ticker, date = [x.strip() for x in row.split(",")]
            result = get_fmv(ticker, date)

            if result:
                results.append(result)
            else:
                results.append({
                    "ticker": ticker.upper(),
                    "date_used": date,
                    "high": "N/A",
                    "low": "N/A",
                    "fmv": "No Data"
                })
        except:
            results.append({
                "ticker": "Invalid",
                "date_used": row,
                "high": "-",
                "low": "-",
                "fmv": "Formatting Error"
            })

    table_rows = ""
    for r in results:
        table_rows += f"""
        <tr>
            <td>{r['ticker']}</td>
            <td>{r['date_used']}</td>
            <td>{r['high']}</td>
            <td>{r['low']}</td>
            <td>{r['fmv']}</td>
        </tr>
        """
        
    return f"""
    <html>
        <head>
            <title>FMV Results</title>
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
                    width: 700px;
                    text-align: center;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background-color: #4f46e5;
                    color: white;
                }}
                a {{
                    color: #6366f1;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>FMV Results</h2>
                <table>
                    <tr>
                        <th>Ticker</th>
                        <th>Date Used</th>
                        <th>High</th>
                        <th>Low</th>
                        <th>FMV</th>
                    </tr>
                    {table_rows}
                </table>
                <br>
                <a href="/">Calculate Another</a>
            </div>
        </body>
    </html>
    """
