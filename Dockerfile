# from: https://images.chainguard.dev/directory/image/python/overview
FROM cgr.dev/chainguard/python:latest-dev as dev
WORKDIR /app
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM cgr.dev/chainguard/python:latest
WORKDIR /app
COPY main.py main.py
COPY --from=dev /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENTRYPOINT ["python", "-u", "main.py"]
