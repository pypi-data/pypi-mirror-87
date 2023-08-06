from .RIE import RIE
from .ROM import Rom
from .UBI import Body

from twisted.internet.defer import inlineCallbacks


class Robot:
    body = Body()
    rom = Rom()
    rie = RIE()

    def __init__(self, session):
        self.session = session

    @inlineCallbacks
    def say(self, text):
        yield self.session.call(self.rie.dialogue.say, text=text, lang='en')

    # NOTE: streamAudio werkt niet met youtube urls, directe url nodig.
    @inlineCallbacks
    def streamAudio(self, url):
        yield self.session.call(self.rom.actuator.audio.stream, url=url, sync=True)
        input()
        self.stopAudio()

    @inlineCallbacks
    def stopAudio(self):
        yield self.session.call(self.rom.actuator.audio.stop)
