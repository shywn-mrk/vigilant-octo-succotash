from random import choice

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from bitpin.posts.models import Post

User = get_user_model()


class Command(BaseCommand):
    help = "Creates 1,000 random posts"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = list(User.objects.all())

        posts = [
            Post(
                user=choice(users),
                title=fake.sentence(nb_words=6),
                body=fake.paragraph(nb_sentences=10),
            )
            for _ in range(1000)
        ]

        Post.objects.bulk_create(posts)

        self.stdout.write(self.style.SUCCESS("Successfully created 1,000 posts"))
