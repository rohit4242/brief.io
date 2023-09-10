from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import openai

SECRET_KEY = os.getenv("SECRET_KEY")
openai.api_key = SECRET_KEY


@csrf_exempt
def summarize_text(request):
    if request.method == "POST":
        data = request.POST.get("text", "")

        if data:
            summary = summarize_text_with_chatgpt(data)
            return JsonResponse({"summary": summary})
        else:
            return JsonResponse({"error": "No text provided."}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are supported."}, status=405)


def summarize_text_with_chatgpt(text):
    # Construct the prompt for summarization
    prompt = f"Summarize the following text: {text}"

    # Call ChatGPT Turbo to generate a summary
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,  # Adjust the max_tokens for desired summary length
        n=1,  # Number of responses to generate
        stop=None,  # You can add a stop condition here if needed
        temperature=0.7,  # Adjust the temperature for creativity
    )

    # Extract the summary from the response
    summary = response.choices[0].text.strip()

    return summary
