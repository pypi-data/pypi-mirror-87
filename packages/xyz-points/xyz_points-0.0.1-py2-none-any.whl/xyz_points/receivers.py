# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, pre_save
from .models import Item, Point
from django.db.models import Sum

@receiver(post_save, sender=Item)
def update_points(sender, **kwargs):
    item = kwargs.get('instance')
    point = item.point
    s = point.items.aggregate(s=Sum('value'))['s']
    Point.objects.filter(id=point.id).update(value=s)