FROM python:3.12

WORKDIR /backend

COPY ./backend/requirements.txt \
    ./backend/pyproject.toml \
    ./backend/poetry.lock /backend/

RUN apt-get update && apt-get install -y \
    mc \
    supervisor \
    curl \
    bash \
    nano \
    systemd \
    && apt-get install -y systemctl \
    && rm -rf /var/lib/apt/lists/*


RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && pip install poetry \
    && rm -rf /var/cache/apt \
    && poetry export --without-hashes -f requirements.txt --output requirements.txt \
    && pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

#RUN curl -sSL https://install.python-poetry.org | python3 -

#COPY ./backend/pyproject.toml /app/
#COPY ./backend/poetry.lock /app/

#RUN pip install poetry && rm -rf /var/cache/apt

#RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

#RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
#    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV TZ = Europa/Moscow

#RUN mkdir -p /var/log/fastapi_server

COPY /docker/supervisor/supervisord.conf /etc/supervisord.conf

CMD ["timedatectl", "set-timezone", "Europe/Moscow"]
CMD ["/usr/bin/supervisord", "-n", "-c",  "/etc/supervisord.conf"]
