cd frontend && npm install && npm run dev -- --host --port 3000
cd ..
cd backend && python -m venv .venv && .\.venv\Scripts\activate && pip install -r requirements.txt && python app.py (or flask run --host 0.0.0.0 --port 8000 
cd ..
