import uuid

def process_input(topic):
    TEMPLATE = "Generate a script for youtube video on {}."
    output = TEMPLATE.format(topic)
    return output

def script_processing(temp_script):
    processed_script = temp_script.split("\n")
    new_list = []
    script_desc = []

    for i in processed_script:
        if i == " " or not i:
            continue
        new_list.append(i)
    # print(new_list)
    i = 0
    while i < len(new_list):
        # ts = SCENE.format(i)#//2
        # script_desc[str(uuid.uuid4())] = [new_list[i][11:-1]]
        script_desc.append([i, str(uuid.uuid4()), new_list[i][11:-1], None])
        i += 1
        # script_desc[ts].append(new_list[i][20:-1])
        # i += 1
    return script_desc
