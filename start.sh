#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/instance/WILPS-fbd52af604db.json"

flask run --host=127.0.0.1 --port=8132