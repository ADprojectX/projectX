def convert_to_image(sender, receiver, prompt):
    r = sender.send(prompt)
    print(type(r),r)
    message_id = r.json()['id']
    print(message_id)
    pass