

### IMPORTANT CONFIGS !!!

# Store all generative images - When set to true, this will keep all generated images in the generated_images directory
# When set to False images are overwritten each run.
STORE_ALL_GEN_IMAGES = True
# When set to True - Use Generative Images (Images in the generated_images folder)
# for the simple_interpolate_api run, When set to false use the src_directory parameter 
# This flag does override the src_dir parameter
USE_GEN_IMAGES = True
# When set to True - Save generated frames 
# for the simple_interpolate_api run, When set to false
SAVE_GEN_IMAGES = False


# negative prompting for all calabash generations 
BASE_NEG_PROMPT = "vase, clay, cartoon, anime, painting, b&w, pottery, colorful, fake, bright, bowl, grass, text, "


# models that are trained on subsets of the calabash dataset, each has their own style
models =[
    "SD1.5\\cccb_burn_400.safetensors", 
    "SD1.5\\cccb.safetensors",
    "SD1.5\\calabash2-200-realistic.safetensors",
    # "SD1.5\\calabash_aerial.safetensors" # taking this out because it produces pottery clay outputs sometimes.
 ]


# Positive prompting specific to each trained model, can tinker with these if you want to create variation in output but be wary, they can greatly change the 
# output so test before commiting
model_pos_prompts = {
    "SD1.5\\calabash_aerial.safetensors": "xyz calabash, high quality, side lighting, closeups, circle, organic, gourd, imperfect",
    "SD1.5\\cccb_burn_400.safetensors" : "photo of cccb, circle, high quality",   # add calabash?
    "SD1.5\\cccb.safetensors": "photo of a cccb calabash, textured background", # can take out textured background for closer to original look
    "SD1.5\\calabash2-200-realistic.safetensors" : "xyz calabash, organic, squash, high quality, photo-realistic"
}

model_neg_prompts = {
    "SD1.5\\calabash_aerial.safetensors": BASE_NEG_PROMPT,
    "SD1.5\\cccb_burn_400.safetensors": BASE_NEG_PROMPT,
    "SD1.5\\cccb.safetensors":  BASE_NEG_PROMPT,
     "SD1.5\\calabash2-200-realistic.safetensors": BASE_NEG_PROMPT,
}

# samplers ifluence the style of generated frames. I have found the uncommented ones below to be fairly consistant/good 
samplers = [
            "euler", 
            "euler_ancestral", 
            "heun", 
            "heunpp2",
            # "dpm_2",
            # "dpm_2_ancestral" 
            # "lms",
            # "dpm_fast",
            # "dpm_adaptive",
            # "dpmpp_2s_ancestral",
            # "dpmpp_sde",
            # "dpmpp_sde_gpu", f
            # "dpmpp_2m",
            # "dpmpp_2m_sde",
            # "ddpm",
            # "ddim",
            # "uni_pc",
            # "uni_pc_bh2",
            # "k_euler",
            # "k_euler_a",
            # "k_lcm",
            ]

# similar to samplers can effect style of generated frames
schedulers = ["normal", 
            "karras", 
            "exponential", 
            "sgm_uniform", 
            "simple", 
            "ddim_uniform"
              ]

