FROM python:3.7.12
RUN pip3 install python-telegram-bot flask gunicorn python-dateutil flask_basicauth
WORKDIR /code
ADD telegram_warn.py /code/telegram_warn.py
ENV CHATID xxxxx
ENV TOKEN xxxx
CMD ["python3","/code/telegram_warn.py"]

