FROM python:3.11 AS builder

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.1 && poetry build


FROM python:3.11 AS runtime

COPY --from=builder /app/dist/frikibot-0.1.0.tar.gz /build/

WORKDIR /build

RUN pip install --no-cache-dir frikibot-0.1.0.tar.gz

WORKDIR /app

CMD [ "python", "-m", "frikibot" ]
