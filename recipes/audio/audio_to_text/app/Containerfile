FROM registry.access.redhat.com/ubi9/python-311:1-77.1725907703
WORKDIR /locallm
COPY requirements.txt /locallm/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt
COPY whisper_client.py whisper_client.py
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "whisper_client.py" ]
