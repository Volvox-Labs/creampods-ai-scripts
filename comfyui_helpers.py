from os import listdir
from os.path import isfile, join
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random
import os
import moviepy.video.io.ImageSequenceClip

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
BASE_DIR = os. getcwd() 

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
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            print("executing ?")
            message = json.loads(out)
            print(message)
            if message['type'] == 'executing':
                print("executing ??")
                data = message['data']
                print(data['node'])
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

def create_file_name(image_path, type, x, count):
    if(type == 3):
        cstr = str(count)
        extra_zeros = 5 - len(cstr)
        return ("0" * extra_zeros) + cstr +  '.png'
    else:
        return str(x) + "-" + str(type) + "-" + str(count) + '.png'

def save_images(images, folder, type, x):
    count = 0
    file_name = ""
    for node_id in images:
        # print(str(node_id))
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image_path = "./"+ folder +"/"
            if(not os.path.isdir(folder)):
                os.mkdir(image_path)
            # output will still save if save is configured in confy ui workflow 
            # would be better to save here to have control over how ouput is saved
            file_name = create_file_name(image_path,type,x,count) 
            count += 1
            image = Image.open(io.BytesIO(image_data))
            print(file_name)
            image.save(image_path + file_name)
    return file_name

def clear_folder(folder):
    import shutil
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



def get_random_file(path):
    files = os.listdir(BASE_DIR + path)
    # Filtering only the files.
    filenum = random.randint(0, len(files)-1)
    return files[filenum]

def save_video(video_name, image_folder):
    fps=8
    dirFiles = os.listdir(image_folder)
    dirFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for img in os.listdir(image_folder):
        print(img)

    image_files = [os.path.join(image_folder,img)
                for img in os.listdir(image_folder)
                if img.endswith(".png")]

    
    os.chdir(BASE_DIR + "/output")
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(video_name+'.mp4')