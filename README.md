qofdatabase
===========

The code behind the QOF Datbase website - www.gpcontract.co.uk

Installation
============

$ mkvirtualenv -a `pwd` qof

$ pip install -r requirements.txt

$ cp local_settings.py.example local_settings.py

Edit local_settings.py as appropriate.

$ python manage.py syncdb