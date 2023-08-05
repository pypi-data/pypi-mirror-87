FROM python:3.6-slim-stretch

LABEL maintainer="SDC <sdc@ringier.com>"

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         nginx \
         ca-certificates \
         g++ \
         git \
    && rm -rf /var/lib/apt/lists/*

# PYTHONUNBUFFERED keeps Python from buffering the standard
# output stream, which means that logs can be delivered to the user quickly. 
# PYTHONDONTWRITEBYTECODE keeps Python from writing the .pyc files which are unnecessary in this case. 

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

ARG requirements_file_path
ARG module_path
ARG target_dir_name

COPY ${requirements_file_path} /opt/program/sagify-requirements.txt
WORKDIR /opt/program/${target_dir_name}

# Here we get all python packages.
RUN pip install flask gevent gunicorn future sagemaker-training
RUN pip install -r ../sagify-requirements.txt && rm -rf /root/.cache
RUN apt-get -y purge --auto-remove git

COPY ${module_path}/trainer.py /opt/program/${target_dir_name}/trainer.py
COPY ${module_path}/prediction.py /opt/program/${target_dir_name}/prediction.py
COPY ${module_path}/container/executor.sh /opt/program/${target_dir_name}/container/executor.sh
COPY ${module_path}/container/prediction /opt/program/${target_dir_name}/container/prediction
COPY ${module_path}/container/training /opt/program/${target_dir_name}/container/training

ENTRYPOINT ["container/executor.sh"]
