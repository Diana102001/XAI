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

########
# serializers.py

class DynamicFormSerializer(serializers.Serializer):
    # Dynamically add fields based on feature names
    def __init__(self, *args, **kwargs):
        feature_names = kwargs.pop('feature_names', None)
        super(DynamicFormSerializer, self).__init__(*args, **kwargs)
        if feature_names:
            for feature in feature_names:
                self.fields[feature] = serializers.CharField()
