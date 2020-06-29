from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
	""" Serializer for the Person model """
	class Meta:
		model = Person
		fields = ('height', 'weight', 'uploaded', 'from_file')