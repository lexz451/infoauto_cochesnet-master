from django.db.models import CharField
from model_utils.models import TimeStampedModel
from picklefield import PickledObjectField


class Setting(TimeStampedModel):
    name = CharField(max_length=255, unique=True)
    value = PickledObjectField()

