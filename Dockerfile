# syntax=docker/dockerfile:1.6
############################
#        BUILDER
############################
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    python3-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel packaging
# Build wheels (multi-arch safe) - setuptools et wheel inclus dans les wheels
RUN pip wheel --no-cache-dir --wheel-dir /wheels setuptools wheel packaging && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

############################
#        RUNTIME
############################
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG user=enroller
ARG group=enroller
ARG ENVIRONMENT=develop # develop / prod
ARG GIT_SHA=unknown
ARG GIT_BRANCH=unknown
LABEL git.sha=$GIT_SHA git.branch=$GIT_BRANCH
ENV uid=1000
ENV gid=1000
# Runtime libs uniquement
RUN apt-get update && apt-get install -y \
    libffi8 \
    && rm -rf /var/lib/apt/lists/*
RUN if [ "$ENVIRONMENT" = "prod" ]; then \
      groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /usr/sbin/nologin ${user}; \
    else \
      groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}; \
    fi
WORKDIR /app
COPY --from=builder /wheels /wheels
# Installer setuptools en premier pour fournir distutils et pkg_resources
RUN pip install --no-cache-dir setuptools>=69.0.0 \
    && pip install --no-cache-dir /wheels/* \
    && pip install --no-cache-dir --force-reinstall setuptools>=69.0.0 

COPY . .
RUN chown -R ${user}:${group} /app
USER ${user}
ENTRYPOINT ["python", "run_enroller.py"]