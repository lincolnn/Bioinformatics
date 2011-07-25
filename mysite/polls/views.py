# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from polls.models import Choice, Poll
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from.django.views.generic import DetailView, ListView

def index(request):

    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]

    context = {'latest_poll_list': latest_poll_list}

    return render_to_response('polls/index.html',context) 

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})

def vote(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls.views.results', args=(p.id,))
        )

def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
        c = {'poll': p}
    except Poll.DoesNotExist:
        raise Http404
        
    return render_to_response(
        'polls/detail.html',
        {'poll': p},                       
        context_instance=RequestContext(request)
    )

    
 
