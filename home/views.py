from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return HttpResponse('Your current open cases')

def login(request):
  return HttpResponse('Login to access your cases')
