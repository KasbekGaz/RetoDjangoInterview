from django.shortcuts import render, get_object_or_404
from django.db.models import F
#from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
#from django.template import loader
from .models import Question, Choice
from django.urls import reverse
from django.views import generic

# pagina principal
'''
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)
'''
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Devuelve las 5 primeras preguntas publicadas."""
        return Question.objects.order_by("-pub_date")[:5]

# detalles
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/details.html", {"question": question})
'''
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

# resultados
'''
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})
'''
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# votar
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # vuelve a mostrar el formulario de votacion de preguntas
         return render(
            request,
            "polls/details.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        #Siempre devuelve un HttpResponseRedirect después de tratar con éxito
        # con los datos POST esto evita que los datos se publiquen dos veces si
        #el usuario presiona el botón Atrás
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



