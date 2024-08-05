FROM registry.access.redhat.com/ubi9/python-311:1-72.1722518949
WORKDIR /chat
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /chat/requirements.txt
COPY chatbot_ui.py .
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "chatbot_ui.py" ]
