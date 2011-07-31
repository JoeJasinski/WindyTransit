from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def index(request, template_name=""):
    context = {}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
