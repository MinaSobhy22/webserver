# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from yolo_model import get_analysis
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
import base64

import json
import os 

from django.core.files.uploadedfile import InMemoryUploadedFile

     
class AnalyzeAPI(APIView):
 
    def get(self, request, format=None):
        if (request.GET.get('location')):
            location = request.GET.get('location')
        else:
            return HttpResponse("Error! Must provide a location in the http request.")

        # ('bicycle',0.8530976176261902,(341.8388671875, 285.8398132324219, 492.896240234375, 323.5571594238281))
        # ('dog', 0.8239734172821045, (226.709716796875, 376.563232421875, 189.12977600097656, 289.1200256347656))
        # ('truck', 0.6358878016471863, (574.12841796875, 126.13533782958984, 212.54315185546875, 83.70974731445312))
        dir_path = os.path.dirname(os.path.realpath(__file__))

        parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir))
        image_path = parent_dir + '/media/images/' + location
        data = get_analysis({'image_path': image_path})

        if (data == -1):
            return HttpResponse("Error in the inputs.")

        # Common function for post processing on the output and construct the JSON that will be sent to the user
        output_dict = construct_output(data)

        return JsonResponse(output_dict)

    def post(self,request):
        try:
            
            data = request.data['image']
            #imgdata = base64.b64decode(data.read())  
            imgdata = base64.b64decode(data)       
            filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
            path = default_storage.save('images/api/' + filename, ContentFile(imgdata))
            image_path = os.path.join(settings.MEDIA_ROOT, path)


            #data = request.data['image']
            #print data.name
            #path = default_storage.save('images/api/' + data.name, ContentFile(data.read()))
            #image_path = os.path.join(settings.MEDIA_ROOT, path)
        except:
            return HttpResponse("Must provide an image with parameter name 'image'")

        data = get_analysis({'image_path': image_path})
        output_dict = construct_output(data)
        # print output_dict

        return JsonResponse(output_dict)




def construct_output(data):
    id = 0
    output_dict = {}
    for element in data:
        item_dict = {}
        item_dict['name'] = element[0]
        item_dict['accuracy'] = element[1]
        item_dict['x1'] = element[2][0]
        item_dict['y1'] = element[2][1]
        item_dict['x2'] = element[2][2]
        item_dict['y2'] = element[2][3]

        output_dict[id] = item_dict
        id = id + 1 

    return output_dict
