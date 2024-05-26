# ml_utils.py

import os
import django
import pickle
import json
import numpy as np

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from .models import AIModel, ModelVersion, Query, Explanation
from datetime import datetime
from sklearn.datasets import make_classification
import pandas as pd
from interpret.glassbox import (LogisticRegression,
                                ClassificationTree,
                                ExplainableBoostingClassifier)
from interpret.glassbox._decisiontree import TreeExplanation
from interpret import show
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from .serializers import AIModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io




def run():
    # aimodel=AIModel(name="test2",description="none")
    # aimodel.save()

    # serializer = AIModelSerializer(aimodel)
    # d=serializer.data

    # content = JSONRenderer().render(serializer.data)
    # print(content)

    # stream=io.BytesIO(content)
    # data=JSONParser().parse(stream)
    # print(data)

    # serializer=AIModelSerializer(data=data)
    # print(serializer.is_valid())

    # print(serializer.validated_data)
    # serializer.save()


    serializer = AIModelSerializer(AIModel.objects.all(), many=True)
    print(serializer.data)

#     # Generate synthetic data
#     X, y = make_classification(n_samples=1000, n_features=4, n_classes=2, random_state=42)

#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#     tree = ClassificationTree()
#     tree.fit(X_train.astype(float), y_train.astype(float))
#     print("Training finished.")
#     y_pred = tree.predict(X_test.astype(float))
#     print(f"F1 Score {f1_score(y_test.astype(float), y_pred.astype(float), average='macro')}")
#     print(f"Accuracy {accuracy_score(y_test.astype(float), y_pred.astype(float))}")

#     m = AIModel.objects.get(id=1)
# ##    print(m.name)
#     ###create model version
#     serialized_instance = pickle.dumps(tree)

#     modelv=ModelVersion(model=m,model_file=serialized_instance,version_number='V1',released_at=datetime.now(),notes='blah blah')

#     modelv.save()
#     print(modelv.get_deferred_fields())
#     ###

#     input=np.array([1, 2, 1, 5])
#     output=np.array(tree.predict(input))
    
#     print(output)
#     queryinput=json.dumps(input.tolist())
#     queryoutput=json.dumps(output.tolist())
#     print("they are jsonsss now")
#     query = Query(
#     model=m,
#     modelv=modelv,
#     query_input=queryinput,
#     query_output=queryoutput
#     )
#     query.save()
#     print(query)
#     print(query.pk)
#     e=tree.explain_local(input,output) 
#     print("the explaination is: ",str(e._internal_obj))
    
#     decision=(e._internal_obj.get('specific')[0]).get('decision')
#     pre=(e._internal_obj.get('specific')[0]).get('perf').get('predicted_score')
#     TheExp="The decision was made with these steps: from node "
#     for d in decision:
#         if (d==decision[-1]):
#             TheExp+=str(d)+", so the taken decition is "+str(pre)+ " :)"
#         else:
#             nodes=(e._internal_obj.get('specific')[0]).get('nodes')
#             for n in nodes:
#                 if (n.get('data').get('id')==str(d)):
#                     f=n.get('data').get('label')    

#             TheExp+= str(d)+" the feature "+f
#             TheExp+=" then it goes to the node"
    
#     print("dddddddddd",TheExp)
#     # show(e)
#     print(tree.feature_names_in_)
#     print(tree.feature_types_in_)
#     exp=query.explain()

#     print("ffffffff",exp)    
#     # Convert the explanation to a dictionary
    
#     pickled_object = pickle.dumps(exp)
#     un_pickled_object=pickle.loads(pickled_object)
#     print(un_pickled_object)

#     # d=e.__dict__
#     # print(e._internal_obj["overall"])
#     # j=json.dumps(e)
#     #print(d)

#     #show(e)

#     # print(f"Explanation saved")
#     # explainationObj=Explanation(
#     #     query=query,
#     #     explanation_type="self_expanatory",
#     #     explain_input=query.query_output,
#     #     rate=0,
#     #     explain_output=query.query_input
#     # )
#     # explainationObj.save()
#     # print("the exp is",explainationObj)
    
"""
    q=Query(input,tree,m)
    output=q.query_output

    e=Explanation(q)
    o=e.explain_output
 """


""""
{'overall': None, 'specific': [{'type': 'tree', 'features': ['feature_0000', 'feature_0001', 'feature_0002', 'feature_0003'],
                                'nodes': [{'data': {'id': '1', 'label': 'feature_0002 <= -0.07\n# Obs: 0, 0', 'feature': 'feature_0002'}}, 
                                            {'data': {'id': '2', 'label': 'feature_0002 <= -0.43\n# Obs: 0, 0', 'feature': 'feature_0002'}},
                                            {'data': {'id': '3', 'label': 'feature_0000 <= -1.81\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '4', 'label': 'Impurity: 0.41\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '5', 'label': 'Impurity: 0.17\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '6', 'label': 'feature_0000 <= -0.63\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '7', 'label': 'Impurity: 0.24\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '8', 'label': 'Impurity: 0.40\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '9', 'label': 'feature_0000 <= -0.09\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '10', 'label': 'feature_0000 <= -0.77\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '11', 'label': 'Impurity: 0.07\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '12', 'label': 'Impurity: 0.50\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '13', 'label': 'feature_0002 <= 0.03\n# Obs: 0, 0', 'feature': 'feature_0002'}},
                                            {'data': {'id': '14', 'label': 'Impurity: 0.28\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '15', 'label': 'Impurity: 0.00\n# Obs: 0, 1', 'feature': None}}],
                                'edges': [{'data': {'source': '3', 'target': '4', 'edge_weight': 0.13125}},
                                          {'data': {'source': '3', 'target': '5', 'edge_weight': 6.6}},
                                          {'data': {'source': '6', 'target': '7', 'edge_weight': 0.525}},
                                          {'data': {'source': '6', 'target': '8', 'edge_weight': 0.54375}},
                                          {'data': {'source': '2', 'target': '3', 'edge_weight': 6.731249999999999}},
                                          {'data': {'source': '2', 'target': '6', 'edge_weight': 1.0687499999999999}},
                                          {'data': {'source': '10', 'target': '11', 'edge_weight': 2.00625}},
                                          {'data': {'source': '10', 'target': '12', 'edge_weight': 1.36875}},
                                          {'data': {'source': '13', 'target': '14', 'edge_weight': 0.11249999999999999}},
                                          {'data': {'source': '13', 'target': '15', 'edge_weight': 3.7125}},
                                          {'data': {'source': '9', 'target': '10', 'edge_weight': 3.375}},
                                          {'data': {'source': '9', 'target': '13', 'edge_weight': 3.825}},
                                          {'data': {'source': '1', 'target': '2', 'edge_weight': 7.800000000000001}},
                                          {'data': {'source': '1', 'target': '9', 'edge_weight': 7.199999999999999}}],
                                'decision': array([ 1, 9, 13, 15]),
                                'perf': {'is_classification': True, 'actual': nan, 'predicted': 1, 'actual_score': nan, 'predicted_score': 1.0}}]}
"""