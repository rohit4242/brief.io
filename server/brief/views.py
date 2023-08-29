from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from django.http import JsonResponse

model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
tokenizer = AutoTokenizer.from_pretrained("t5-small")


@csrf_exempt
def summarize_text(request):
    if request.method == "POST":
        data = request.POST.get("text", "")

        if data:
            tokens_input = tokenizer.encode(
                "summarize: " + data,
                return_tensors="pt",
                max_length=tokenizer.model_max_length,
                truncation=True,
            )

            summary_ids = model.generate(
                tokens_input,
                min_length=80,
                max_length=150,
                length_penalty=2.0,  
                num_beams=4, 
                no_repeat_ngram_size=3,
                early_stopping=True,
            )

            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            return JsonResponse({"summary": summary})
        else:
            return JsonResponse({"error": "No text provided."}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are supported."}, status=405)
