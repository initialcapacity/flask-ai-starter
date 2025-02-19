FROM python:3.12

WORKDIR /apps
COPY ./starter ./starter
COPY ./requirements.txt ./requirements.txt
COPY ./bin/app.sh ./app.sh
COPY ./bin/collect.sh ./collect.sh
COPY ./bin/analyze.sh ./analyze.sh
RUN pip install -r requirements.txt
CMD [ "./app.sh" ]
