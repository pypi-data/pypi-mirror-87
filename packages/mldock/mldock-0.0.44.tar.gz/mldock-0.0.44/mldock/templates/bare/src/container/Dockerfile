FROM python:3.7-slim-buster
LABEL maintainer="sheldon sgwilliams2718@gmail.com"
SHELL ["/bin/bash", "-c"]
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         nginx \
         ca-certificates \
         g++ \
         git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-dev build-essential && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root
# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /root/tools/google-cloud-sdk/.install/.backup

# Path configuration
ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
# Make sure gsutil will use the default service account
RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

# PYTHONUNBUFFERED keeps Python from buffering the standard
# output stream, which means that logs can be delivered to the user quickly. 
# PYTHONDONTWRITEBYTECODE keeps Python from writing the .pyc files which are unnecessary in this case. 

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
# ENV PATH="/opt/program:${PATH}"

ARG requirements_file_path
ARG module_path
ARG target_dir_name

WORKDIR /opt/program/

# Here we get all python packages.
RUN pip install flask gevent gunicorn future mldock[ai-platform]

# install project specfic requirements
COPY ${requirements_file_path} /opt/program/sagify-requirements.txt
RUN pip install -r sagify-requirements.txt && rm -rf /root/.cache
RUN apt-get -y purge --auto-remove git

COPY ${module_path}/trainer.py /opt/program/${target_dir_name}/trainer.py
COPY ${module_path}/prediction.py /opt/program/${target_dir_name}/prediction.py
COPY ${module_path}/env.py /opt/program/${target_dir_name}/env.py
COPY ${module_path}/container/prediction /opt/program/${target_dir_name}/container/prediction
COPY ${module_path}/container/training /opt/program/${target_dir_name}/container/training

ENTRYPOINT ["src/container/prediction/executor.sh"]
CMD python src/container/prediction/serve.py
