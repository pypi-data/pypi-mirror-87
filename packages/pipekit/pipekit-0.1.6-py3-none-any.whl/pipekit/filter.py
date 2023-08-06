#!/usr/bin/env python3

from pprint import pprint  # noqa: W0611 F401

from .component import Component
from .message import Message


class Filter(Component):

    def __call__(self, messages):
        return self.filter(messages)

    async def filter(self, messages):
        async for channel, message in messages:
            channel, message = await self.process(channel, message)
            yield (channel, message)

    async def process(self, channel, message):
        raise NotImplementedError(f'process() out {self}')


class ChannelChain(Filter):

    TESTS = dict(directory=lambda m: m.path.id_dir(),
                 file=lambda m: m.path.id_file())

    async def process(self, channel, message):
        for test_name, test_fn in self.TESTS.items():
            if test_fn(message):
                return test_name, message


class LifeCycleSignal(Filter):

    async def filter(self, messages):
        # import pudb; pudb.set_trace()
        # self.debug('*** starting')
        async for channel, message in messages:
            yield (channel, message)

            if not self.running:
                break

        settings = self.settings()
        if settings.event == 'finished':
            # self.debug(f'*** finishing (outbox.{settings.get("channel", "finished")})')
            # message = LifeCycleMessage('finished')
            # message.checkin(self)
            # yield (settings.get('channel', 'finished'), message)
            yield (settings.get('channel', 'finished'), LifeCycleMessage('finished'))
            # yield ('default', message)
            # self.debug(f'*** finished (outbox.{settings.get("channel", "finished")})')


class LifeCycleMessage(Message):
    def __init__(self, event, **kwargs):
        super().__init__(event=event, **kwargs)


# ofilters:
#     rehydrated-filetree-stream:
#         component: pipekit.filter:MessageStreamFilter
#         settings:
#             add: local-fs-object

# ofilters:
#     rehydrated-filetree-stream:
#         component: pipekit.filter:MessageStreamFilter
#         settings:
#             wait:
#                 action: message
#                 channel: finished

class MessageStreamFilter(Filter):

    def configure(self, **settings):
        # import pudb
        # pudb.set_trace()
        settings.setdefault('name', self.id.split('.')[-1])
        for prop in ['add', 'wait']:
            if prop in settings:
                value = settings[prop]
                if isinstance(value, str):
                    value = [value]
                settings[prop] = set(value)
                break

        self.settings = settings
        self.stream = MessageStream(self.name)
        self.seen = set()
        return settings

    async def process(self, channel, message):
        settings = self.settings()
        if message.meta.type in settings.get('add', []):
            self.stream.add(message)
        elif settings.wait:
            if isinstance(message.meta.get('stream'), MessageStream) \
                    and message.meta.stream.name == self.name:
                self.seen.add(message)  # TODO: duplicate detection ?

        return channel, message

    def finalize(self):
        settings = self.settings()
        if settings.add:
            self.stream.complete = True
        elif settings.wait:
            if self.stream.complete and len(self.seen) == len(self.stream):
                if settings.action == 'message':
                    return settings.channel, Message()


class MessageStream:
    def __init__(self, name):
        self.name = name
        self.messages = dict()
        self.complete = False

    def add(self, message):
        message.meta.setdefault('streams', dict())
        message.meta['streams'][self.name] = self
        self.messages[message.meta.id] = message

    def remove(self, message):
        del message.meta['streams'][self.name]
        del self.messages[message.meta.id]


class MessageMangleFilter(Filter):

    def deepget(self, mapping, key):
        if '.' not in key:
            return mapping[key]

        else:
            current, remainder = key.split('.', 1)
            return self.deepget(mapping[current], remainder)

    def deepset(self, mapping, key, value):
        if '.' not in key:
            mapping[key] = value

        else:
            current, remainder = key.split('.', 1)
            self.deepset(mapping[current], remainder, value)

    async def process(self, channel, message):
        for spec in self.settings.attributes:
            if len(spec) != 1:
                raise ValueError(f'Bad configuration: {self.settings}')

            key = list(spec.keys())[0]
            self.deepset(message, key, spec[key].format(**message))
        return channel, message
