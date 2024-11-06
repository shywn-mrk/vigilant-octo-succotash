# Generated by Django 5.0.9 on 2024-11-06 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW post_avg_ratings AS
            SELECT post_id, AVG(score) AS avg_rating
            FROM posts_rating
            GROUP BY post_id;
            """,
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS post_avg_ratings;"
        ),
        
        migrations.RunSQL(
            "CREATE UNIQUE INDEX idx_avg_view ON post_avg_ratings(post_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_avg_view;"
        ),
    ]