from rest_framework import serializers

from bitpin.posts.models import Post
from bitpin.posts.models import Rating


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


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
