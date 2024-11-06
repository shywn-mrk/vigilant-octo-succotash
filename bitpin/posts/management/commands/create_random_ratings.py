from random import choice
from random import randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from bitpin.posts.models import Post
from bitpin.posts.models import Rating

User = get_user_model()


class Command(BaseCommand):
    help = "Creates random ratings"

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        posts = list(Post.objects.all())

        if not users or not posts:
            self.stdout.write(
                self.style.WARNING(
                    "No users or posts found. Add some users and posts before running this command.",  # noqa: E501
                ),
            )
            return

        created_count = 0
        for _ in range(10000):
            user = choice(users)
            post = choice(posts)
            score = randint(0, 5)

            _, created = Rating.objects.update_or_create(
                user=user,
                post=post,
                defaults={"score": score},
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} ratings"),
        )
