source env/bin/activate
DJANGO_SETTINGS_MODULE=elecprog.settings_dev
SECRET_KEY='!r3j&l@c$ma=4ztprnj#-q6esf+47!aq98%t*^so5n=boc2jps'
export DJANGO_SETTINGS_MODULE
export SECRET_KEY
python manage.py runserver 0.0.0.0:8000
