### IMPORTANT CONFIGS !!!

USE_GEN_IMAGES = False
SAVE_GEN_IMAGES = True
#keep all generated frames in memory for use, other wise limit cache
CACHE = True 


BASE_NEG_PROMPT = "vase, clay, cartoon, anime, 3d, painting, b&w, pottery, colorful, fake, bright, blue, bowl, grass, text, brick "



models =[
    "SD1.5\\cccb_burn_400.safetensors", 
    "SD1.5\\cccb.safetensors",
    "SD1.5\\calabash2-200-realistic.safetensors",
    # "SD1.5\\calabash_aerial.safetensors" # cropping this out because it produces pottery shapes :(
 ]

model_pos_prompts = {
    "SD1.5\\calabash_aerial.safetensors": "xyz calabash, circle, hight quality, side lighting, closeups, organic, squash imperfect",
    "SD1.5\\cccb_burn_400.safetensors" : "photo of cccb, circle, high quality, organic",   # add calabash?
    "SD1.5\\cccb.safetensors": "photo of a cccb calabash, textured background", # can take out textured background for closer to original look
    "SD1.5\\calabash2-200-realistic.safetensors" : "photo of xyz calabash, circle, organic, squash, high quality, photo realistic"
}

model_neg_prompts = {
    "SD1.5\\calabash_aerial.safetensors": BASE_NEG_PROMPT,
    "SD1.5\\cccb_burn_400.safetensors": BASE_NEG_PROMPT,
    "SD1.5\\cccb.safetensors":  BASE_NEG_PROMPT,
     "SD1.5\\calabash2-200-realistic.safetensors": BASE_NEG_PROMPT,
}


samplers = [
            "euler", 
            # "euler_ancestral", 
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

schedulers = ["normal", 
            "karras", 
            "exponential", 
            "sgm_uniform", 
            "simple", 
            "ddim_uniform"
              ]

