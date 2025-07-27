FROM python:3.12-bookworm
WORKDIR /app
COPY . .
RUN pip install uv && uv pip install --system . && pip install pyyaml
CMD ["python", "-m", "glyphd", "serve", "--host", "0.0.0.0", "--port", "8000", "--reload"]
