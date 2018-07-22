from log_list import LogListener
import events as events
from entities import Match
import commands


def connect(match):
    engine = Engine()
    engine.connect('log', match)


class Engine(LogListener):

    def on_player_join(self, player_id):
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
            commands.draw(self.context, player._id, Match.INITIAL_HAND_SIZE)

    def on_refresh(self):
        player = self.context.current_player()
        for card in player.board:
            card.activated = False
        self.publish(events.Draw, player._id)
        self.publish(events.Prompt, player._id)

    def on_draw(self, player_id):
        commands.draw(self.context, player_id, 1)


