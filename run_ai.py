
import run_comfy_api  
import random
import parameters
import time 
import time

start_time = time.time()
TOTAL_RUNS = 5

#random model
model_idx = random.randint(0,len(parameters.models)-1)
model = parameters.models[model_idx]

# circle_true = random.randint(0,1) 
circle = 0

# hold_for_frames_idx = random.randint(1, 3)
# hold_for_frames = hold_for_frames_idx * 4


#  MK TO RUN 

# OTHER COMPUTERS 

# RUN MODEL #1, #2, #3  
# RUN GENERATED content on this dataset 

# dont clear cash 

# Run Calabash Dataset (different denoise levels)
# Run GENERATED CONTENT



# MK COMPUTER 

# RUN Macros on highier denoise,  --- add zoom in calabash to this dataset
# RUN GENERATED content on this data set 




#after a certain number of runs we might want to clear the generated images folder 

denoise_vals = [.2, .3, .4, .5, .6]
denoise_idx = random.randint(0, 4)
denoise = denoise_vals[denoise_idx]

def get_random_model():
    model_idx = random.randint(0,len(parameters.models)-1)
    return parameters.models[model_idx]

for x in range(TOTAL_RUNS):
    print("\n"+str(x) + " run\n")
    model = get_random_model()
    # model = "SD1.5\\calabash2-200-realistic.safetensors"
    # run_comfy_api.simple_interpolate_api(keyframes=10, src_dir="macros", hold_for_frames=6, denoise=1)
    run_comfy_api.calabash_model_api(keyframes=2, model=model, hold_for_frames=3, circle=circle)

# run_comfy_api.calabash_model_api(keyframes=6, model=model, hold_for_frames=6, circle=circle_true)
    

# Calculate total time taken
total_time = time.time() - start_time

# Convert total time to hours and minutes
hours, remainder = divmod(total_time, 3600)
minutes, seconds = divmod(remainder, 60)

print("\n\n--- Execution time: %s hours, %s minutes, %s seconds ---\n\n" % (hours, minutes, seconds))