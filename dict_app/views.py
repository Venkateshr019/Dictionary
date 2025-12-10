from django.shortcuts import render
from .models import SearchHistory
from .services.dictionary import lookup_word



def home(request):
    context = {
        "query": "",
        "result": None,
        "error": "",
    }

    if request.method == "POST":
        query = request.POST.get("word", "").strip()
        context["query"] = query

        if not query:
            context["error"] = "Please enter a word to search."
        else:
            entry = lookup_word(query)
            if entry:
                context["result"] = {
                    "word": query,
                    "meanings": entry.meanings,
                    "synonyms": entry.synonyms,
                    "antonyms": entry.antonyms,
                    "examples": entry.examples,
                    "pronunciation": entry.pronunciation,
                    "pronunciation_audio": entry.pronunciation_audio,
                }
                try:
                    SearchHistory.objects.create(
                        word=query.lower(),
                        definition="; ".join(entry.meanings),
                        synonyms=", ".join(entry.synonyms),
                        antonyms=", ".join(entry.antonyms),
                        examples=" | ".join(entry.examples),
                        pronunciation=entry.pronunciation,
                    )
                except Exception:
                    pass
            else:
                context["error"] = f"No definition found for “{query}”."

    return render(request, "dict_app/home.html", context)
