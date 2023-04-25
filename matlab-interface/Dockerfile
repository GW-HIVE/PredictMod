FROM mathworks/matlab:r2022a

USER root

WORKDIR /opt/matlab/R2022a/extern/engines/python/

RUN pip install . && pip install flask

USER matlab

ENV MLM_LICENSE_FILE 27000@fb-lic-p06.ead.gwu.edu
ENV MATLAB_SERVER_MODE docker

COPY . /matlab-interface
WORKDIR /matlab-interface


