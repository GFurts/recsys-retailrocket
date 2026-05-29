# ================================
# Stage 1: builder
# ================================
FROM python:3.10-slim AS builder

WORKDIR /app

RUN pip install poetry==2.4.1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root

# ================================
# Stage 2: runtime
# ================================
FROM python:3.10-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

COPY src/ ./src/
COPY configs/ ./configs/
COPY dvc.yaml ./
COPY .env.example ./.env.example
COPY start.sh ./
RUN chmod +x start.sh

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

CMD ["sh", "start.sh"]