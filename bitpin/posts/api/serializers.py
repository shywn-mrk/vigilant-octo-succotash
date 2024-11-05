from django.db.models import Avg
from rest_framework import serializers

from bitpin.posts.models import Post
from bitpin.posts.models import Rating


class PostSerializer(serializers.ModelSerializer):
    user_total_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [f.name for f in Post._meta.fields] + [
            "user_total_ratings",
            "avg_rating",
        ]

    def get_user_total_ratings(self, obj):
        return obj.rating_set.count()

    def get_avg_rating(self, obj):
        return obj.rating_set.aggregate(Avg("score"))["score__avg"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["score", "post", "user"]
        read_only_fields = ["post", "user"]

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            user=self.context["request"].user,
            post=self.context["post"],
            defaults={"score": validated_data["score"]},
        )
        return rating
