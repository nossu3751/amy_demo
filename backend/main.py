# import requests


# headers = {
#     "Authorization": "Bearer %s" % token,
# }

# payload = {
#      "power":"on",
# }

# data = {
#     "period":2,
#     "cycles":5,
#     "color":"white"
# }
# response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

# # response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', data=data, headers=headers)
# print(response.json())