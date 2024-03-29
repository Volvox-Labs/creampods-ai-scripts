#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    # stringify client id and workflow json
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    print(f"prompt_id: {prompt_id}")
    print("prompt was queued.")
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print("execution is done.")
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output
    return output_images

with open("simple_interpolation_api.json", "r", encoding="utf-8") as f:
    workflow_jsondata = f.read()
jsonwf = json.loads(workflow_jsondata)

numframes = random.randint(1, 10)
# jsonwf["5"]["inputs"]["frame_rate"] = numframes
jsonwf["2"]["inputs"]["multiplier"] = numframes

#   "5": {
#     "inputs": {
#       "frame_rate": 8,

#set the text prompt for our positive CLIPTextEncode
# prompt["6"]["inputs"]["text"] = "xyz calabash"
# prompt["6"]["inputs"]["text"] = "fake, cartoon, low quality"

# random int generator here

#set the seed for our KSampler node
# prompt["3"]["inputs"]["seed"] = 5
print('testing')
ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, jsonwf)

#Commented out code to display the output images:

for node_id in images:
    for image_data in images[node_id]:
        from PIL import Image
        import io
        # output will still save if save is configured in confy ui workflow 
        # would be better to save here to have control over how ouput is saved
        image = Image.open(io.BytesIO(image_data))
        print(f"image: {prompt_id}")
        # image.save(f"Output-{node_id}.png")
        # image.show() #shows image in popup

