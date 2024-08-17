FROM python:3.12

COPY . /home/im_habit_bot

WORKDIR /home/im_habit_bot

RUN pip install -r requirements.txt

ENV PYTHONPATH="/home/im_habit_bot"

CMD python3 bin/main.py
