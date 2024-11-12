from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_websocket(uid, message, mess_type="notify.user"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{uid}",
        {
            "type": mess_type,
            "message": message,
        },
    )
