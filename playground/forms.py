from django.forms import ModelForm,Form,forms,FloatField
from .models import AIModel, ModelVersion, Query

class AIModelForm(ModelForm):
    class Meta:
        model = AIModel
        fields= '__all__'

class ModelVersionForm(ModelForm):
    class Meta:
        model=ModelVersion
        fields='__all__'

class QueryForm(ModelForm):
    class Meta:
        model=Query
        fields=['model','modelv']


#################### TEST

def generate_dynamic_form(feature_names):
    class DynamicForm(forms.Form):
        pass
        ### modify later to make sure of all feature types are accepted :)
    for feature_name in feature_names:
        field = FloatField(label=feature_name) 
        DynamicForm.base_fields[feature_name] = field

    return DynamicForm