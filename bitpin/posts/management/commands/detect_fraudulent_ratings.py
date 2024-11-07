import statistics
from collections import Counter
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from bitpin.posts.models import Post
from bitpin.posts.models import Rating


class Command(BaseCommand):
    help = (
        "Detects potentially fraudulent rating patterns and provides an analysis report"
    )

    def handle(self, *args, **kwargs):
        self.detect_unusual_low_ratings()
        self.user_rating_similarity_analysis()
        self.detect_statistical_outliers()

    def detect_unusual_low_ratings(self):
        time_window = timezone.now() - timedelta(hours=1)
        recent_low_ratings = Rating.objects.filter(
            score__lte=1,
            created_at__gte=time_window,
        )

        post_low_ratings = Counter(rating.post_id for rating in recent_low_ratings)

        flagged_posts = [
            post_id
            for post_id, count in post_low_ratings.items()
            if count > 10  # noqa: PLR2004
        ]

        self.stdout.write(
            self.style.WARNING("Unusual Low Ratings Detected:"),
        )
        for post_id in flagged_posts:
            post = Post.objects.get(id=post_id)
            self.stdout.write(
                f"Post ID {post_id} ('{post.title}'): {post_low_ratings[post_id]} low ratings in the last hour",  # noqa: E501
            )

    def user_rating_similarity_analysis(self):
        user_ratings = Rating.objects.values_list("user_id", "post_id", "score")

        user_post_ratings = {}
        for user_id, post_id, score in user_ratings:
            if user_id not in user_post_ratings:
                user_post_ratings[user_id] = {}
            user_post_ratings[user_id][post_id] = score

        flagged_users = []
        for user_id, ratings in user_post_ratings.items():
            low_ratings_count = sum(1 for score in ratings.values() if score <= 1)
            if low_ratings_count > 5:  # noqa: PLR2004
                flagged_users.append(user_id)

        self.stdout.write(
            self.style.WARNING(
                "\nUsers with Similar Low Ratings Detected:",
            ),
        )
        for user_id in flagged_users:
            self.stdout.write(
                f"User ID {user_id} consistently rated multiple posts with low scores",
            )

    def detect_statistical_outliers(self):
        post_ids = Rating.objects.values_list("post_id", flat=True).distinct()

        self.stdout.write(
            self.style.WARNING("\nStatistical Outliers Detected:"),
        )
        for post_id in post_ids:
            scores = list(
                Rating.objects.filter(post_id=post_id).values_list("score", flat=True),
            )
            if len(scores) < 10:  # noqa: PLR2004
                continue

            mean_score = statistics.mean(scores)
            stdev_score = statistics.stdev(scores)

            outliers = [
                score for score in scores if score < mean_score - 2 * stdev_score
            ]
            if len(outliers) > len(scores) * 0.2:
                post = Post.objects.get(id=post_id)
                self.stdout.write(
                    f"Post ID {post_id} ('{post.title}'): {len(outliers)} outliers detected out of {len(scores)} ratings",  # noqa: E501
                )

        self.stdout.write(
            self.style.SUCCESS("\nFraud Detection Analysis Completed."),
        )
