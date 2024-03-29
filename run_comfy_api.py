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
import comfyui_helpers
# import parameters

# need to replace these paths
# path_to_macros = "C:\Users\mkski\ComfyUI_windows_portable_nvidia_cu121_or_cpu\ComfyUI_windows_portable\ComfyUI\input\macros"
# path_to_calabashes = "C:\Users\mkski\ComfyUI_windows_portable_nvidia_cu121_or_cpu\ComfyUI_windows_portable\ComfyUI\input\calabashes"

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
BASE_DIR = os. getcwd() 

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
# denoise - (.4 - .8) determines how much macros are merged with calabashes, highier value -> greater calabash noise


def simple_interpolate_macros_api(keyframes=3, src_dir="calabash", hold_for_frames=8, denoise=.6):
    pause_interpolate(keyframes, src_dir, hold_for_frames, denoise)


# def trained_models_api(keyframes, model):
    # 1. generate key frames, interpolate, upscale


    


# -------------------------------------------------------------------------------------
#
#                                   API ENDPOINTS
#
#--------------------------------------------------------------------------------------



# change any parameters here
numframes = random.randint(1, 10)
ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))




def pause_interpolate(keyframes, source_dir, hold_for_frames, denoise):

        # load comfy workflows
    with open("workflows/simple_interpolation_load_from_path_api.json", "r", encoding="utf-8") as f:
        simple_interpolation = f.read()

    with open("workflows/upscale_api.json", "r", encoding="utf-8") as f:
        upscale_frames = f.read()

    with open("workflows/image_animate_api2.json", "r", encoding="utf-8") as f:
        image_animate = f.read()

    json_simple_interpolation = json.loads(simple_interpolation)
    json_upscale_frames = json.loads(upscale_frames)
    json_image_animate = json.loads(image_animate)


    # using datetime module
    import time;
 
    # ct stores current time
    ct = time.strftime("%Y%m%d-%H%M%S")
    # print("current time:-", ct)

    
    lastKeyFrame = ""
    source_dir_ = "/"+source_dir+"/"

    # randomize params

    seed=random.randint(0, 1000000)
    # print(f"seed-{seed}")
    sampler = parameters.samplers[random.randint(0, len(parameters.samplers)-1)]
    # print(f"sampler-{sampler}")
    json_image_animate["29"]["inputs"]["sampler_name"] = sampler
    scheduler = parameters.schedulers[random.randint(0, len(parameters.schedulers)-1)]
    # print(f"scheduler-{scheduler}")
    json_image_animate["29"]["inputs"]["scheduler"] = scheduler
    denoise_idx = random.randint(2, 3)
    denoise = .2 + (denoise_idx * .2)
    # print(f"denoise-{denoise}\n\n")
    json_image_animate["29"]["inputs"]["denoise"] = denoise
    # hold_for_frames_idx = random.randint(1, 3)
    # hold_for_frames = hold_for_frames_idx * 4


    # print(filename)
    json_image_animate["2"]["inputs"]["multiplier"] = hold_for_frames
    json_image_animate["29"]["inputs"]['seed'] = seed
    denoise_valid = str(round(denoise * 10))
    file_prefix = str(ct) + "-" + source_dir + "-" + str(seed) + "-" + sampler + "-" + scheduler +"-" + denoise_valid
    # json_combine_frames["8"]["inputs"]["filename_prefix"] = file_prefix


    for x in range(keyframes):
        # print(f"keyframe-{x}")

        if(x==0):
            filename = comfyui_helpers.get_random_file(source_dir_)
        else: 
            filename = lastKeyFrame

        # part 1 animation     

        json_image_animate["26"]["inputs"]["image"] = BASE_DIR + source_dir_ + filename
        images = comfyui_helpers.get_images(ws, json_image_animate)
        last_img = comfyui_helpers.save_images(images, "all_frames", 1, x)

        # part 2 interpolation 

        json_simple_interpolation["33"]["inputs"]["image"] = BASE_DIR + "\\all_frames\\" + last_img
        filename = comfyui_helpers.get_random_file(source_dir_)
        lastKeyFrame = filename
        json_simple_interpolation["34"]["inputs"]["image"] = BASE_DIR + source_dir_ + filename
        images = comfyui_helpers.get_images(ws, json_simple_interpolation)
        # save_images(images, "simple_interp")
        comfyui_helpers.save_images(images,"all_frames", 2, x)

    
    # part 3 upscaling 

    json_upscale_frames["13"]["inputs"]["directory"] = BASE_DIR + "\\all_frames"
    images = comfyui_helpers.get_images(ws, json_upscale_frames)

    comfyui_helpers.clear_folder(BASE_DIR+"\\all_frames")
    comfyui_helpers.save_images(images, "all_frames", 3, 0)

    # save video to output directory
    # COMMENT OUT TO SAVE SPACE ON DRIVE ****************
    print(f"saving {file_prefix}")
    # images = get_images(ws, json_combine_frames) 

    comfyui_helpers.save_video(file_prefix, BASE_DIR + "/all_frames")


def trained_models_api(keyframes, hold_for_frames):
    print("use model to generate frames")


    #   "4": {
    # "inputs": {
    #   "ckpt_name": "SD1.5\\cccb.safetensors"

    #   "6": {
    # "inputs": {
    #   "text": "photo of a cccb calabash, texture in background, organic, imperfect, dry",

    #   "7": {
    # "inputs": {
    #   "text": "text, watermark, ugly, rotting, white background, cgi, people, fake, colorful",


# clear folder before run
comfyui_helpers.clear_folder(BASE_DIR+"/all_frames")
simple_interpolate_macros_api()

#vlc 