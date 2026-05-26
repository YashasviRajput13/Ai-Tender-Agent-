FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/analysis_service /app/services/analysis_service
EXPOSE 8003
CMD ["uvicorn", "services.analysis_service.main:app", "--host", "0.0.0.0", "--port", "8003"]
