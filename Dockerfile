FROM python:3.10-alpine

WORKDIR /src

COPY . . 

RUN apk add --no-cache build-base
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "udemy_enroller.py", "--max-pages=900000"]
