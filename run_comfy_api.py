#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint
[]
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import random
import os
import moviepy.video.io.ImageSequenceClip
import parameters
from datetime import datetime
# import comfyui_helpers
from os import listdir
from os.path import isfile, join
from PIL import Image
import io
# import parameters


# need to replace these paths
# path_to_macros = "C:\Users\mkski\ComfyUI_windows_portable_nvidia_cu121_or_cpu\ComfyUI_windows_portable\ComfyUI\input\macros"
# path_to_calabashes = "C:\Users\mkski\ComfyUI_windows_portable_nvidia_cu121_or_cpu\ComfyUI_windows_portable\ComfyUI\input\calabashes"

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
BASE_DIR = os. getcwd() 
ALL_FRAMES_PATH = BASE_DIR+"\\all_frames\\"
GEN_IMAGES_PATH = BASE_DIR+"\\generated_images\\"
SPECIAL_MODELS_PATH = BASE_DIR+"\\special_models\\"
img_count = 0

# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



# -------------------------------------------------------------------------------------
#
#                                   API ENDPOINTS
#
#--------------------------------------------------------------------------------------

# frames get stored to /all_frames dir and get cleared at each run.

# keyframes - number of keyframes (pre-interpolation) > keyframes = more output
# source_dir - where images are being queried from
# hold_for_frames - how long to pause between morphing 
# denoise - (.2 - .6) determines how much macros are merged with calabashes, highier value -> more calabash is incorporated between keyframes


def simple_interpolate_api(keyframes=2, src_dir="macros", hold_for_frames=12, denoise=.6):
    clear_folder(ALL_FRAMES_PATH)
    clear_folder(SPECIAL_MODELS_PATH)
    if(parameters.USE_GEN_IMAGES):
        print("\n!!! Overriding input parameter 'src_dir' Using Generated Images !!!\n")
        src_dir="generated_images"
    pause_interpolate(keyframes, src_dir, hold_for_frames, denoise)


# keyframes - number of keyframes (pre-interpolation) > keyframes = more output
# source_dir - where images are being queried from
# hold_for_frames - how long to pause between morphing 
# denoise - (.2 - .6) determines how much macros are merged with calabashes, highier value -> more calabash is incorporated between keyframes

def calabash_model_api(keyframes=3, model="SD1.5\\cccb_burn_400.safetensors", hold_for_frames=6, circle=True):
    clear_folder(ALL_FRAMES_PATH)
    clear_folder(SPECIAL_MODELS_PATH)
    generate_with_trained_models(keyframes, model, hold_for_frames, circle)
# def trained_models_api(keyframes, model):
    # 1. generate key frames, interpolate, upscale, prompt pos, prompt neg


    


# -------------------------------------------------------------------------------------
#
#                                   API ENDPOINTS
#
#--------------------------------------------------------------------------------------



# change any parameters here
numframes = random.randint(1, 10)
ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))



# -------------------------------------------------------------------------------------
#
#                               PAUSE_INTERP ON DATASET
#
#--------------------------------------------------------------------------------------

def pause_interpolate(keyframes, source_dir, hold_for_frames, denoise):
    print(f"keyframes: {keyframes}" )
    print(f"hold_for_frames: {hold_for_frames}" )
    print(f"source_dir: {source_dir}" )
    print(f"denoise: {denoise}" )

    json_upscale_frames = json.loads(upscale_frames)
    json_simple_interpolation = json.loads(simple_interpolation)
    json_image_animate = json.loads(image_animate)

    # using datetime module
    import time;
    # ct stores current time
    ct = time.strftime("%Y%m%d-%H%M%S")
    
    lastKeyFrame = ""
    source_dir_ = "/"+source_dir+"/"

    # randomize params

    seed=round(datetime.now().timestamp()*1000)
    # print(f"seed-{seed}")
    sampler = parameters.samplers[random.randint(0, len(parameters.samplers)-1)]
    # print(f"sampler-{sampler}")
    json_image_animate["29"]["inputs"]["sampler_name"] = sampler
    scheduler = parameters.schedulers[random.randint(0, len(parameters.schedulers)-1)]
    # print(f"scheduler-{scheduler}")
    json_image_animate["29"]["inputs"]["scheduler"] = scheduler
    json_image_animate["29"]["inputs"]["denoise"] = denoise


    # print(filename)
    json_image_animate["2"]["inputs"]["multiplier"] = hold_for_frames
    json_image_animate["29"]["inputs"]['seed'] = seed
    denoise_valid = str(round(denoise * 10))
    file_prefix = str(ct) + "-" + source_dir + "-" + str(seed) + "-" + sampler + "-" + scheduler +"-" + denoise_valid


    for x in range(keyframes):
        # print(f"keyframe-{x}")

        if(x==0):
            filename = get_random_file(source_dir_)
        else: 
            filename = lastKeyFrame

        # part 1 animation     

        json_image_animate["26"]["inputs"]["image"] = BASE_DIR + source_dir_ + filename
        images = get_images(ws, json_image_animate)
        last_img = save_images(images, "all_frames", True)

        # part 2 interpolation 

        json_simple_interpolation["33"]["inputs"]["image"] = BASE_DIR + "\\all_frames\\" + last_img
        filename = get_random_file(source_dir_)
        lastKeyFrame = filename
        json_simple_interpolation["34"]["inputs"]["image"] = BASE_DIR + source_dir_ + filename
        images = get_images(ws, json_simple_interpolation)
        save_images(images,"all_frames", False)

    
    # part 3 upscaling 

    json_upscale_frames["13"]["inputs"]["directory"] = BASE_DIR + "\\all_frames"
    images = get_images(ws, json_upscale_frames)

    clear_folder(BASE_DIR+"\\all_frames")
    save_images(images, "all_frames", False)

    # save video to output directory
    # COMMENT OUT TO SAVE SPACE ON DRIVE ****************
    print(f"saving {file_prefix}")
    # images = get_images(ws, json_combine_frames) 

    save_video(file_prefix, BASE_DIR + "/all_frames")







# -------------------------------------------------------------------------------------
#
#                          CREATE WITH CALABASH TRAINED MODELS
#
#--------------------------------------------------------------------------------------


def generate_with_trained_models(keyframes, model, hold_for_frames, circle):
    print(f"model: {model}" )
    print(f"keyframes: {hold_for_frames}" )
    print(f"hold for frames: {hold_for_frames}" )
    print(f"circle: {circle}" )

    json_upscale_frames = json.loads(upscale_frames)
    json_circle_special_model = json.loads(circle_special_model)
    json_special_model = json.loads(special_model)
    json_simple_interpolation = json.loads(simple_interpolation)


    # json_special_model['4']['inputs']['ckpt_name'] = "SD1.5\\cccb.safetensors"
    # json_special_model['4']['inputs']['ckpt_name'] = "SD1.5\\calabash_aerial.safetensors"
    json_special_model['4']['inputs']['ckpt_name'] = model 
    # positive prompr
    json_special_model['6']['inputs']['text'] = parameters.model_pos_prompts[model]
    # negative prompt
    json_special_model['7']['inputs']['text'] = parameters.model_neg_prompts[model]
    json_circle_special_model["19"]["inputs"]["text"] = parameters.model_pos_prompts[model]
    json_circle_special_model["20"]["inputs"]["text"] = parameters.model_neg_prompts[model]
    json_circle_special_model['18']['inputs']['ckpt_name'] = model

    
    for x in range(keyframes):
        seed =  round(datetime.now().timestamp()*1000)
        json_special_model['3']['inputs']['seed'] = seed
        json_circle_special_model['21']['inputs']['seed'] = seed
        images = ""
        # print("getting frames")
        if(circle):
            images = get_images(ws, json_circle_special_model)
        else: 
            images = get_images(ws, json_special_model)
        # print(images)
        save_images(images,  "all_frames", True)
        # print("got frames")

    global img_count
    img_count = 0

    # testing above
    interpolate_between_frames(ALL_FRAMES_PATH, hold_for_frames, json_simple_interpolation, "special_models")
    print("upscaling frames")
    json_upscale_frames["13"]["inputs"]["directory"] = BASE_DIR + "\\special_models"
    images = get_images(ws, json_upscale_frames)
    print("successfully upscaled.")
    clear_folder(SPECIAL_MODELS_PATH)
    save_images(images, "special_models", False)
    # duplicate_every_nth_frame(BASE_DIR+"\\special_models")
    file_prefix = str(model + "-" + str(seed) + "-trained_models").replace('\\', '').replace(".", "").replace('/', '')
    save_video(file_prefix, BASE_DIR + "/special_models")



def interpolate_between_frames(path, frames, wf, folder):
    count = 0
    print("interpolate between: " + path)
    for filename in os.listdir(path):
        print(f"{filename}")
        if(count==0):
            previous = filename
            count =  count + 1
            continue
        this = filename
        wf["33"]["inputs"]["image"] = path + previous
        wf["34"]["inputs"]["image"] = path + this
        wf["2"]["inputs"]["multiplier"] = frames
        images = get_images(ws, wf)
        save_images(images, folder, False)
        count =  count + 1
        previous = this



# -------------------------------------------------------------------------------------
#
#                         COMFYUI - HELPER FUNCTIONS 
#
#--------------------------------------------------------------------------------------



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
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    # print("execution is done.")
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

def create_file_name(image_path, count):

    cstr = str(count)
    extra_zeros = 5 - len(cstr)
    return ("0" * extra_zeros) + cstr +  '.png'

def save_images(images, folder, save_for_later):
    count = 0
    file_name = ""
    for node_id in images:
        # print(str(node_id))
        for image_data in images[node_id]:
            image_path = BASE_DIR +"/"+ folder +"/"
            global img_count 
            if(not os.path.isdir(folder)):
                os.mkdir(image_path)
            # output will still save if save is configured in confy ui workflow 
            # would be better to save here to have control over how ouput is saved
            file_name = create_file_name(image_path, img_count) 
            count += 1
            img_count += 1
            image = Image.open(io.BytesIO(image_data))
            image.save(image_path + file_name)
            gen_img_name = file_name
            if(parameters.SAVE_GEN_IMAGES and save_for_later):
                if(parameters.STORE_ALL_GEN_IMAGES):
                    gen_img_name = str(round(datetime.now().timestamp()*1000)) +'.png' 
                image.save(GEN_IMAGES_PATH + gen_img_name)
    return file_name


def get_random_file(path):
    files = os.listdir(BASE_DIR + path)
    # Filtering only the files.
    filenum = random.randint(0, len(files)-1)
    return files[filenum]

def save_video(video_name, image_folder):
    fps=12
    dirFiles = os.listdir(image_folder)
    dirFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    image_files = [os.path.join(image_folder,img)
                for img in os.listdir(image_folder)
                if img.endswith(".png")]

    
    os.chdir(BASE_DIR + "/output")
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(video_name+'.mp4')


    # clear folder before run


if(not os.path.isdir(GEN_IMAGES_PATH)):
    os.mkdir(GEN_IMAGES_PATH)

clear_folder(ALL_FRAMES_PATH)
clear_folder(SPECIAL_MODELS_PATH)


with open("workflows/image_animate_api2.json", "r", encoding="utf-8") as f:
    image_animate = f.read()

# load comfy workflows
with open("workflows/specialized_model_api.json", "r", encoding="utf-8") as f:
    special_model = f.read()
            # load comfy workflows
with open("workflows/simple_interpolation_load_from_path_api.json", "r", encoding="utf-8") as f:
    simple_interpolation = f.read()
    
with open("workflows/upscale720x1080_api.json", "r", encoding="utf-8") as f:
    upscale_frames = f.read()

        # load comfy workflows
with open("workflows/circle_calabash_api.json", "r", encoding="utf-8") as f:
    circle_special_model = f.read()



