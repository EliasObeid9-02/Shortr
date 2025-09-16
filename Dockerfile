FROM python:3.13.7-alpine3.21 AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /app
WORKDIR /app
RUN uv sync --locked

# Expose the port the app runs on
EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh" ]
