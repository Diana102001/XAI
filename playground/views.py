from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import AIModel,ModelVersion,Query
from .forms import AIModelForm,QueryForm,ModelVersionForm, generate_dynamic_form
from django.template.loader import render_to_string
import pandas as pd
import json
from interpret import show,preserve,show_link
import os
from .serializers import AIModelSerializer,QuerySeralizer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics




class AIModelList(generics.ListCreateAPIView):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    

class QueryList(generics.ListCreateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySeralizer
    # """
    # List all snippets, or create a new snippet.
    # """
    # def get(self, request, format=None):
    #     aimodels = AIModel.objects.all()
    #     serializer = AIModelSerializer(aimodels, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = AIModelSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        


class AIModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=AIModel.objects.all()
    serializer_class=AIModelSerializer

class QueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Query.objects.all()
    serializer_class=QuerySeralizer

    # """
    # Retrieve, update or delete a snippet instance.
    # """
    # def get_object(self, pk):
    #     try:
    #         return AIModel.objects.get(pk=pk)
    #     except AIModel.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     aimodel = self.get_object(pk)
    #     serializer = AIModelSerializer(aimodel)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     aimodel = self.get_object(pk)
    #     serializer = AIModelSerializer(aimodel, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
def say_hello(request):
    # pull and transform from db or send email
    return HttpResponse('Hello world')
def home(request):
    aimodels=AIModel.objects.all()
    context={'aimodels':aimodels}
    return render(request,"home.html",context)
def createAIModel(request):
    form=AIModelForm()
    if request.method == 'POST':
        form=AIModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'aimodel_form.html',context)

def createMV(request):
    form=ModelVersion()
    if request.method == 'POST':
        form=ModelVersionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'modelversion_form.html',context)


def createQuery(request):
    form=QueryForm()
    if request.method == 'POST':
        form=QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}

    return render(request,'query_form.html',context)


########## TEST
def query_view(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            model_version = form.cleaned_data['modelv']
            return redirect('dynamic_form_view', model_version_id=model_version.id)
    else:
        form = QueryForm()

    return render(request, 'query_form.html', {'form': form})

def dynamic_form_view(request, model_version_id):
    model_version = get_object_or_404(ModelVersion, id=model_version_id)
    model = model_version.getModel()
    feature_names = model.feature_names_in_

    DynamicForm = generate_dynamic_form(feature_names)
    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data
            # Create a Query instance and store input data
            query = Query(
                model=model_version.model,
                modelv=model_version,
                query_input=json.dumps(list(input_data.values()))
            )
            result = use_ai_model(model, input_data)
            query.query_output = json.dumps(result.get(0))
            query.save()  # Save the query with input and output data
            return render(request, 'result.html', {'result': result, 'query_id': query.pk})

    else:
        form = DynamicForm()

    return render(request, 'dynamic_form.html', {'form': form, 'model_version': model_version})

def use_ai_model(model, input_data):
    # Assuming the model has a predict method
    input_df = pd.DataFrame([input_data])
    result = model.predict(input_df)
    return {"result": result[0]}

def get_dynamic_form(request, model_version_id):
    model_version = get_object_or_404(ModelVersion, id=model_version_id)
    model = model_version.getModel()
    feature_names = model.feature_names_in_

    DynamicForm = generate_dynamic_form(feature_names)
    form = DynamicForm()
    form_html = render_to_string('dynamic_form_partial.html', {'form': form})
    
    return JsonResponse({'form_html': form_html})

def explain_query(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    e = query.explain()
    explanation=describe_explanation(e)
    # explanation ="ccc"
    return JsonResponse({'explanation': explanation})


def describe_explanation(e):
    decision=(e._internal_obj.get('specific')[0]).get('decision')
    pre=(e._internal_obj.get('specific')[0]).get('perf').get('predicted_score')
    TheExp="The decision was made with these steps: from node "
    for d in decision:
        if (d==decision[-1]):
            TheExp+=str(d)+", so the taken decition is "+str(pre)+ " :)"
        else:
            nodes=(e._internal_obj.get('specific')[0]).get('nodes')
            for n in nodes:
                if (n.get('data').get('id')==str(d)):
                    f=n.get('data').get('label')
                    # Find the position of #
                    position_of_hash = f.find('#')
                    substring = f[:position_of_hash]
            TheExp+= str(d)+" the feature "+substring
            TheExp+=" then it goes to the node"
    
    return TheExp

def visualise_query(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    e = query.explain()
    u=show_link(e)
    print(e)
    return redirect(u)

    
# def visualise_query(request, query_id):
#     # Instantiate the explainer (example using LIME)
#     query = get_object_or_404(Query, id=query_id)
#     e = query.explain()
#     # Create a directory to store the HTML file if it doesn't exist
#     html_dir = 'explanations'
#     if not os.path.exists(html_dir):
#         os.makedirs(html_dir)

#     # Generate the HTML file
#     html_file_path = os.path.join(html_dir, f'visual.html') 
#     with open(html_file_path, 'w') as html_file:
#         preserve(e, file_name=html_file)
        
#     with open(html_file_path, 'r') as html_file:
#         return HttpResponse(html_file.read(), content_type='text/html')
