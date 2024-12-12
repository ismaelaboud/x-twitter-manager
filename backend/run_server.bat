@echo on
call venv\Scripts\activate
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
