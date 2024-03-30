### IMPORTANT CONFIGS !!!

USE_GEN_IMAGES = True
SAVE_GEN_IMAGES = True
#keep all generated frames in memory for use, other wise limit cache
CACHE = True 


BASE_NEG_PROMPT = "cartoon, anime, 3d, painting, b&w, pottery, colorful, fake, bright, blue, bowl, grass, text, "



models =[
    "SD1.5\\cccb_burn_400.safetensors", 
    "SD1.5\\cccb.safetensors",
    # "SD1.5\\calabash2-200-realistic.safetensors",
    "SD1.5\\calabash_aerial.safetensors"
 ]

model_pos_prompts = {
    "SD1.5\\calabash_aerial.safetensors": "xyz calabash, hight quality, side lighting, closeups, circle, organic, gourd, imperfect",
    "SD1.5\\cccb_burn_400.safetensors" : "photo of cccb, circle, high quality",   # add calabash?
    "SD1.5\\cccb.safetensors": "photo of a cccb calabash, textured background" # can take out textured background for closer to original look
    "SD1.5\\calabash2-200-realistic.safetensors" : "xyz calabash, organic, squash"
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

