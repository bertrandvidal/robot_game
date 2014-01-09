import rg
import random

class Robot(object):

  def act(self, game):
    target = random.choice(rg.locs_around(self.location, filter_out=("invalid")))
    if target in game.robots and "robot_id" not in game.robots[target]:
      return ["attack", target]
    else:
      return ["move", target]
