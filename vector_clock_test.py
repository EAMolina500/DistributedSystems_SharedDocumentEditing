import unittest
import vector_clock as vc

class VectorClockTest(unittest.TestCase):
    def test_init_default(self):
        """Tests initialization with default values."""
        clock = vc.VectorClock()
        self.assertEqual(clock._clock, [0, 0, 0])

    def test_init_custom(self):
        """Tests initialization with custom values."""
        clock = vc.VectorClock([1, 2, 3])
        self.assertEqual(clock._clock, [1, 2, 3])

    def test_increment(self):
        """Tests incrementing a specific server's timestamp."""
        clock = vc.VectorClock()
        clock.increment(2)  # Increment server 2
        self.assertEqual(clock._clock, [0, 1, 0])

    def test_compare_equal(self):
        """Tests comparing two equal clocks."""
        clock1 = vc.VectorClock([1, 1, 1])
        clock2 = vc.VectorClock([1, 1, 1])
        self.assertEqual(clock1.compare(clock2), "equal")

    def test_compare_larger(self):
        """Tests comparing a larger clock."""
        clock1 = vc.VectorClock([2, 1, 1])
        clock2 = vc.VectorClock([1, 1, 1])
        self.assertEqual(clock1.compare(clock2), "larger")

    def test_compare_smaller(self):
        """Tests comparing a smaller clock."""
        clock1 = vc.VectorClock([0, 1, 1])
        clock2 = vc.VectorClock([1, 1, 1])
        self.assertEqual(clock1.compare(clock2), "smaller")

    def test_compare_conflict(self):
        """Tests comparing clocks with a conflict."""
        clock1 = vc.VectorClock([1, 2, 0])
        clock2 = vc.VectorClock([1, 1, 2])
        self.assertEqual(clock1.compare(clock2), "conflict")

if __name__ == "__main__":
    unittest.main()
