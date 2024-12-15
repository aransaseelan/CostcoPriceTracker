FROM python:3.11.6

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app/database.py", "--server.port=8501", "--server.address=0.0.0.0"]
