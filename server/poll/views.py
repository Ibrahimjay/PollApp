# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]    
    contex = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'poll/index.html', contex)


def details(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "poll/details.html", {'question': question})

def results(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    return render(request, "poll/results.html", context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
# Redisplay the question voting form.
        return render(request, 'poll/details.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
# Always return an HttpResponseRedirect after successfully dealing
# with POST data. This prevents data from being posted twice if a
# user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))