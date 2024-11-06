from rest_framework import serializers

from bitpin.posts.models import Post
from bitpin.posts.models import Rating


class PostSerializer(serializers.ModelSerializer):
    total_ratings = serializers.IntegerField(read_only=True)
    avg_rating = serializers.DecimalField(
        read_only=True,
        default=0,
        decimal_places=1,
        max_digits=2,
    )

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user"]


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
