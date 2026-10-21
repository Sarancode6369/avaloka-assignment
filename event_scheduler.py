"""Event scheduler: overlap check, minimum rooms, and room assignment."""
import heapq
from typing import Dict, List, Tuple

Event = Tuple[int, int]


def can_attend_all(events: List[Event]) -> bool:
    ordered = sorted(events)                       
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:      
            return False
    return True


def min_rooms_required(events: List[Event]) -> int:
    if not events:
        return 0
    starts = sorted(s for s, _ in events)
    ends = sorted(e for _, e in events)

    rooms = 0
    j = 0                                         
    for s in starts:
        if s < ends[j]:
            rooms += 1                            
        else:
            j += 1                                
    return rooms


def _room_name(n: int) -> str:                     
    s, n = "", n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return f"Room {s}"


def assign_rooms(events: List[Event]) -> Dict[int, str]:
    """Returns {event_index: 'Room A', ...}"""
    order = sorted(range(len(events)), key=lambda i: events[i])
    busy, free, next_id, result = [], [], 0, {}

    for i in order:
        start, end = events[i]
        while busy and busy[0][0] <= start:        
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room, next_id = next_id, next_id + 1
        result[i] = _room_name(room)
        heapq.heappush(busy, (end, room))
    return result
