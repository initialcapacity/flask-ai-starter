#!/usr/bin/env bash

gunicorn -w 4 'starter.app:create_app()' --bind=0.0.0.0:${PORT}
