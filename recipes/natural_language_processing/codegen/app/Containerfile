FROM registry.access.redhat.com/ubi9/python-311:1-77.1726664316
WORKDIR /codegen
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /codegen/requirements.txt
COPY codegen-app.py .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "codegen-app.py"]
