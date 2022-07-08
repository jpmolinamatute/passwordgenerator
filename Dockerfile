FROM python:3.10.0-alpine3.15

ARG SECRET_USER="secret"
ARG SECRET_HOME="/opt/${SECRET_USER}"

ENV LENGTH="20"
ENV MIN_PATTER="1"
ENV SPECIAL_CHAR="!\"#$&'()*+,-./:;<=>?@[\\]^_`{|}~%"
RUN apk update\
    && apk upgrade\
    && pip install --upgrade pip\
    && pip install pipenv\
    && adduser -h "${SECRET_HOME}" -S -G nogroup "${SECRET_USER}"
COPY --chown=${SECRET_USER}:nogroup ./Pipfile ./Pipfile.lock ./password/ ./run.py ${SECRET_HOME}/

RUN cd ${SECRET_HOME}\
    && pipenv install --system --deploy

USER ${SECRET_USER}
WORKDIR ${SECRET_HOME}
ENTRYPOINT ./run.py -l "${LENGTH}" -m "${MIN_PATTER}" -p "${SPECIAL_CHAR}"
