# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster AS python_builder

ENV POETRY_VERSION 1.1.14

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PIP_NO_CACHE_DIR 1

ENV WORKDIR /app

WORKDIR ${WORKDIR}

RUN pip install "poetry==${POETRY_VERSION}"

ENV VIRTUAL_ENV /opt/venv
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY src src

RUN poetry build && pip install dist/*.whl

FROM python:3.10.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV VIRTUAL_ENV /opt/venv

ENV HOME /home/user
ENV APP_HOME ${HOME}/app

RUN mkdir -p ${HOME}

RUN groupadd -r user && \
    useradd -r -g user -d ${HOME} -s /sbin/nologin -c "Docker image user" user

RUN mkdir ${APP_HOME}

WORKDIR ${APP_HOME}

COPY --from=python_builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=python_builder /app/src ./src

ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"

RUN chown -R user:user ${HOME}

ARG PORT=8080
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["python -m", "src.run"]
