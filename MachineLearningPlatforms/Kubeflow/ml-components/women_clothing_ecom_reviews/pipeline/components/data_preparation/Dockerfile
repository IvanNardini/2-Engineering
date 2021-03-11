FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY component .
EXPOSE 9090
ENTRYPOINT [ "python", "./run_prepare.py" ]