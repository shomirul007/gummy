from rest_framework import serializers

class SubredditSerializer(serializers.Serializer):
    name = serializers.CharField()
    members = serializers.IntegerField()
    description = serializers.CharField()
