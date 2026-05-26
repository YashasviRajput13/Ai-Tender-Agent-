FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY fastapi_gateway /app/fastapi_gateway
EXPOSE 8000
CMD ["uvicorn", "fastapi_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
