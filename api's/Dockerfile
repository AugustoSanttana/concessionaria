# Estágio 1: Estágio de construção (builder)
FROM python:3.12-slim as builder

WORKDIR /src

# Copia e instala as dependências Python em um ambiente virtual
COPY requirements.txt requirements.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Estágio 2: Estágio final
FROM python:3.12-slim

WORKDIR /src

# Copia o ambiente virtual do estágio de construção
COPY --from=builder /opt/venv /opt/venv

# Copia o código da aplicação
COPY . /src

# Configuração para rodar o Flask
# Adiciona o ambiente virtual ao PATH
ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]