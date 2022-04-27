FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt update

COPY ./requirements/base.txt /base.txt
COPY ./requirements/local.txt /local.txt
RUN pip install -r local.txt

RUN pip install -i https://mirrors.aliyun.com/pypi/simple redis flower


WORKDIR /code


COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


ENTRYPOINT ["/entrypoint"]