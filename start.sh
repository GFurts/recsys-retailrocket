#!/bin/bash
uvicorn recsys.api:app --host 0.0.0.0 --port $PORT