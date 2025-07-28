FROM python:3.12-bookworm
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y curl \
    && pip install uv && uv pip install --system .
EXPOSE 8000
CMD ["python", "-m", "glyphd", "serve", "--host", "0.0.0.0", "--port", "8000", "--reload"]
