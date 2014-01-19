import rg
import random

class Robot(object):

  NW = (7, 7)
  NE = (7, 11)
  SW = (11, 7)
  SE = (11, 11)
  DIRECTION = [NW, NE, SW, SE]

  def closest(self, positions, from_pos=None, dist_method=rg.dist):
    # return the closest position in the list compared to from_pos
    # usinog dist_metho
    from_pos = from_pos or self.location
    distances = map(lambda pos: dist_method(from_pos, pos), positions)
    closest = min((dist, index) for (index, dist) in enumerate(distances))
    return positions[closest[1]]

  def opponents_around(self, game):
    # return the opponents directly around the robot
    around = rg.locs_around(self.location, filter_out=("invalid"))
    robots_around = [game.robots[pos] for pos in around if pos in game.robots]
    return [robot for robot in robots_around if "robot_id" not in robot]

  def weakest_opponent(self, game):
    # return the weakest ennemy directly around or None if there is no
    # opponent around
    opponents = sorted(self.opponents_around(game), key=lambda x: x["hp"])
    return opponents[0] if opponents else None

  def is_surrounded(self, game):
    return len(self.opponents_around(game)) == 4

  def act(self, game):
    # We don't want to die during spawn turns so we move to an empty
    # non-spawn position
    if game.turn % rg.settings.spawn_every == 0 and "spawn" in rg.loc_types(self.location):
      empty_pos = rg.locs_around(self.location, filter_out=("invalid", "obstacle", "spawn"))
      if empty_pos:
        return ["move", empty_pos[0]]
      else:
        return ["suicide"]
    # Move to one of the "quarters"
    around = rg.locs_around(self.location, filter_out=("obstacle", "invalid"))
    position = rg.toward(self.location, random.choice(self.DIRECTION))
    position = self.closest(around, position)
    action = "move"
    if self.is_surrounded(game):
      return ["suicide"]
    # By the end we guard if we have low hp
    if 0 < self.hp < 15 and (rg.settings.max_turns - game.turn) < 5:
      return ["guard"]
    # Attack the weakest opponent around if any
    weakest = self.weakest_opponent(game)
    if weakest:
      # We go KABOOOOOM if we're low on hp!!
      if self.hp < 10:
        return ["suicide"]
      return ["attack", weakest.location]
    return [action, position]

