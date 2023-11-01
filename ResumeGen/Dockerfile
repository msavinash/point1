FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

ENV PORT 5000

WORKDIR $APP_HOME

VOLUME $APP_HOME

RUN apt-get update && apt-get install -y wkhtmltopdf

COPY . ./

# RUN echo $(fc-list) && sleep 10
RUN apt-get -y install fontconfig
COPY ./fonts ~/.fonts
COPY ./fonts /usr/shared/fonts
COPY ./fonts /usr/share/fonts/truetype
# refresh system font cache
RUN fc-cache -f -v
# RUN echo $(fc-list) && sleep 10
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app