import os
import time
import json  # Make sure to import the json module

from dotenv import load_dotenv
load_dotenv()

import openai
from openai import OpenAI

from django.http import JsonResponse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import OpenAIThread
# Load API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
# Replace this with the actual assistant ID you want to use
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def ask_openai(request):
    try:
        data = json.loads(request.body)
        user_question = data.get('question')

        if not user_question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        # Check if the user already has an active thread
        user = request.user
        openai_thread, created = OpenAIThread.objects.get_or_create(
            user=user,
            defaults={'assistant_id': ASSISTANT_ID}
        )
        

        # Use the existing thread ID or create a new one if necessary
        thread_id = openai_thread.thread_id
        if created or thread_id is None:
            # If no active thread, create a new one
            thread = client.beta.threads.create()
            thread_id = thread.id
            openai_thread.thread_id = thread_id
            openai_thread.save()
        print(openai_thread.thread_id)
        # Add a User Message to the Thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_question
        )

        # Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=openai_thread.assistant_id
        )

        # Polling for the assistant's response
        while run.status in ["queued", "in_progress"]:
            time.sleep(1)  # Wait for 1 second before checking again
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

        # Retrieve all the messages in the thread
        response_messages = client.beta.threads.messages.list(thread_id=thread_id)

        # Format the messages for the front end
        conversation_history = [{
            'role': message.role,
            'content': message.content[0].text.value
        } for message in response_messages.data]

        return JsonResponse({'conversation': conversation_history})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('ask_form')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ask_form')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def ask_form(request):
    return render(request, 'assistant/ask.html')



logout_view = LogoutView.as_view(next_page=reverse_lazy('assistant/login')) 