import requests

api_url = "https://zk7qrgpllsqutxwtz7xqfjfnxm0nezko.lambda-url.eu-north-1.on.aws/"

# The 8 features the model expects
# MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
data = {
    "features": [8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5555, 37.88, -122.23]
}

response = requests.post(api_url, json=data)

if response.status_code == 200:
    print("Success!")
    print(response.json())
else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)