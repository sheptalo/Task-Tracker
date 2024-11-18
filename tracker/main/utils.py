import os
from datetime import datetime
from smtplib import SMTP

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from dotenv import load_dotenv
import logging

load_dotenv()


def send_websocket(uid, message, mess_type="notify.user"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{uid}",
        {
            "type": mess_type,
            "message": message,
        },
    )
    logging.info(f"Отправлено WebSocket уведомление пользователю с id {uid}")


def send_email(to, message):
    smtp_obj = SMTP("smtp.gmail.com", 587)
    smtp_obj.starttls()

    from_email = os.environ.get("SENDER_EMAIL")

    smtp_obj.login(from_email, os.environ.get("GOOGLE_KEY"))
    smtp_obj.sendmail(from_email, to, message)
    smtp_obj.quit()
    logging.info(f"Отправлено Письмо {to}")


def filter_get_params(filters, query, get_data):
    for i in filters:
        if i.split("__")[0] in get_data.keys():
            query = query.filter(**{i: get_data[i]})
    return query


def order_query(query, order_by):
    return query.order_by(order_by) if order_by != "" else query


def date_filter(mode, query, start="", end=""):
    if start:
        start_date = datetime(
            day=int(start.split(".")[0]),
            month=int(start.split(".")[1]),
            year=int(start.split(".")[-1]),
        )
        filter_kwargs_start = {mode + "__gte": start_date}
        query = query.filter(**filter_kwargs_start)
    if end:
        end_date = datetime(
            day=int(end.split(".")[0]),
            month=int(end.split(".")[1]),
            year=int(end.split(".")[-1]),
        )
        filter_kwargs_end = {mode + "__lte": end_date}

        query = query.filter(**filter_kwargs_end)

    return query
