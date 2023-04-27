from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from author.serializers import UserSerializer
from .models import Image, Badge, Post


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    def validate(self, data):
        if data['image'].size > 6000000:
            raise serializers.ValidationError({"Error": "Image size too big!"})

        return super().validate(data)

    class Meta:
        model = Image
        fields = ('image',)


class BadgeSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if len(data['name']) > 100:
            raise serializers.ValidationError({"Error": "The maximum character of name can be 100."})

    class Meta:
        model = Badge
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)
    badges = serializers.PrimaryKeyRelatedField(queryset=Badge.objects.all(), many=True, required=False)
    images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"

    def validate(self, value):
        if len(value) > 100:
            return serializers.ValidationError({"Error": "Max title length is 100 characters."})
        return value

    def create(self, validated_data):
        user = self.context['user']
        badges_data = validated_data.pop('badges', [])
        images = validated_data.pop('images', [])
        post = Post.objects.create(author=user, **validated_data)

        for badge_data in badges_data:
            badge = Badge.objects.get(pk=badge_data.id)
            post.badges.add(badge)

        for image in images:
            post.images.create(image=image)

        if 'image' in validated_data:
            post.image = validated_data['image']
            post.save()

        return post

    def update(self, instance, validated_data):
        post = instance
        post.title = validated_data.get('title', post.title)
        post.content = validated_data.get('content', post.content)
        post.state = validated_data.get('state', post.state)
        post.release_date = validated_data.get('release_date', post.release_date)
        post.selected_image = validated_data.get('selected_image', post.selected_image)
        post.save()

        badges_data = validated_data.pop('badges', None)
        if badges_data is not None:
            post.badges.clear()
            for badge_data in badges_data:
                try:
                    badge = Badge.objects.get(id=badge_data.id)
                    post.badges.add(badge)
                except Badge.DoesNotExist:
                    pass

        images_data = validated_data.pop('images', None)
        if images_data is not None:
            for image_data in images_data:
                post.images.clear()
                post.images.create(image=image_data)

        return post
