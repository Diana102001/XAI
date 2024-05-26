from rest_framework import serializers
from .models import AIModel,Query

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=AIModel
        fields=['name','description']
    
class QuerySeralizer(serializers.ModelSerializer):
    class Meta:
        model=Query
        fields='__all__'
