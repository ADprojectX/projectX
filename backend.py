import script
import openai_request as osr
import text_processing as tp
import text_to_audio as tta
import text_to_image as tti


if __name__ == '__main__':
    # topic = input()
    # voice_number = input()
    topic = 'Top 15 Psycological facts for men.'
    voice_number = 0
    processed_topic = tp.process_input(topic)
    scene_dic = tp.script_processing(script.temp_script)
    for k,v in scene_dic.items():
        # {key:[nar, img_desc, ]}
        scene_dic[k].append(tta.convert_to_audio(v[0], voice_number))
        # scene_dic[k].append(tta.convert_to_image(v[1]))
    print(scene_dic)
    # script_response = osr.request_script(processed_topic)
    
