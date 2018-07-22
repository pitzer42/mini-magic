from log_list import LogListener
import models2.events as events
from models2.entities import Match


def connect(match):
    engine = Engine()
    engine.connect('log', match)

class Engine(LogListener):

    def on_player_join(self):
        if self.context.has_enough_players():
            self.publish(events.Ready)
        else:
            self.publish(events.Setup)

    def on_ready(self):
        self.publish(events.InitialDraw)
        self.publish(events.TurnBegin, self.context.current_player()._id)
        self.publish(events.Refresh)

    def on_initial_draw(self):
        for player in self.context.players:
            player.draw(Match.INITIAL_HAND_SIZE)

    def on_refresh(self):
        player = self.context.current_player()
        for card in player.board:
            card.activated = False
        self.publish(events.Draw, player._id)

    def on_draw(self, player_id):
        player = self.context.get_player_by_id(player_id)
        player.draw(1)
        self.publish(events.Prompt, player_id)


