import json
temp_script = """Narrator: "The Zeigarnik Effect states that people are more likely to remember uncompleted tasks than completed ones. This is because our brains have a natural tendency to focus on unfinished work, keeping it in our thoughts until it's completed."

"""
"""
Narrator: "Welcome to today's videos, where we'll explore 15 psychological facts that will blow your mind. Let's dive right in!"

Narrator: "Fact number 1: The Zeigarnik Effect."

Narrator: "Fact number 2: The Halo Effect."

Narrator: "The Halo Effect is a cognitive bias that causes us to form an overall impression of someone based on a single positive trait. This can lead to inaccurate judgments and even impact our decisions."

Narrator: "Fact number 3: The Power of Suggestion."

Narrator: "The power of suggestion can significantly influence our thoughts and actions. When someone suggests something to us, it can plant an idea in our minds, making us more likely to think or act in a certain way."

Narrator: "Fact number 4: The Bystander Effect."

Narrator: "The Bystander Effect is a psychological phenomenon that occurs when multiple people witness an emergency situation but fail to intervene. This is because each individual assumes someone else will take action, leading to inaction by all."

Narrator: "Fact number 5: The Mere Exposure Effect." no samjanu bro

Narrator: "The Mere Exposure Effect is a psychological phenomenon where people develop a preference for things they're exposed to repeatedly. Familiarity breeds liking, and we tend to favor things we've encountered before."

Narrator: "Fact number 6: The Placebo Effect."

Narrator: "The Placebo Effect occurs when a person experiences an improvement in their symptoms, even though they've received a treatment with no active ingredients. This demonstrates the power of our minds and how our beliefs can influence our physical health."

Narrator: "Fact number 7: The Foot-in-the-Door Technique."

Narrator: "The Foot-in-the-Door Technique is a persuasion strategy where someone agrees to a small request, making them more likely to comply with a larger request later on. This is because they've already established a pattern of compliance."

Narrator: "Fact number 8: Cognitive Dissonance."

Narrator: "Cognitive Dissonance is the mental discomfort we experience when our actions, beliefs, or attitudes are inconsistent with each other. To resolve this discomfort, we often change our beliefs or attitudes to align with our actions."
"""


img_desc = '''Image Description: A to-do list with some tasks checked off
Image Description: A brain with gears turning inside
Image Description: A woman struggling to remember an unfinished task
'''
'''
Image Description: A person with a halo above their head
Image Description: A group of people, with one person standing out due to their positive trait
Image Description: A person whispering into another person's ear
Image Description: A group of people agreeing to an idea
Image Description: A person in distress, surrounded by onlookers
Image Description: A group of people standing around, not helping in an emergency
Image Description: A person becoming more familiar with an object
Image Description: A person choosing a familiar item over a new one
Image Description: A person taking a placebo pill
Image Description: A person feeling better after taking a placebo
Image Description: A person agreeing to a small request
Image Description: A person agreeing to a larger request
Image Description: A person with conflicting thoughts
Image Description: A person adjusting their beliefs to match their actions'''


def script_processing(temp_script):
    processed_script = temp_script.split("\n")
    new_list = []
    script_desc = {}

    for i in processed_script:
        if i == " " or not i:
            continue
        new_list.append(i)
    # print(new_list)
    SCENE = "scene#{}"
    i = 0
    while i < len(new_list):
        ts = SCENE.format(i // 2)
        script_desc[ts] = [new_list[i][11:-1]]
        i += 1
        # script_desc[ts].append(new_list[i][20:-1])
        # i += 1
    return script_desc


script_desc = script_processing(temp_script)

# create a JSON file and write the script_desc to it
with open('script_desc.json', 'w') as f:
    json.dump(script_desc, f)

# create a JSON file and write the list to it
# with open('my_list.json', 'w') as f:
#     json.dump(script_processing(temp_script), f)
