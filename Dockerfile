FROM mathworks/matlab:r2022a

ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt update && apt install -y \
    vim-gtk3

RUN cd /opt/matlab/R2022a/extern/engines/python && \
    python setup.py install && \
    cd -

USER matlab

# COPY . /predictmod


