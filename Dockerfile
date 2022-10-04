FROM odoo:14

USER root

RUN apt-get update && apt-get install -y nano git build-essential libssl-dev libffi-dev cargo swig python3-dev
