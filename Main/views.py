from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyttsx3
import speech_recognition as sr
import time
import json
import pymysql
db_host = '127.0.0.1'
db_user = 'root'
db_password = '1234'
db_name = 'new_schema'
json_data=""
@csrf_exempt
def say(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        print(text)
        if text:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()
        return JsonResponse({'status': 'success', 'message': 'Text spoken successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are supported'})

@csrf_exempt
def takeCommand(request):
    if request.method == 'POST':
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 0.9
                print("Listening...")
                start_time = time.time()  # Start the timer
                audio = r.listen(source)
                end_time = time.time()  # End the timer after capturing the audio
                response_time = end_time - start_time  # Calculate the response time
                print(f"Response time: {response_time} seconds")
                print("Recognizing...")
                query = r.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return JsonResponse({'status': 'success', 'query': query})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Some Error Occurred.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are supported'})

def home(request):
    return render(request, 'home.html')
def index(request):
    return render(request, 'index.html')
# Database configuration

@csrf_exempt
def update_feedback(request):
    print("apicalled")
    if request.method == 'POST':
        data = json.loads(request.body)
        feedback = data.get('feedback')
        answer = data.get('answer')
        print('feedback')
        if not feedback or not answer:
            return JsonResponse({'error': 'Feedback and conversation_id are required'}, status=400)

        try:
            connection = pymysql.connect(host=db_host,
                                         user=db_user,
                                         password=db_password,
                                         database=db_name,
                                         cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "UPDATE Conversations SET feedback = %s WHERE answer_text = %s"
                cursor.execute(sql, (feedback, answer))
                connection.commit()

            connection.close()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)