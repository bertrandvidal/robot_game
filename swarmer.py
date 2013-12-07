import rg

class Robot(object):

  def act(self, game):
    if game.turn % 10 == 0 and "spawn" in rg.loc_types(self.location):
      return ["move", rg.toward(self.location, rg.CENTER_POINT)]
    return ["guard"]
