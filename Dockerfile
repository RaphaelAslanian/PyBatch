FROM python:3.6

LABEL maintainer="raphael.aslanian@gmail.com"

# Requirements and code
ADD requirements.txt requirements.txt

# Install dependencies
RUN pip3 install pip --upgrade && \
    pip3 install -r requirements.txt

COPY src/ ./src/

EXPOSE 5000

CMD ["python", "src"]

