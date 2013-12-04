from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, loader
from django.utils import simplejson
from datetime import datetime
from frontend.models import Task

# Create your views here.
def index(request):
    if 'when' in request.GET:
        today = request.GET['when']
    else:
        today = datetime.now()

    return render_to_response(
        "tasks/list.html",
        {'lista': Task.objects.filter(when=today)},
        RequestContext(request)
    )

def create(request):
    task = Task()
    task.when = datetime.now().strftime('%Y-%m-%d')
    task.save()
    return HttpResponse(task.id, mimetype='application/json')

def start_time(request):
    t = Task.objects.get(id=request.GET['id'])
    t.what = request.GET['what']
    t.from_hour = request.GET['from_hour']
    t.save()
    return HttpResponse('1')

def stop_time(request):
    t = Task.objects.get(id=request.GET['id'])
    t.to_hour = request.GET['to_hour']
    t.save()
    return HttpResponse('1')

def save(request):
    t = Task.objects.get(id=request.GET['id'])
    t.what = request.GET['what']
    t.from_hour = request.GET['from_hour'] + ':00' if request.GET['from_hour'] else None
    t.to_hour = request.GET['to_hour'] + ':00' if request.GET['to_hour'] else None
    t.save()
    return HttpResponse(simplejson.dumps({ 'delta': t.delta }), mimetype='application/json')

def add_task(request):
    if request.POST and request.POST['new_task_name']:
        Task(
            name=request.POST['new_task_name'],
            priority=request.POST['priority']
        ).save()
    return HttpResponseRedirect(reverse("frontend.views.index"))

def action(request):
    result = { 'success': False }
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'id') and GET.has_key(u'action'):
            r = (globals()[GET['action']])(GET)
            result = { 'success': True }
            if isinstance(r, dict):
                result.update(r)
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

def delete_task(GET):
    get_object_or_404(Task, id=GET['id']).delete()
