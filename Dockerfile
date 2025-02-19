FROM python:3.9-bullseye


RUN apt-get update && apt-get install gcc gfortran musl -y

RUN pip install --upgrade pip
RUN pip install dacite
RUN pip install matplotlib

# create workdir
WORKDIR /opt/apps/pymedeas

# copy requirements to the workdir
COPY requirements.txt .

# Install all requrements for our app
RUN pip install -r requirements.txt

# copy source files to the workdir
ADD scenarios ./scenarios
ADD pytools ./pytools
ADD outputs ./outputs
ADD models ./models
ADD plot_tool.py .
ADD run.py .

# to build the image run
# docker build --network host -t pymedeas .

# To get to a cmd prompt run
# docker exec -it --net=host pymedeas bash

# To run the app
# python run.py -h
