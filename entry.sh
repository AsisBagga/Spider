#!/bin/bash
redis-server --daemonize yes && python manage.py runserver 0.0.0.0:8000