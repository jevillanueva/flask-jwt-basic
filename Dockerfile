FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


# expect a build-time variable
ARG A_HOST="0.0.0.0"
ARG A_PORT=5000
ARG A_DEBUG=False

# use the value to set the ENV var default
ENV SERVER_HOST=${A_HOST}
ENV SERVER_PORT=${A_PORT}
ENV DEBUG=${A_DEBUG}

EXPOSE ${A_PORT}

CMD [ "python", "./app.py" ]