from rest_framework import serializers
from .models import Note
from .models import VaultPassword
from .utils.encryption import encrypt_password, decrypt_password
from .models import VaultFile

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at']

class VaultPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    decrypted_password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VaultPassword
        fields = ['id', 'site_name', 'username', 'password', 'decrypted_password', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        password = validated_data.pop('password')
        encrypted = encrypt_password(password)
        return VaultPassword.objects.create(user=user, encrypted_password=encrypted, **validated_data)

    def get_decrypted_password(self, obj):
        return decrypt_password(obj.encrypted_password)

class VaultFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultFile
        fields = ['id', 'file', 'uploaded_at']