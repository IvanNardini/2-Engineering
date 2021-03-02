FROM tensorflow/tensorflow:2.4.1
WORKDIR usr/local/pipeline/components/prepare
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src .
ENTRYPOINT ["python", "src/component.py"]
