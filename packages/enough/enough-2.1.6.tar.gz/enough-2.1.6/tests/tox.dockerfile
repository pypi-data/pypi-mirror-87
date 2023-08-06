RUN pip install python-openstackclient python-heatclient # this is not necessary to run tests but to cleanup leftovers when tests fail
RUN pip install tox
RUN git init
COPY requirements.txt requirements-dev.txt tox.ini setup.cfg setup.py README.md /opt/
RUN tox --notest
