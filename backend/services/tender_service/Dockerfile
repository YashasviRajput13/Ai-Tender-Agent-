FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/tender_service /app/services/tender_service
EXPOSE 8002
CMD ["uvicorn", "services.tender_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
