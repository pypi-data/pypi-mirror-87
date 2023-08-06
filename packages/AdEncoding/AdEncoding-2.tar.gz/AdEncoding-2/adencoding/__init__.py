def encode(string,level):
    import base64

    message = string
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    if level == 1 or 0:
        return(base64_message)
    else:
        for i in range(level - 1):
            message_bytes = base64_message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
        return(base64_message)

def decode(string,level):
    import base64

    message = string
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64decode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    if level == 1 or 0:
        return(base64_message)
    else:
        for i in range(level - 1):
            message_bytes = base64_message.encode('ascii')
            base64_bytes = base64.b64decode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
        return(base64_message)