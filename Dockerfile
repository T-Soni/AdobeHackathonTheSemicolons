# Use amd64 platform for compatibility
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory (creates /app)
WORKDIR /app

# Copy the script into the container
COPY process_pdfs.py .

# Install dependencies
RUN pip install pymupdf

# Create default folders inside image (will be overwritten by volume mounts when run)
RUN mkdir -p input output

CMD ["python", "process_pdfs.py"]
