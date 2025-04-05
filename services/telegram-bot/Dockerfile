FROM python AS builder

WORKDIR /usr/src/app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY /services/telegram-bot .
RUN pip install --no-cache-dir .
RUN pip install -r extra_req.txt


FROM python AS test_runner
WORKDIR /tmp
COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app/tests tests
ENV PATH=/venv/bin:$PATH

# install test dependencies
RUN pip install pytest

RUN mkdir -p /tmp/.mongodb && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
    --output-document /tmp/.mongodb/root.crt && \
    chmod 0644 /tmp/.mongodb/root.crt
# run tests
RUN pytest tests


FROM python AS service

WORKDIR /root/app/site-packages
COPY --from=test_runner /tmp/.mongodb /root/app/site-packages/.mongodb
COPY --from=test_runner /venv /venv
ENV PATH=/venv/bin:$PATH