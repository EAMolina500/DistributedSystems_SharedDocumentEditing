class VectorClock:
  def __init__(self, initial_value=None):
    if initial_value is None:
      self._clock = [0,0,0]
    else:
      self._clock = initial_value

  def increment(self, server_id):
    self._clock[server_id-1] += 1

  def get_value(self):
    return self._clock

  def compare(self, other_clock):
    differences = [a - b for a, b in zip(self._clock, other_clock._clock)]

    if all(diff == 0 for diff in differences):
        return 'equal'
    elif all(diff >= 0 for diff in differences):
        return 'larger'
    elif all(diff <= 0 for diff in differences):
        return 'smaller'
    else:
        return 'conflict'

  def get_smaller(self, clock, other_clock):
    if (self.compare(clock, other_clock) == 'smaller'):
      return clock
    elif (self.compare(other_clock, clock) == 'smaller'):
      return other_clock
    else:
      return None

  def compute_new(self, other_clock):
    new_clock = VectorClock([max(a, b) for a, b in zip(self._clock, other_clock._clock)])
    return new_clock

if __name__ == "__main__":
  vc = VectorClock() # [0,0,0]

  vc.increment(1)
  print(vc.get_value())
  vc.increment(2)
  print(vc.get_value())
  vc.increment(3)
  print(vc.get_value())

  vc1 = VectorClock([1,-1,3])
  vc2 = VectorClock([0,0,1])
  #print(vc1.compare(vc2))

  print('new clock')
  print(vc1.compute_new(vc2).get_value())
