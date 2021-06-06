from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': ('Текст сообщения'),
            'group': ('Выберите группу'),
        }
        help_texts = {
            'text': ('Это поле для ввода текста Вашей записи. '
                     'Текст будет виден на сайте как есть.'),
            'group': ('Группа постов, она же подборка записей, в которой'
                      ' Вы желаете разместить своё сообщение.'),
        }
