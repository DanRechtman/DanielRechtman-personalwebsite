SHELL := /bin/bash


run: 
	.\venv\Scripts\deactivate.bat
	.\venv\Scripts\activate.bat
	python manage.py runserver & npm run dev && fg