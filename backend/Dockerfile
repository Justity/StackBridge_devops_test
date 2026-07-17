# Official slim base image, pinned version (no `latest`)
FROM python:3.12-alpine

WORKDIR /app

COPY app.py .

# Run as an unprivileged user instead of root
RUN adduser -D -H appuser
USER appuser

# Documentation only: the port is reachable inside the docker network,
# it is NOT published to the host
EXPOSE 8080

CMD ["python", "app.py"]
