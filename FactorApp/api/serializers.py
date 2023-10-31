from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from FactorApp.models import Follow, Following, User, Post
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'avatar', 'first_name', 'last_name', 'gender', 'contact', 'dob',)


class UserAvatarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["avatar",]

    def save(self, *args, **kwargs):
        if self.instance.avatar:
            self.instance.avatar.delete()
        return super().save(*args, **kwargs)


class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'gender', 'contact','dob',)
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, data):
        user_query = User.objects.filter(email__iexact=data).exists()
        if user_query:
            raise serializers.ValidationError(f'{data} already exist!')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs, *args, **kwargs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        qs = User.objects.filter(email__iexact=email).exists()
        if qs is None:
            raise serializers.ValidationError(f'Sorry {email} does not exist.')
        if not user:
            raise serializers.ValidationError('Incorrect email or password.')
        return super(LoginSerializer, self).validate(attrs, *args, **kwargs)


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'contact', 'dob',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.gender = validated_data['gender']
        instance.contact = validated_data['contact']
        instance.dob = validated_data['dob']
        instance.save()
        return super(ProfileUpdateSerializer, self).update(instance, validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return super(ChangePasswordSerializer, self).validate(attrs)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return super(ChangePasswordSerializer, self).validate(value)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%b %d, %Y", required=False)
    created_time = serializers.TimeField(format="%I:%M:%S %p", required=False)
    images = serializers.ImageField(required=False)
    videos = serializers.FileField(required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('user', 'text', 'images', 'videos', 'created_date', 'created_time',)
        read_only_fields = ('created_date', 'created_time',)
    
    def get_user(self, instance):
        return instance.email


class LikePostSerializer(serializers.ModelSerializer):
    likes = UserSerializer(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ["likes", "likes_count", "is_liked"]
    
    def get_likes(self, instance):
        return instance.likes.email
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        login_user = self.context['request'].user
        likes_obj = self.instance.likes.all()
        unlikes_obj = self.instance.unlikes.all()
        has_clicked = False

        if login_user in likes_obj:
            has_clicked = True

        return has_clicked

    def update(self, *args, **kwargs):
        login_user = self.context['request'].user
        likes_obj = self.instance.likes.all()
        unlikes_obj = self.instance.unlikes.all()

        if login_user not in likes_obj and login_user not in unlikes_obj:
            self.instance.likes.add(login_user)
        else:
            self.instance.likes.remove(login_user)

        return super().update(*args, **kwargs)


class UnLikePostSerializer(serializers.ModelSerializer):
    unlikes = UserSerializer(read_only=True, many=True)
    unlikes_count = serializers.SerializerMethodField()
    is_unliked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ["unlikes", "unlikes_count", "is_unliked"]
    
    def get_unlikes(self, instance):
        return instance.unlikes.email
    
    def get_unlikes_count(self, obj):
        return obj.unlikes.count()
    
    def get_is_unliked(self, obj):
        login_user = self.context['request'].user
        likes_obj = self.instance.likes.all()
        unlikes_obj = self.instance.unlikes.all()
        has_clicked = False

        if login_user in unlikes_obj:
            has_clicked = True

        return has_clicked

    def update(self, *args, **kwargs):
        login_user = self.context['request'].user
        likes_obj = self.instance.likes.all()
        unlikes_obj = self.instance.unlikes.all()

        if login_user not in unlikes_obj and login_user not in likes_obj:
            self.instance.unlikes.add(login_user)
        else:
            self.instance.unlikes.remove(login_user)

        return super().update(*args, **kwargs)


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True, many=True)
    followers_count = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%b %d, %Y, %I:%M:%S %p", required=False)
    is_followed = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ["user", "followers", "followers_count", "date", "is_followed"]
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_is_followed(self, obj):
        login_user = self.context['request'].user
        followers_obj = self.instance.followers.all()
        has_followed = False

        if login_user in followers_obj:
            has_followed = True

        return has_followed

    def update(self, *args, **kwargs):
        login_user = self.context['request'].user
        followers_obj = self.instance.followers.all()

        if login_user not in followers_obj:
            self.instance.followers.add(login_user)
        else:
            self.instance.followers.remove(login_user)

        return super().update(*args, **kwargs)


class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followings = UserSerializer(read_only=True, many=True)
    followings_count = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%b %d, %Y, %I:%M:%S %p", required=False)
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = Following
        fields = ["user", "followings", "followings_count", "date", "is_following"]
    
    def get_followings_count(self, obj):
        return obj.followings.count()
    
    def get_is_following(self, obj):
        login_user = self.context['request'].user
        followers_obj = self.instance.followings.all()
        has_followed = False

        if login_user in followers_obj:
            has_followed = True

        return has_followed

    def update(self, *args, **kwargs):
        user_id = self.context['user_id']
        followee = User.objects.get(id=int(user_id))
        followers_obj = self.instance.followings.all()

        if followee not in followers_obj:
            self.instance.followings.add(followee)
        else:
            self.instance.followings.remove(followee)

        return super().update(*args, **kwargs)

"""
class FollowSeriliazer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True, many=True)
    to_user = UserSerializer(read_only=True, many=True)
    followed_date = serializers.DateTimeField(format="%b %d, %Y, %I:%M:%S %p", required=False)

    def get_from_user(self, obj):
        pass

    class Meta:
        model = Follow
        fields = ["from_user", "to_user", "followed_date",]
"""

