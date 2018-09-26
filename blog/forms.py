from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):


    class Meta(object):
        model = Article
        fields = ["title", "description", "card_image", "main_image", "featured", "tags",
                  "category",]
        exclude = ["slug","end_publish_date","last_update","start_publish_date","publish_date","status", "author",]


