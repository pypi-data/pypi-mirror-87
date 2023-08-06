def interceptor(text):
    if text["success"]:
        pass
    else:
        raise Exception(text["msg"])

def exist(text):
    if text["success"]:
        return True
    else:
        return False