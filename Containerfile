FROM python:3.10
RUN useradd -m -u 1000 user
WORKDIR /locallm
COPY requirements.txt /locallm/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /locallm/requirements.txt
USER user
COPY --chown=1000 ./ /locallm