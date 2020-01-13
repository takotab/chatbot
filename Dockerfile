FROM jonemo/pythonnet:python3.6.4-mono4.8.0.524-pythonnet2.3.0

RUN pip install --upgrade pip
RUN pip install tensorflow==1.15.0
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
