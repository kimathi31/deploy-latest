import io
from PIL import Image as im
import torch
from .forms import ImageUploadForm
import datetime
from io import BytesIO
import base64
#import tensorflow as tf
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny

@api_view(['GET','POST'])
@permission_classes([AllowAny])   
def deploy(request):    
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image = request.FILES.get('image')
        img = image.file.read()
        #decode image from bytes
        encoded_img = im.open(image)
                   
        path_hubconfig = "detectapi/yolov5"
        path_weightfile = "detectapi/model/firstmodelsimilarfeatures.pt"
        path_weightfile2 = "detectapi/model/latestversion2.pt"
                        
        #model = torch.hub.load('ultralytics/yolov5', 'custom',
        #                        path=path_weightfile,verbose=False)
        model2 = torch.hub.load(path_hubconfig,'custom',source = 'local',path=path_weightfile2,verbose=False)   
        
        results = model2(encoded_img, size=608)
        results.render()        
        
        #save base64
        for img in results.ims:
            img_base64 = im.fromarray(img)
            byte = BytesIO()
            img_base64.save(byte,'jpeg')
            img_base64 = base64.b64encode(byte.getvalue())

        results = results.pandas().xyxy[0]
        Disease = results.name
        Disease = ','.join(Disease)

        
     
        if len(results)==0:
            model = torch.hub.load(path_hubconfig,'custom',source ='local',path=path_weightfile,verbose=False)
            results2 = model(encoded_img,size=640)
            results2.render() 
            for img in results2.ims:
                img_base64 = im.fromarray(img)
                byte = BytesIO()
                img_base64.save(byte,'jpeg')             
                img_base64 = base64.b64encode(byte.getvalue())

            results2 = results2.pandas().xyxy[0]
            Disease = results2.name
            Disease = ','.join(Disease)

         
            if len(results2)==0 and len(results)==0:                    
                alert = 'Could not make prediction for the given image.Additions are being made to the knowledge base'
                return Response({'alert':alert})
                                            
            #list of diseases
        Disease_list= crop_diseases.objects.values_list('disease')                    
                    
            #get disease details                   
        def getsymptoms(x):            
            for y in Disease_list:
                x == y
                [symptoms] = crop_diseases.objects.filter(disease = x).values_list('symptom').distinct()
                symptoms = ''.join(symptoms)
            return symptoms

        def getmeasures(x):            
            for y in Disease_list:
                x == y
                [measures] = crop_diseases.objects.filter(disease = x).values_list('measure').distinct()
                measures = ''.join(measures)
            return measures

        #Model1 query
        symptoms ={}
        for x in results.name:
            symptoms[x] = getsymptoms(x)
        
        measures ={}
        for x in results.name:
            measures[x] = getmeasures(x)

        if len(results)==0:
            #model2 query
            symptoms ={}
            for x in results2.name:
                symptoms[x] = getsymptoms(x)
            measures = {}
            for x in results2.name:
                measures[x] = getmeasures(x)
                
                
        disease_details = pd.DataFrame({'Symptoms':symptoms,'Treatment':measures})  

        symptoms = symptoms.values()
        symptoms = list(symptoms)
        symptoms = ''.join(symptoms)
        measures = measures.values()
        measures = list(measures)
        measures = ''.join(measures)
        #save to db
        post = detection()
        post.Analysis_REF_No 
        post.Disease = Disease                
        post.Date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        post.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        post.image =  img_base64.decode('utf-8')
        post.symptoms = symptoms
        post.measures = measures
        post.save()  
                                
        return Response({'Details':disease_details,'Image':img_base64})                 

@api_view(['GET'])
@permission_classes([AllowAny])   
def getdata(request):    
    if request.method == 'GET':    
        disease = detection.objects.values_list('Disease')
        date = detection.objects.values_list('Date')
        time = detection.objects.values_list('Time')
        image = detection.objects.values_list('image')
        symptoms = detection.objects.values_list('symptoms')
        measures = detection.objects.values_list('measures')
         
        data = pd.DataFrame({'Disease':disease,'Date':date,'Time':time,'Image':image,'Symptoms':symptoms,'Measure':measures})
        data = data.applymap(lambda x:x[0])   

        return Response({'data':data})