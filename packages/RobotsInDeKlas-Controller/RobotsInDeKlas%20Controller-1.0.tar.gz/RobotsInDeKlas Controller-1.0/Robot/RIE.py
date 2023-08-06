class Config:
    path = "rie.dialogue.config."
    nativeVoice = path + "native_voice"
    language = path + "language"
    profanity = path + "profanity"


class KeyWord:
    path = "rie.dialogue.keyword."
    add = path + "add"
    remove = path + "remove"
    clear = path + "clear"
    stream = path + "stream"
    close = path + "close"
    read = path + "read"


class Dialogue:
    path = "rie.dialogue."
    say = path + "say"
    sayAnimated = path + "say_animated"
    ask = path + "ask"
    stop = path + "stop"
    config = Config()
    keyWord = KeyWord()


class Vision:
    pathCard = "rie.vision.card."
    pathFace = "rie.vision.face."
    info = pathCard + "info"
    stream = pathCard + "stream"
    read = pathCard + "read"
    close = pathCard + "close"
    infoFace = pathFace + "info"
    streamFace = pathFace + "stream"
    readFace = pathFace + "read"
    closeFace = pathFace + "close"
    find = pathFace + "find"
    track = pathFace + "track"
    stop = pathFace + "stop"

class RIE:
    cloudModules = "rie.cloud_modules.ready"
    dialogue = Dialogue()
    vision = Vision()