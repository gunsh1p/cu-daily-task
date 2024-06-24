from tortoise import models, fields

class Event(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=50)
    time = fields.TimeField()
    chat_id = fields.BigIntField()
    thread_id = fields.IntField(null=True, default=None)