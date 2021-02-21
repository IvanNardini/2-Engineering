FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY prepare.py .
ENTRYPOINT ["python", "store_data_v2.py"]