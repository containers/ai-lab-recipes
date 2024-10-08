FROM registry.access.redhat.com/ubi9/python-311:1-77.1726664316
WORKDIR /locallm
COPY requirements.txt /locallm/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt
COPY object_detection_client.py object_detection_client.py
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "object_detection_client.py" ]
