#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn app.main:app --reload 