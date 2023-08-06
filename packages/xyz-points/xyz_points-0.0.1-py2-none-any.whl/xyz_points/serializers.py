# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_restful.mixins import IDAndStrFieldSerializerMixin
from rest_framework import serializers
from . import models


class ProjectSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Project
        exclude = ()

class SubjectSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", label=models.Project._meta.verbose_name, read_only=True)
    class Meta:
        model = models.Subject
        exclude = ()

class CategorySerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", label=models.Project._meta.verbose_name, read_only=True)
    class Meta:
        model = models.Category
        exclude = ()

class SessionSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", label=models.Project._meta.verbose_name, read_only=True)
    class Meta:
        model = models.Session
        exclude = ()

class PointSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Point
        exclude = ()

class ItemSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Item
        exclude = ()
