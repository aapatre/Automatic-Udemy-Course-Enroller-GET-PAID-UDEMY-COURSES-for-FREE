FROM python:3.12-slim

ARG user=enroller
ARG group=enroller
ENV uid=1000
ENV gid=1000

# RUN addgroup --gid 1000 enroller && adduser -uid 1000 enroller enroller
RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}
# RUN mkdir -p /home/${user}/.udemy_enroller /src  && chown ${user} /home/${user} /home/${user}/.udemy_enroller /src 
RUN mkdir -p /home/${user}/.udemy_enroller  && chown ${user} /home/${user}/.udemy_enroller 

WORKDIR /src
COPY . . 
RUN pip install --no-cache-dir -r requirements.txt

USER ${user}
ENTRYPOINT [ "python", "run_enroller.py" ]
