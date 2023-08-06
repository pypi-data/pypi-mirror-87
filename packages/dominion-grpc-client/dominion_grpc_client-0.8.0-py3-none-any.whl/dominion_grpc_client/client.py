import json
from threading import Thread

import grpc

from dominion_object_model import object_model
from dominion_grpc_proto import dominion_pb2_grpc
from dominion_grpc_proto.dominion_pb2 import PlayerInfo, Card, ActionResponse


class Client(object_model.GameClient, object_model.Player):
    def __init__(self, name, player_factory):
        self.name = name
        self._player = player_factory(self)
        self._state = None
        self._server = None

    def run(self, host='localhost', port=50051):
        try:
            with grpc.insecure_channel(f'{host}:{port}') as channel:
                self._server = dominion_pb2_grpc.DominionServerStub(channel)
                messages = self._server.Join(PlayerInfo(name=self.name))
                for message in messages:
                    self._handle_message(message)
        except Exception as e:
            self.on_game_event(dict(event='server error', exception=e))

    def _handle_message(self, message):
        if message.type == 'play':
            self.play()
        elif message.type == 'respond':
            data = json.loads(message.data)
            self.respond(data['action'], *data['args'])
        elif message.type == 'on_game_event':
            event = json.loads(message.data)
            self.on_game_event(event)
        elif message.type == 'on_state_change':
            state = json.loads(message.data)
            self.on_state_change(state)
        elif message.type == 'ack':
            data = json.loads(message.data)
            self.name = data['name']
        else:
            print('Unknown message type:', message.type)

    def start_game(self):
        pi = PlayerInfo(name=self.name)
        self._server.Start(pi)

    # Player interface
    def play(self):
        Thread.start(target=lambda: self._player.play())

    def respond(self, action, *args):
        response = self._player.respond(action, *args)
        card = Card(name=action)
        payload = json.dumps(response)
        response = ActionResponse(card=card, payload=payload)
        self._server.Respond(response)

    def on_game_event(self, event):
        self._player.on_game_event(event)

    def on_state_change(self, state):
        self._player.on_state_change(state)

    # GameClient interface
    def play_action_card(self, card_type):
        self._server.PlayCard(Card(name=card_type))

    def buy(self, card_type):
        self._server.Buy(Card(name=card_type))

    def done(self):
        self._server.Done(PlayerInfo(name=self.name))
