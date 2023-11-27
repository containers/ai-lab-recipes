FROM python:3.10
RUN useradd -m -u 1000 user
WORKDIR /locallm
COPY requirements.txt /locallm/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /locallm/requirements.txt
USER user
ENV MODEL_FILE=llama-2-7b-chat.Q5_K_S.gguf
COPY --chown=1000 ./ /locallm
ENTRYPOINT [ "python", "app.py" ]