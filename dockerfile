FROM python:3.11.4
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
WORKDIR /app
COPY ./src /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]