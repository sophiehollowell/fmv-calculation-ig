# fmv-calculation-ig
Fair Market Value Calculation Tool for Infinite Giving. This tool calculates the Fair Market Value (FMV) and summarize information of publicly traded securities using data from Yahoo finance. The goal was to streamline the need to research historical data for specific tickers and manually derive needed information. Users can input one or two stocks (ticker, date, and quantity), and the tool returns:
* Stock ticker
* Trading date
* High price
* Low price
* Fair market value (FMV)
* Quantity
* Tax Deductible Amount (Quantity x FMV)

## Features
* Supports multiple tickers at once
* Automatically adjusts to the next trading day (weekends & holidays)
* Accepts fractional shares
* Calculates FMV and total tax deductible amount

## Tech Stack
* Python
* FastAPI
* yfinance
* HTML/CSS/JS

# Quick Start
### Prerequisites
* Python 3.9+ insalled
* pip (Python package manager)
* A code editor (VS Code, IntelliJ, etc.)
* Basic familiarity with running commands in PowerShell/terminal

### Installations
```
## Clone the repository
git clone https://github.com/sophiehollowell/fmv-calculation-ig.git
cd fmv-calculation-ig

## Create virtual environment (manage dependencies)
python -m venv .venv

## Activate venv
.venv\Scripts\activate.ps1 # Windows
### If this fails on Windows, you may need to allow scripts in terminal with the following line: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

source .venv/bin/activate # Mac/Linux

## Install dependences
pip install -r requirements.txt

## Run the app
uvicorn main:app --reload

## Open app in browser
http://127.0.0.1:8000

## Repository Structure
fmv-calculation-ig/
│
├── main.py            # FastAPI app (UI + endpoints)
├── fmv_functions.py   # FMV calculation logic
├── requirements.txt   # Dependencies
└── README.md
```
### Deployment
This app can be deployed using platforms like:
* Render
* Replit
* Railway

Once deployed, the tool can be shared via URL!
