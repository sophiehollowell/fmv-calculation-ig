from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from typing import List
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
                width: 550px;
                text-align: center;
            }
            .row {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
                justify-content: center;
            }
            input[type=text], input[type=date], input[type=number] {
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                width: 150px;
            }
            button {
                padding: 8px 12px;
                border-radius: 6px;
                border: none;
                cursor: pointer;
            }
            .add-btn {
                background-color: #e5e7eb;
                margin-top: 10px;
            }
            .submit-btn {
                background-color: #6366f1;
                color: white;
                margin-top: 20px;
            }
            .submit-btn:hover {
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
            <img class="logo" src="https://media.licdn.com/dms/image/v2/D4E0BAQGbPCneStvFWA/company-logo_200_200/B4EZYVri5.GYAI-/0/1744120459243/infinite_giving_logo?e=2147483647&v=beta&t=jeA4JjajxPeOld2QDnroyVJ6x2EsrWeCz_9q17ZoQhk">
            <h1>FMV Calculator</h1>

            <form action="/fmv" method="post">
                <div id="rows">
                    <div class="row">
                        <input type="text" name="ticker" placeholder="Ticker (AAPL)">
                        <input type="date" name="date">
                        <input type="number" step="any" name="quantity" placeholder="Shares (e.g. 5)">
                    </div>
                </div>

                <button type="button" class="add-btn" onclick="addRow()">+ Add Row</button><br>
                <input type="submit" value="Calculate FMV" class="submit-btn">
            </form>
        </div>

        <script>
        function addRow() {
            const container = document.getElementById("rows");

            const div = document.createElement("div");
            div.className = "row";

            div.innerHTML = `
                <input type="text" name="ticker" placeholder="Ticker (AAPL)">
                <input type="date" name="date">
                <input type="number" step="any" name="quantity" placeholder="Shares (e.g. 5)">
                <button type="button" onclick="this.parentElement.remove()">Remove</button>
            `;

            container.appendChild(div);
        }
        </script>
    </body>
    </html>
    """

@app.post("/fmv", response_class=HTMLResponse)
def fmv_form(
    ticker: List[str] = Form(...),
    date: List[str] = Form(...),
    quantity: List[float] = Form(...)
):
    results = []

    for t, d, q in zip(ticker, date, quantity):
        if not t.strip() or not d.strip():
            results.append({
                "ticker": "Invalid",
                "date_used": d,
                "high": "-",
                "low": "-",
                "fmv": "Missing Input",
                "quantity": q or "-",
                "total_value": "-"
            })
            continue

        try:
            q_val = float(q) if q else 0
        except:
            q_val = 0

        result = get_fmv(t, d, q_val)

        if result:
            results.append(result)
        else:
            results.append({
                "ticker": t.upper(),
                "date_used": d,
                "high": "N/A",
                "low": "N/A",
                "fmv": "No Data",
                "quantity": q_val,
                "total_value": "No Data"
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
            <td>{r['quantity']}</td>
            <td>{r['total_value'] if r['total_value'] is not None else '-'}</td>
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
                width: 800px;
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
                    <th>Quantity</th>
                    <th>Tax Deductible Amount</th>
                </tr>
                {table_rows}
            </table>
            <br>
            <a href="/">Calculate Another</a>
        </div>
    </body>
    </html>
    """
