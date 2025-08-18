FROM python:3.13.7-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y locales && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/'        /etc/locale.gen \
    && sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen 
COPY main.py requirements.txt /app/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "/app/main.py"]
