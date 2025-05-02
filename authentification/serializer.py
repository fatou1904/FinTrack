from rest_framework import serializers

from .models import User

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']

class UserRegister(serializers.ModelSerializer):
    confirmer_password = serializers.CharField(write_only = True, required=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'confirmer_password']
        extra_kwargs = {'password' : {'write_only': True}}
        
        def validate(self, data):
            if data ['password'] != data['confirmer_password']:
                raise serializers.ValidationError({"password":"les mots de passe ne correspondent pas"})
            return data
        
    def create(self, validated_data):
        validated_data.pop('confirmer_password')
        user = User.objects.create_user (
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user