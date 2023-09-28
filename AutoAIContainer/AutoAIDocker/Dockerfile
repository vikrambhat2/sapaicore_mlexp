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


RUN pip3 --no-cache-dir install numpy scipy pandas flask gunicorn scikit-learn==1.0.2 autoai-libs==1.13.4 ibm-cloud-sdk-core==3.16.7 ibm_watson_openscale python-dotenv
# Set environment variables from the .env file

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

#COPY requirements.txt /app/src/requirements.txt
#RUN pip install -r /app/src/requirements.txt

RUN mkdir -p /app/src
COPY auto.py /app/src/
COPY .env /app/src/
COPY auto-ai-pipeline.pickle /app/src/auto-ai-pipeline.pickle

ADD auto.py auto.py
ADD auto-ai-pipeline.pickle auto-ai-pipeline.pickle
ADD .env .env
# Required to execute script
RUN chgrp -R nogroup /app && \
    chmod -R 770 /app
    
EXPOSE 7000

#
CMD ["python", "auto.py"]