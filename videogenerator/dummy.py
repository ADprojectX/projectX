# import os
# print(os.listdir(os.getcwd()))
import subprocess
path ='/Users/ad_demon/Documents/GitHub/projectX/OBJECT_STORE/12/54/output/a_brain_with_gears_turning_inside.mp4'

# Run the terminal command
command = "whisperx ${path} --model medium.en --output_dir . --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --align_extend 2"
subprocess.run(command, shell=True)