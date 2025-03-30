FROM python AS builder

WORKDIR /usr/src/app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY . .
RUN pip install .
RUN pip install -r extra_req.txt


FROM python AS test_runner
WORKDIR /tmp
COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app/tests tests
ENV PATH=/venv/bin:$PATH

# install test dependencies
RUN pip install pytest

# run tests
RUN pytest tests


FROM python AS service
WORKDIR /root/app/site-packages
COPY --from=test_runner /venv /venv
ENV PATH=/venv/bin:$PATH
