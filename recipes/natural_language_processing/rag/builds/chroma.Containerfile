# This Container file gets run from the root dir because it uses /data 
FROM docker.io/chromadb/chroma:0.4.25.dev109
WORKDIR /rag
COPY recipes/natural_language_processing/rag/requirements.txt .
COPY data /data
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /rag/requirements.txt
COPY populate_vectordb.py rag_app.py .
EXPOSE 8000
ENTRYPOINT ["/docker_entrypoint.sh"]
RUN python3 populate_vectordb.py
