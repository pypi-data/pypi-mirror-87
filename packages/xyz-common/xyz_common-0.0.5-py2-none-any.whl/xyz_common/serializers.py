# -*- coding:utf-8 -*- 

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from . import models

class ContenttypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ("app_label", 'model', 'name', '__str__', 'id')

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setting
        exclude = ()
