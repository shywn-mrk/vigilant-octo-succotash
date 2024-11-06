from celery import shared_task
from django.db import connection


@shared_task
def refresh_materialized_view():
    with connection.cursor() as cursor:
        cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY post_avg_ratings;")
