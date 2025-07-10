from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField() 