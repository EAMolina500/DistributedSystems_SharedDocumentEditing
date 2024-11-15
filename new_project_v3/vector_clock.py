#import pdb

class VectorClock:
  def __init__(self, server_id, clock=[0,0,0]):
    self._server_id = server_id
    self._clock = clock

  def __repr__(self):
    return f"{self._clock}"

  def get_clock(self):
    return self._clock

  def set_clock(self, clock):
    self._clock = clock

  def increment(self):
    index = self._server_id - 1
    self._clock[index] += 1

  def compute_new(self, other_clock):
    #pdb.set_trace()
    new_clock = [max(a, b) for a, b in zip(self._clock, other_clock.get_clock())]
    self._clock = new_clock

  def compare(self, other_clock):
    differences = [a - b for a, b in zip(self._clock, other_clock.get_clock())]

    if all(diff == 0 for diff in differences):
      return 'equal'
    elif all(diff >= 0 for diff in differences):
      return 'larger'
    elif all(diff <= 0 for diff in differences):
      return 'smaller'
    else:
      return 'conflict'
