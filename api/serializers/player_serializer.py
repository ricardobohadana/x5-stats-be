from rest_framework import serializers

from api.models.player import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ['id']  # `id` is excluded from input but included in the response

