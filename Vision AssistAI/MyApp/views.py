import json
from django.http import JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .middlewares import auth, guest

import requests
import openai


import base64
import io

import base64
import io
import tempfile





def save_base64_image_as_temp_file(base64_data):
    # Split the data URL part from the actual Base64 data
    header, encoded = base64_data.split(",", 1)
    
    # Decode the Base64 data
    image_data = base64.b64decode(encoded)
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    
    # Write the image data to the temporary file
    temp_file.write(image_data)
    temp_file.close()
    
    return temp_file.name

# In your Django app's views.py
from django.http import HttpResponse # type: ignore
from django.conf import settings # type: ignore
import os

def serve_temp_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')
    else:
        return HttpResponse("File not found", status=404)


# Imgur client ID
IMGUR_CLIENT_ID = "60660ff50bfdc0f"

# OpenAI API key
client = openai.OpenAI(
    api_key="647bab5949254a898c50e57bccda014a",
    base_url="https://api.aimlapi.com",
)

def upload_image_to_imgur(image_path):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    url = "https://api.imgur.com/3/image"
    
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(url, headers=headers, files={"image": image_file})
        
        # Print response for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        response_data = response.json()
        
        if response_data["success"]:
            return response_data["data"]["link"]
        else:
            raise Exception("Failed to upload image to Imgur: " + response_data.get("data", {}).get("error", "Unknown error"))
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    
def analyze_image(image_url):
  response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "only detect object or face and content of image"},
        {
          "type": "image_url",
          "image_url": {
            "url": image_url,
            "detail": "high"
          },
        },
      ],
    }
  ],
  max_tokens=300,
  )
  return response.choices[0].message.content


@guest
def register_view(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data={'username':'', 'password1': '', 'password2': ''}
        form=UserCreationForm(initial=initial_data)

    return render(request,'auth/register.html',{'form':form})

@guest
def login_view(request):
    
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data={'username':'', 'password1': ''}
        form=AuthenticationForm(initial=initial_data)

    return render(request,'auth/login.html',{'form':form})


@auth
def dashboard_view(request):
    return render(request,'dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def handle_image_post(request):
    if request.method == 'POST':       

        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            image_data_url = data.get('image', '')

            # Print the received image URL
            print("Received image URL:", image_data_url)
            # Path to your image
            #image_path = "C:/Users/mf19-14/llama/dri.jpg"
            image_url=" "
            try:
                temp_file_path = save_base64_image_as_temp_file(image_data_url)
                print("Temporary file path:", temp_file_path)
                image_data_url = upload_image_to_imgur(temp_file_path)
            except:
                print("temprary saving error ")                    
            print("decode url ",image_data_url)
            description = analyze_image(image_data_url)
            print(description)
            
            # Respond with the received URL for demonstration
            response_data = {'received_image_url': description}
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    



