import json
from random import randint

from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from api.permissions import SuperUserMixin
from .models import Article, ParagraphBatch, Paragraph, Question, Answer


class IndexView(TemplateView):
    template_name = "piaf/index.html"


class AdminView(TemplateView, SuperUserMixin):
    template_name = "piaf/admin.html"
    count_inserted_articles = None

    def post(self, request, *args, **kwargs):
        content = request.FILES["file"].read()
        data = json.loads(content).get("data")
        for d in data:
            article = Article(
                name=d["displaytitle"],
                theme=d["categorie"],
                reference=d.get("wikipedia_page_id"),
                audience=request.POST["audience"],
            )
            article.save()
            for (i, p) in enumerate(d["paragraphs"]):
                if i % 5 == 0:
                    batch = ParagraphBatch()
                    batch.save()
                Paragraph(batch=batch, article=article, text=p["context"]).save()
        self.count_inserted_articles = len(data)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_inserted_articles"] = self.count_inserted_articles
        return context


@method_decorator(csrf_exempt, name="dispatch")
class ParagraphApi(View):
    # Provide a randomly picked pending article.
    def get(self, request, *args, **kwargs):
        qs = ParagraphBatch.objects.filter(status="pending")
        theme = request.GET.get("theme")
        if theme:
            qs = qs.filter(paragraphs__article__theme=theme)
        batch = qs[randint(0, qs.count() - 1)]
        article = batch.article
        paragraph = batch.paragraphs.filter(status="pending").first()
        data = {"id": paragraph.id, "theme": article.theme, "text": paragraph.text}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        paragraph = Paragraph.objects.get(pk=data["paragraph"])
        paragraph.complete(data["data"], request.user)
        return HttpResponse(status=201)
