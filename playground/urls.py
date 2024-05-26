#map our urls to our view function
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns=[
    #path returns urlpattern opject
    #always end route with /
    path('hello/',views.say_hello),
    path('',views.home,name="home"),

    path('create-aimodel',views.createAIModel,name="create-aimodel"),
    path('create-mversion',views.createMV,name="create-mversion"),
    # path('create-query',views.createQuery,name="create-query"),
    ############# TEST
    path('create-query', views.query_view, name='create-query'),
    path('dynamic_form/<int:model_version_id>/', views.dynamic_form_view, name='dynamic_form_view'),
    path('get_dynamic_form/<int:model_version_id>/', views.get_dynamic_form, name='get_dynamic_form'),
    path('explain_query/<int:query_id>/', views.explain_query, name='explain_query'),
    path('visualise_query/<int:query_id>/', views.visualise_query, name='visualise_query'),
    path('aimodels/', views.AIModelList.as_view()),
    path('aimodels/<int:pk>/', views.AIModelDetail.as_view()),
    path('queries/', views.QueryList.as_view()),
    path('queries/<int:pk>/', views.QueryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
