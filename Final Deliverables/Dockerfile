FROM python:3.7-alpine
LABEL maintainer="susanthika m, susanthika02m@gmail.com"
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
WORKDIR /docker-plasma app
