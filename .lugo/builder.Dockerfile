FROM python:3.9-slim-buster

# Installing NodeJS to we can use Nodemon instead of watchdog (Whatchdos does not work weel on containers on Windows)
ENV NODE_VERSION=16.13.0
RUN apt-get update && apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN npm install -g nodemon@3.0.1
  
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
