FROM continuumio/miniconda3
WORKDIR /app

# Install pkg-config and libmysqlclient-dev
RUN apt-get update && apt-get install -y pkg-config libmysqlclient-dev

COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "my_project_env", "/bin/bash", "-c"]

COPY . .

CMD ["conda", "run", "-n", "my_project_env", "python", "main.py"]