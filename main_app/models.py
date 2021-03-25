from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=256)

    def __repr__(self):
        return f"<User '{self.username}'>"

    def __str__(self):
        return f"<User '{self.username}'>"


class Twit(models.Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    author = fields.ForeignKeyField("models.User", related_name="twits")
    date_posted = fields.DatetimeField(auto_now=True)
    date_updated = fields.DatetimeField(auto_now=True, null=True)

    def __repr__(self):
        return f"<Twit '{self.author.username}' '{self.text[:50]}'>"

    def __str__(self):
        return f"<Twit '{self.author.username}' '{self.text[:50]}'>"