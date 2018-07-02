# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from forms import UploadedImageForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import requests
import json

# /detect/
def home(request):
    if (request.method == 'POST'):
        form = UploadedImageForm(request.POST, request.FILES)
        uploaded_img = request.FILES['uploaded_file']

        if form.is_valid():
            form.save()
            
            print uploaded_img.name
            res = requests.get(request.build_absolute_uri(reverse('analyze:analyze')), params={'location': uploaded_img.name})
            
            if (res.status_code == 200):
                print res.json()
                res = res.json()

                res = json.dumps(res, indent=4, sort_keys=True)
            else:
                res = "Error in getting the request!"

    else:
        form = UploadedImageForm()
        uploaded_img = 0
        res = 0

    # return render(request, 'home.html', {'form':form})
    return render(request, 'home.html', {'form':form, 'uploaded_img':uploaded_img, 'result': res})


