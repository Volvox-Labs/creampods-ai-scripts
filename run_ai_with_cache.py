
import run_comfy_api  
import random
import parameters
import time 
import time
import os

BASE_DIR = os. getcwd() 
ALL_FRAMES_PATH = BASE_DIR+"\\all_frames\\"
GEN_IMAGES_PATH = BASE_DIR+"\\generated_images\\"


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

# This script or any python script calling the apis should be called from a batch script in 
# case of crash it will restart the client. 

start_time = time.time()
TOTAL_RUNS = 10000


#random model
model_idx = random.randint(0,len(parameters.models)-1)
model = parameters.models[model_idx]

# Whether or not to constrain the calabash generation to a centered circle. This is produce not great low res images so lets keep it off
circle_true = False

# hold_for_frames_idx = random.randint(1, 3)
# hold_for_frames = hold_for_frames_idx * 4
# try: 

#after a certain number of runs we might want to clear the generated images folder 

denoise_vals = [.5, .6, .7, .8, .9]
denoise_idx = random.randint(0, len(denoise_vals)-1)
denoise = denoise_vals[denoise_idx]


for x in range(TOTAL_RUNS):
    parameters.USE_GEN_IMAGES = False 
    parameters.SAVE_GEN_IMAGES = True
    print("\n"+str(x) + " run\n")
    model_idx = random.randint(0,len(parameters.models)-1)
    model = parameters.models[model_idx]

    # example of API call to simple interpolate. This name is deceiving (sorry :(), there is a custom model used in this 
    # api that generates new calabash forms between frames randomly selected from the src_dir. The highier the denoise value
    # the more the model is used and the input images are changed.
    if(random.randint(0,1)):
        run_comfy_api.simple_interpolate_api(keyframes=10, src_dir="calabash", hold_for_frames=6, denoise=denoise)
    else:
        run_comfy_api.calabash_model_api(keyframes=5, model=model, hold_for_frames=12, circle=circle_true)

    #Sometimes we want to clear the cache to change up the results 
    #clear_folder(ALL_FRAMES_PATH)
    for y in range(10):
        parameters.USE_GEN_IMAGES = True
        parameters.SAVE_GEN_IMAGES = random.randint(0,1)
        run_comfy_api.simple_interpolate_api(keyframes=10, src_dir="calabash", hold_for_frames=6, denoise=denoise)
    
    if(random.randint(0,1)):
        clear_folder(GEN_IMAGES_PATH)

    # run_comfy_api.calabash_model_api(keyframes=6, model=model, hold_for_frames=6, circle=circle_true)
    

# Calculate total time taken
total_time = time.time() - start_time

# Convert total time to hours and minutes
hours, remainder = divmod(total_time, 3600)
minutes, seconds = divmod(remainder, 60)

print("\n\n--- Execution time: %s hours, %s minutes, %s seconds ---\n\n" % (hours, minutes, seconds))

# except: 