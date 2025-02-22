#!/bin/bash

if [ -d ".venv" ]; then
    echo ".venv уже существует, пропуск"
else
    python -m venv .venv
fi

source .venv/bin/activate && pip install fastapi