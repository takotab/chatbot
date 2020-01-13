FROM python:3.5.5-jessie

# https://www.mono-project.com/download/stable/#download-lin
RUN sudo apt install gnupg ca-certificates
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
RUN sudo apt update

RUN sudo apt install mono-devel

# https://github.com/pythonnet/pythonnet/issues/562#issuecomment-339044574
RUN pip install pip --upgrade && \
  pip install setuptools --upgrade 

RUN pip install git+https://github.com/pythonnet/pythonnet 

#https://github.com/pythonnet/pythonnet/issues/562#issuecomment-339057789
# RUN python pythonnet/setup.py bdist_wheel \
#   && pip install --no-index --find-links=./pythonnet/dist/ pythonnet

# littlebit of a change to make debug quicker
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

#COPY prepfiles.zip /app/prepfiles.zip

# want the download things in the dockerfile these are trys
# maybe next try to run python entity_rec/check_prep_files.py
# RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-oSe1f08q2MA6s4ix_5ELFZ6U5wp-aKP" -O prepfiles.zip && rm -rf /tmp/cookies.txt /app/prepfiles.zip
# ADD https://drive.google.com/a/devoteam.com/uc?export=download&id= /app

COPY prepfiles.zip /app/prepfiles.zip

COPY . /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "main.py"]
