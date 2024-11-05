FROM python:3.13.0-bookworm
WORKDIR /app
COPY main.py requirements.txt /app/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "/app/main.py"]
