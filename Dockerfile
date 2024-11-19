FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit

COPY ABA_Framework/ .

EXPOSE 8501

CMD ["streamlit", "run", "💻_ABA_Generator.py", "--server.port=8501", "--server.address=0.0.0.0"]
