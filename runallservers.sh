#!/bin/bash

python manage.py runserver &
python manage.py celeryd -B -l INFO &
