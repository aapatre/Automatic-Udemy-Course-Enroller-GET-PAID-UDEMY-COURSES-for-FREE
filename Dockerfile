FROM python:3.11-alpine

RUN apk add --no-cache build-base libffi-dev

RUN addgroup -S enroller && adduser -S enroller -G enroller
USER enroller
RUN mkdir -p ~/.udemy_enroller

WORKDIR /src

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "run_enroller.py" ]
