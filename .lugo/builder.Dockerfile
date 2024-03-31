FROM python:3.9-slim-buster

#RUN apt-get update
#RUN apt-get install -y git-core curl build-essential openssl libssl-dev
#RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash  \
#    && \
#    nvm install 20

    # verifies the right Node.js version is in the environment
#RUN node -v # should print `v20.12.0`

    # verifies the right NPM version is in the environment
#RUN npm -v # should print `10.5.0`

ENV NODE_VERSION=16.13.0
RUN apt-get update && apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version
