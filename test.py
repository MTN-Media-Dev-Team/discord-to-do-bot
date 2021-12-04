import json

channels = [["channel1", "message1"], ["channel2", "message2"]]

print(json.dumps(channels))

print(channels)

print(json.loads(json.dumps(channels)))

for channel in channels:
    print(channel[0])
    print(channel[1])