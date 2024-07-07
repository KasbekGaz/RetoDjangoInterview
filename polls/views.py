from django.shortcuts import render, get_object_or_404
from django.db.models import F
#from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
#from django.template import loader
from .models import Question, Choice
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from .forms import QuestionForm

# pagina principal
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """Devuelve las 5 primeras preguntas publicadas."""
        return Question.objects.order_by("-pub_date")[:5]

# detalles
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

# resultados
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
        #Aqui se evita que los resultados se muestren dos veces si el usuario usa el botón atrás
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# Formulario de crear y actualizar.
class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index") #redirige al index

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")