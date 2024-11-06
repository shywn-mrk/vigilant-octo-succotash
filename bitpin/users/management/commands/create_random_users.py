from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "Creates 2,000 random users"

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = [
            User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                is_active=True,
            )
            for _ in range(2000)
        ]

        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS("Successfully created 2,000 users"))
