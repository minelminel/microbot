"""
message.py
"""
import logging, uuid, time
from types import SimpleNamespace
import marshmallow as ma

log = logging.getLogger(__name__)

make_uuid = lambda: str(uuid.uuid4())
make_time = lambda: int(time.time() * 1000)


class Message(SimpleNamespace):
    pass


class MessageSchema(ma.Schema):
    # what is the purpose of this message
    # ex. "info"
    type = ma.fields.Str(
        default="message",
        missing="message",
        validate=ma.validate.OneOf(choices=["message", "info", "error"]),
    )

    # epoch milliseconds
    # ex. 1619829580766
    time = ma.fields.Int(default=make_time, missing=make_time)

    # corresponds to the topic
    # ex. "axis.motion"
    room = ma.fields.Str(required=True)

    # description & context
    # ex. "x-axis slider update"
    memo = ma.fields.Str(default=str, missing=str)

    # json object
    # ex. { "X": 10 }
    data = ma.fields.Raw(default=None, missing=None)

    # random unique identifier
    # ex. "fa80d178-b87b-4360-ad90-83ca0888d41d"
    guid = ma.fields.UUID(default=make_uuid, missing=make_uuid)

    @ma.post_load
    def postload(self, data, **kwargs):
        return Message(**data)


# DRIVER
if __name__ == "__main__":
    schema = MessageSchema()
    o = {"room": "info", "memo": "hello world"}
    msg = schema.load(o)
    print(msg)
    print(schema.dump(msg))
