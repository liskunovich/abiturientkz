FROM python:3.10-slim-buster as python-base
LABEL authors="lskdavid"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/pysetup/.venv/bin:$PATH"

RUN apt-get update
RUN apt-get install --no-install-recommends -y build-essential

WORKDIR /opt/pysetup

RUN pip3 install poetry

COPY pyproject.toml ./

RUN poetry install --only main

FROM python:3.10-slim-buster
ENV PATH="/opt/pysetup/.venv/bin:$PATH"

COPY --from=python-base /opt/pysetup/ /opt/pysetup/
COPY ./abiturient /abiturient

WORKDIR ./

CMD ["python3", "-m", "abiturient"]