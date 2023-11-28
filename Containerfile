FROM python:3.10
WORKDIR /locallm
COPY requirements.txt /locallm/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /locallm/requirements.txt
ENV MODEL_FILE=llama-2-7b-chat.Q5_K_S.gguf
COPY ./ /locallm
ENTRYPOINT [ "python", "app.py" ]