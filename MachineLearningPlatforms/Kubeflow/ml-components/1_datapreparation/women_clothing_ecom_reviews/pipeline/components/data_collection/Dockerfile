FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY kaggle.json /root/.kaggle/
RUN chmod 600 /root/.kaggle/kaggle.json
COPY . .
EXPOSE 9090
CMD [ "python", "./run_collect.py" ]