FROM python:3.12.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 8500/tcp

COPY ./overkiz_exporter.py .

ENTRYPOINT ["python", "./overkiz_exporter.py"]