from typing import Any
from django.db import models
import pickle
import numpy as np
import json

# Create your models here.
class AIModel(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
     return self.name

class ModelVersion(models.Model):
  model=models.ForeignKey(AIModel,on_delete=models.CASCADE)
  model_file=models.BinaryField(default=b'')
  version_number=models.CharField(max_length=50)
  released_at=models.DateTimeField()
  notes=models.TextField()

  def save(self, *args, **kwargs):
        if not self.pk:  
           print("already here  :)")
        super().save(*args, **kwargs)


  def getModel(self):
    deserialized_model = pickle.loads(self.model_file)
    return deserialized_model
  
  def predict(self,input): 
    deserialized_model = self.getModel(self)
    output=deserialized_model.predict(input)
    return output


class Query(models.Model):
  model=models.ForeignKey(AIModel,on_delete=models.CASCADE)
  modelv=models.ForeignKey(ModelVersion,on_delete=models.CASCADE)
  query_input=models.JSONField()
  query_output=models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def save(self, *args, **kwargs):
        if not self.pk:  
           print("already here  :)")
        super().save(*args, **kwargs)
 

  def explain(self):
    ##need to generlize (according to the type like self exlanatory or a certain model to explain .....
    model=self.modelv.getModel()
    x=json.loads(self.query_input)
    # print('x is',x[0])
    y=json.loads(self.query_output)
    # print('y is ',y)
    e=model.explain_local(x,y)
    return e




class Feedback(models.Model):
  class RatingChoices(models.IntegerChoices):
        ONE_STAR = 1, 'One Star'
        TWO_STARS = 2, 'Two Stars'
        THREE_STARS = 3, 'Three Stars'
        FOUR_STARS = 4, 'Four Stars'
        FIVE_STARS = 5, 'Five Stars'
  query=models.ForeignKey(Query,on_delete=models.CASCADE,unique=True)
  star_rating=models.IntegerField(choices=RatingChoices.choices)
  text_feedback=models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class ExplainingAlgo(models.Model):
  algorithm=models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Explanation(models.Model):
  query=models.ForeignKey(Query,on_delete=models.CASCADE)
  explainingAlgo=models.ForeignKey(ExplainingAlgo,null=True,on_delete=models.CASCADE)
  explanation_type=models.CharField(max_length=100)
  explain_input=models.JSONField()
  explain_output=models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
  rate=models.BooleanField()
  def save(self, *args, **kwargs):
        if not self.pk:  
           print("already here  :)")
        super().save(*args, **kwargs)

  def output(self):
    return 0   
  
  def visualiseOutput(self):
    return 0