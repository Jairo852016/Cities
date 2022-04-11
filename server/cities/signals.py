# server/cities/signals.py

from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection

from .models import Cities


@receiver(post_save, sender=Cities, dispatch_uid='on_citie_save')
def on_citie_save(sender, instance, *args, **kwargs):
    sender.objects.filter(pk=instance.id).update(search_vector=(
        SearchVector('citie', weight='A') +
        SearchVector('admin_name', weight='B')
    ))

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO cities_citiessearchword (word)
            SELECT word FROM ts_stat('
              SELECT to_tsvector(''simple'', citie) ||
                     to_tsvector(''simple'', coalesce(admin_name, ''''))
                FROM cities_cities
               WHERE id = '%s'
            ')
            ON CONFLICT (word) DO NOTHING;
        """, [str(instance.id),])
    
