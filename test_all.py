import threading
import unittest

from lru_cache import LRUCache, ThreadSafeLRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms


class TestLRU(unittest.TestCase):
    def test_eviction_order(self):
        c = LRUCache(2)
        c.put(1, 1); c.put(2, 2)
        self.assertEqual(c.get(1), 1)
        c.put(3, 3)                               
        self.assertEqual(c.get(2), -1)
        c.put(4, 4)                                
        self.assertEqual((c.get(1), c.get(3), c.get(4)), (-1, 3, 4))

    def test_update_existing(self):
        c = LRUCache(2)
        c.put(1, 1); c.put(1, 10)
        self.assertEqual(c.get(1), 10)

    def test_capacity_one(self):
        c = LRUCache(1)
        c.put(1, 1); c.put(2, 2)
        self.assertEqual((c.get(1), c.get(2)), (-1, 2))

    def test_thread_safe(self):
        c = ThreadSafeLRUCache(50)
        def work(base):
            for i in range(1000):
                c.put(base + i % 100, i); c.get(base + i % 100)
        ts = [threading.Thread(target=work, args=(k * 100,)) for k in range(8)]
        [t.start() for t in ts]; [t.join() for t in ts]
        self.assertLessEqual(len(c.map), 50)


class TestScheduler(unittest.TestCase):
    def test_can_attend(self):
        self.assertTrue(can_attend_all([(9, 10), (10, 11), (11, 12)]))
        self.assertFalse(can_attend_all([(9, 11), (10, 12)]))
        self.assertTrue(can_attend_all([]))

    def test_min_rooms(self):
        self.assertEqual(min_rooms_required([]), 0)
        self.assertEqual(min_rooms_required([(9, 10), (10, 11), (11, 12)]), 1)
        self.assertEqual(min_rooms_required([(9, 11), (10, 12), (10, 13)]), 3)

    def test_assign_rooms(self):
        ev = [(9, 11), (10, 12), (11, 13)]
        r = assign_rooms(ev)
        self.assertEqual(len(set(r.values())), min_rooms_required(ev))
        self.assertEqual(r[0], r[2])               


if __name__ == "__main__":
    unittest.main()
