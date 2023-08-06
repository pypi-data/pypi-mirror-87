import requests
import logging
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.email
