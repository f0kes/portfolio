# Windows PowerShell helper to run frontend and backend locally
# Frontend runs in a separate window; backend runs in this window.
$ErrorActionPreference = "Stop"

# Start frontend dev server in a new PowerShell window
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd `"$PSScriptRoot/frontend`"; npm install; npm run dev -- --host --port 3000"

# Start backend API in this window
Push-Location "$PSScriptRoot/backend"
if (-not (Test-Path .venv)) {
    python -m venv .venv
}
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py # or: flask run --host 0.0.0.0 --port 8000 if that's your entrypoint
Pop-Location
