from django.shortcuts import render
from googletrans import Translator
from gtts import gTTS
from .models import TranslationHistory
import os
from django.conf import settings

def index(request):
    translated_text = ""
    audio_url = None

    if request.method == "POST":
        text1 = request.POST.get("text")
        con_l = request.POST.get("language")

        translator = Translator()
        convert_en = translator.translate(text1, dest=con_l)
        translated_text = convert_en.text

        TranslationHistory.objects.create(
            original_text=text1,
            translated_text=translated_text,
            language=con_l
        )

        tts = gTTS(text=translated_text, lang=con_l)

        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        file_path = os.path.join(settings.MEDIA_ROOT, "output.mp3")
        tts.save(file_path)

        audio_url = settings.MEDIA_URL + "output.mp3"

    history = TranslationHistory.objects.all().order_by("-created_at")

    return render(request, "index.html", {
        "translated_text": translated_text,
        "audio_url": audio_url,
        "history": history
    })
