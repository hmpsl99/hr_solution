from rest_framework import serializers

from .models import User, Profile, Salary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email"
        ]


class CreateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)

    class Meta:
        model = Profile
        fields = [
            "name",
            "username",
            "national_code",
            "birth_date",
            "password"
        ]

    def save(self, **kwargs):
        password = self.validated_data.pop("password")
        super(CreateProfileSerializer, self).save(**kwargs)
        user = self.context.get("user")
        user.set_password(password)
        user.is_active = True
        user.save()
        self.instance.user = user
        self.instance.save()
        return self.instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class SalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = [
            "user",
            "balance",
            "date"
        ]
