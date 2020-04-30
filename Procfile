release: python manage.py migrate && python manage.py csv_to_db --csv genie2.csv
web: gunicorn biblio_support.wsgi