FROM python:3.9

COPY ./stocks_products ./site
RUN pip3 install -r /site/requirements.txt
EXPOSE 8000
ENV MyENV=Default
WORKDIR site

