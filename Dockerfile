FROM locustio/locust
USER root
RUN pip3 install pandas
RUN pip3 install requests
RUN pip3 install pyyaml

