import rg

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

  def weakest(self, game):
    # return the weakest ennemy directly around
    around = rg.locs_around(self.location, filter_out=("invalid"))
    opponents = [game.robots[pos] for pos in around if pos in game.robots and game.robots[pos].robot_id != self.player_id]
    if opponents:
      weakest = sorted(opponents, key=lambda x: x.hp)[0]
      return weakest.location
    return None

  def act(self, game):
    # We don't want to die during spawn turns so we move to an empty
    # non-spawn position
    if game.turn % rg.settings.spawn_every == 0 and "spawn" in rg.loc_types(self.location):
      empty_pos = rg.locs_around(self.location, filter_out=("invalid", "obstacle", "spawn"))
      if empty_pos:
        return ["move", empty_pos[0]]
      else:
        return ["suicide"]
    # Move to the closest "quarter"
    around = rg.locs_around(self.location, filter_out=("obstacle", "invalid"))
    position = rg.toward(self.location, self.closest(self.DIRECTION))
    position = self.closest(around, position)
    action = "move"
    weakest = self.weakest(game)
    if weakest:
      return ["attack", weakest]
    return [action, position]

