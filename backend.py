import requests
from flask import Flask, request
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

API_TOKEN_LIST = [] # removed for security purposes
API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"
API_TOKEN = random.choice(API_TOKEN_LIST)
print("API TOKEN", API_TOKEN)
user_limit = 5000
guest_limit = 1000
min_limit = 300

headers = {"Authorization": f"Bearer {API_TOKEN}"}
@app.route("/model", methods=["GET", "POST"])
def check_input():
    if request.method == 'POST':
        input = request.json['text']
        input = input.replace('"','').replace("'","")

        ### CHECK IF LINK
        if input[:5] == 'https':
            html = urlopen(input).read()
            soup = BeautifulSoup(html)

            for script in soup(["script", "style"]):
                script.decompose()

            strips = list(soup.stripped_strings)
            final_string = ''

            for i in range(len(strips)):
                final_string += strips[i]

            if not (request.json['loggedIn']):
                try:
                    response = requests.post(API_URL, headers=headers, json=final_string[:guest_limit])
                    output = response.json()
                    return (json.dumps(output[0]))
                except:
                    output = [{'summary_text': "Something went wrong... Try again!"}]
                    return (output[0])
            else:
                try:
                    response = requests.post(API_URL, headers=headers, json=final_string[:user_limit])
                    output = response.json()
                    return (json.dumps(output[0]))
                except:
                    output = [{'summary_text': "Something went wrong... Try again!"}]
                    return (output[0])

        ## TEXT

        if len(input) < min_limit:
            output = [{'summary_text': "That is not a sufficient article"}]
            return (output[0])

        if not (request.json['loggedIn']):
            try:
                response = requests.post(API_URL, headers=headers, json=input[:guest_limit])
                output = response.json()
                return (json.dumps(output[0]))
            except:
                output = [{'summary_text': "Something went wrong... Try again!"}]
                return (output[0])
        else:
            try:
                response = requests.post(API_URL, headers=headers, json=input[:user_limit])
                output = response.json()
                return (json.dumps(output[0]))
            except:
                output = [{'summary_text': "Something went wrong... Try again!"}]
                return (output[0])

if __name__ == '__main__':
   app.run(debug = True)