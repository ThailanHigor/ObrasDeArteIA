import requests
import json

url = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/fed35364-6f4e-4d46-98db-b13c4389e2d7/classify/iterations/Iteration1/url'

headers = {'Content-Type': 'application/json', 'Prediction-Key':'8fb419f53f064296bbaafd37fcba6d63'}
data = {'url': 'https://i.pinimg.com/originals/a0/a6/cd/a0a6cd8b502b5f4191ef0a14607ac6e0.jpg'}

resp = requests.post(url=url, headers=headers, data=json.dumps(data))
dataresp = resp.json() # Check the JSON Response Content documentation below
print(resp)
print(dataresp['predictions'])