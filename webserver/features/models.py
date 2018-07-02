# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UploadedImage(models.Model):
    uploaded_file = models.FileField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)