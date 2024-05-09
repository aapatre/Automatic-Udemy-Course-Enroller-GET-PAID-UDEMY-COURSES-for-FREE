FROM python:3.12-slim

#apt-get update && apt-get install -y \
#    build-base \
#    && rm -rf /var/lib/apt/lists/*  
# libffi-dev

RUN addgroup -S enroller && adduser -S enroller -G enroller
USER enroller

RUN mkdir -p ~/.udemy_enroller

WORKDIR /src

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "run_enroller.py" ]
