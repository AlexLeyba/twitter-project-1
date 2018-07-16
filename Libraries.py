from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from Messages.models import UserMessages, Likes, ContentType, Musician, Album, Trees
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from _datetime import datetime
import asyncio
from django.db import connection
from django.db.models import Q, Max