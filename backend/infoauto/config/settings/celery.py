from datetime import timedelta

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update_session_user_every_day': {
        'task': 'infoauto.users.tasks.update_session_user',
        'schedule': crontab(hour=00, minute=00),
    },
    'ubunet_calls': {
        'task': 'infoauto.netelip_leads.tasks.ubunet_calls',
        'schedule': timedelta(seconds=60),
    },
}
