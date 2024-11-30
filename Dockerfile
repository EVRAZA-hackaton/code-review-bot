FROM python:3.11-slim AS builder

WORKDIR /tmp
RUN pip install pipenv
COPY Pipfile Pipfile.lock /tmp/
RUN pipenv requirements > requirements.txt
RUN pipenv requirements --dev > dev-requirements.txt


FROM python:3.11-slim AS deploy

WORKDIR /backend
COPY --from=builder /tmp/requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY ./app /backend/app

RUN useradd nonroot
USER nonroot
CMD ["python", "-m", "app"]