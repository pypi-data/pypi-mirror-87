from django.contrib.auth.models import User
from django.db import models
from w.services.abstract_model_service import AbstractModelService


class UserService(AbstractModelService):
    _model = User

    @classmethod
    def get_or_create(cls, **attrs):
        # noinspection PyUnresolvedReferences
        try:
            return cls._model.objects.get(username=attrs.get("username"))
        except cls._model.DoesNotExist:
            return cls._model.objects.create(**attrs)

    @classmethod
    def create(cls, **attrs) -> models.Model:
        return User.objects.create_user(**attrs)
