FROM python:3.12-slim

#apt-get update && apt-get install -y \
#    build-base \
#    && rm -rf /var/lib/apt/lists/*  
# libffi-dev
ARG user=enroller
ARG group=enroller
ARG uid=1000
ARG gid=1000

# RUN addgroup --gid 1000 enroller && adduser -uid 1000 enroller enroller
RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}
RUN mkdir -p ~/.udemy_enroller && chown ${user} ~/.udemy_enroller

USER ${user}
WORKDIR /src

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "run_enroller.py" ]
