help: _help_

_help_:
	@echo make run - run all tests
	@echo make dev - run tests under development
	@echo make deps - install all the nessecary packages

run:
	python run.py

dev:
	python dev.py

deps:
	sudo apt-get update

	# Installing Selenium framework
	sudo pip install -U selenium

	# Installing Chrome driver for Ubuntu
	sudo apt-get install chromium-chromedriver
	sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

	# Installing python requests
	sudo pip install requests

	# Installing json schema for python
	sudo apt-get install python-jsonschema
