from django.contrib.auth import authenticate
from platforms.models import Platform
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True,
    )
    platform_slug = serializers.CharField(write_only=True)
    exp_msg = "No active account found with the given credentials and platform."

    # We set username_field to None to tell SimpleJWT
    # we are handling identification manually
    username_field = "email"

    def validate(self, attrs: dict) -> dict:
        email = attrs.get("email")
        password = attrs.get("password")
        platform_slug = attrs.get("platform_slug")

        try:
            platform = Platform.objects.get(slug=platform_slug)
            user = CustomUser.objects.get(email=email, platform=platform)
        except (Platform.DoesNotExist, CustomUser.DoesNotExist):
            raise serializers.ValidationError(self.exp_msg)

        user = authenticate(username=user.username, password=password)

        if user is None or not user.is_active:
            raise serializers.ValidationError(self.exp_msg)

        self.user = user
        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @classmethod
    def get_token(cls, user: CustomUser):
        token = super().get_token(user)
        # Add custom claims
        token["platform_slug"] = user.platform.slug
        return token


class RegisterSerializer(serializers.ModelSerializer):
    platform_slug = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "platform_slug")

    def create(self, validated_data: dict) -> CustomUser:
        platform_slug = validated_data.pop("platform_slug")
        password = validated_data.pop("password")
        platform = Platform.objects.get(slug=platform_slug)

        return CustomUser.objects.create_user(
            email=validated_data["email"],
            platform=platform,
            username=f"{validated_data['email']}_{platform_slug}",
            password=password,
        )
