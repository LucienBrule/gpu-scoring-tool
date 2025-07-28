FROM python:3.12-bookworm
WORKDIR /app

# Copy the entire monorepo context
COPY glyphsieve ./glyphsieve
COPY glyphd ./glyphd

# Install glyphsieve first so it's available as a dependency
WORKDIR /app/glyphsieve
RUN pip install uv && uv pip install --system .

# Then install glyphd which depends on glyphsieve
WORKDIR /app/glyphd
RUN uv pip install --system .

EXPOSE 8080
CMD ["uvicorn", "glyphd.api.router:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
