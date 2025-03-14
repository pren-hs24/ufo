FROM python:3.13-alpine

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

COPY src/ /src
WORKDIR /src

CMD ["python3", "main.py"]
