# libreria de formularios por defecto
from django import forms
#importamos el modelo
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'dificultad']
