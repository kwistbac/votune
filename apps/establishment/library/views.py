# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib import messages

from django.views.generic.list import ListView
from django.utils import timezone
from mJuke.models import Song

class LibraryListView(ListView):
	template_name = 'establishment/library/list.html'
	model = Song

	def get_context_data(self, **kwargs):
		context = super(LibraryListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context

def add(request):
	return render_to_response('establishment/library/add.html')

def edit(request, id):
	return render_to_response('establishment/library/edit.html')

def remove(request, id):
	return render_to_response('establishment/library/remove.html')
