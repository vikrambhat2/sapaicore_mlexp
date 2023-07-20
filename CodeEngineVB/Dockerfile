FROM python:3.9.12
ENV LANG C.UTF-8


RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip3 install --upgrade pip

RUN pip3 install --upgrade distlib

# Here we get all python packages.
# There's substantial overlap between scipy and numpy that we eliminate by
# linking them together. Likewise, pip leaves the install caches populated which uses
# a significant amount of space. These optimizations save a fair amount of space in the
# image, which reduces start up time.







# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE


WORKDIR /app
COPY .env /app/.env
COPY . .
ENV $(cat .env | xargs)

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]