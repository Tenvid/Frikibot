FROM python:3.11 AS builder

COPY . /app

WORKDIR /app

RUN pip install poetry

RUN poetry build

FROM python:3.11 AS runtime

COPY --from=builder /app/dist/frikibot-0.1.0.tar.gz /build/

WORKDIR /build

RUN pip install frikibot-0.1.0.tar.gz

WORKDIR /app

CMD python -m frikibot