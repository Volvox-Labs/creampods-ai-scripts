
import run_comfy_api  
import random
import parameters
import time 
import time

start_time = time.time()
TOTAL_RUNS = 10

#random model
model_idx = random.randint(0,len(parameters.models)-1)
model = parameters.models[model_idx]

circle_true = random.randint(0,1) 

# hold_for_frames_idx = random.randint(1, 3)
# hold_for_frames = hold_for_frames_idx * 4



#after a certain number of runs we might want to clear the generated images folder 

denoise_vals = [.2, .3, .4, .5, .6]
denoise_idx = random.randint(0, 4)
denoise = denoise_vals[denoise_idx]


for x in range(TOTAL_RUNS):
    print("\n"+str(x) + " run\n")
    model_idx = random.randint(0,len(parameters.models)-1)
    model = parameters.models[model_idx]
    circle_true = random.randint(0,1) 
    # run_comfy_api.simple_interpolate_api(keyframes=10, src_dir="calabash", hold_for_frames=6, denoise=.6)
    run_comfy_api.calabash_model_api(keyframes=10, model=model, hold_for_frames=12, circle=circle_true)

# run_comfy_api.calabash_model_api(keyframes=6, model=model, hold_for_frames=6, circle=circle_true)
    

# Calculate total time taken
total_time = time.time() - start_time

# Convert total time to hours and minutes
hours, remainder = divmod(total_time, 3600)
minutes, seconds = divmod(remainder, 60)

print("\n\n--- Execution time: %s hours, %s minutes, %s seconds ---\n\n" % (hours, minutes, seconds))