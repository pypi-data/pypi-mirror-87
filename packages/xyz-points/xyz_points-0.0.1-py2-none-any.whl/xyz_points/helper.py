# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from datetime import datetime
from . import models
from django.apps.registry import apps
from xyz_util.datautils import access
from django.contrib.contenttypes.models import ContentType
import logging

log = logging.getLogger('django')

SUBJECT_REGISTER = {}


def subject_add_item_receiver(sender, **kwargs):
    for sid in SUBJECT_REGISTER[sender]:
        try:
            subject = models.Subject.objects.get(id=sid)
            model = kwargs['instance']
            created = kwargs['created']
            function = subject.function
            if function.get('created') and not created:
                break
            subject_add_item(subject, model)
        except:
            import traceback
            log.error('points subject_add_item_receiver sid: %s error: %s', sid, traceback.format_exc())


def subject_add_item(subject, model):
    function = subject.function
    value = access(model, function['value'])

    project = subject.project
    now = datetime.now()
    session = project.sessions.filter(begin_time__lt=now, end_time__gt=now, is_active=True).first()
    if not session:
        return
    # print project, session, subject, model, value
    user = model.user
    category = None
    if 'category' in function:
        cn = access(model, function.get('category'))
        print cn
        category, created = project.categories.get_or_create(name=cn)
    point, created = session.points.get_or_create(
        category=category,
        user=user,
        defaults=dict(value=value)
    )
    item, created = point.items.update_or_create(
        user=user,
        owner_type=ContentType.objects.get_for_model(model),
        owner_id=model.id,
        defaults=dict(
            owner_name=unicode(model),
            value=value
        )
    )


def create_points_receiver():
    from django.db.models.signals import post_save
    try:
        for s in models.Subject.objects.filter(is_active=True):
            fd = s.function
            model = apps.get_model('%s.%s' % (fd['app'], fd['model']))
            sid = s.id
            ms = SUBJECT_REGISTER.setdefault(model, [])
            if not ms:
                post_save.connect(subject_add_item_receiver, sender=model)
            ms.append(sid)
            print 'connect', s, model
    except:
        import traceback
        log.error('create_points_receiver error: %s', traceback.format_exc())
