"""Exact solver for the route selection of Equation (9).

Given a launch point, a set of candidate points with weights, and a distance budget,
find the route that collects the greatest total weight and returns to the launch
point without exceeding the budget. Ties on weight are broken by the shorter route.

The obvious way to solve this is to enumerate every ordering of every subset, which
is what both planning scripts originally did. That costs sum_r P(n, r) routes: about
2,000 for six candidate points, but 1.2e11 for fourteen, so it stops being usable
exactly when the planning problem starts being interesting.

The visiting order only ever matters through the distance it produces, so the subsets
can be kept and each one's shortest route found by dynamic programming over
(visited set, last point) -- the Held-Karp recursion. States whose distance already
exceeds the budget are dropped, since extending a route never shortens it. The result
is identical to the enumeration; only the cost of obtaining it changes.
"""

from __future__ import annotations

import numpy as np

# The mission's distance budget, in metres, shared by the planner and the stability
# analysis so the two cannot drift apart. It is a limit on mission duration rather than
# on endurance: the vessel's battery allows far longer transits than a supervised
# survey of this kind occupies.
MAX_PATH_LENGTH_M = 7_000.0

# The clustering neighbourhood, in metres, shared for the same reason. With a minimum
# of one cell per cluster the grouping is single-linkage at this radius, so it is the
# separation two groups must have, not the width a group may reach. Its value is taken
# from the score field: at this separation the field's semivariance is about a fifth of
# its sill, so two cells this close carry nearly the same score and one profile stands
# for both. src/PathPlanning/ClusterRadius.py reports the sweep behind that choice.
CLUSTER_EPS_M = 100.0

# Mean earth radius, for converting a neighbourhood in metres to the radians the
# haversine metric expects.
EARTH_RADIUS_M = 6_371_000.0

# Where the vessel is launched and recovered, as (latitude, longitude): the slipway at
# Vasstrandlia. Every route starts and ends here, so the radius sweep and the reported
# plan measure their distances from the same place.
LAUNCH_POINT = (62.465779, 6.401947)

# Distances are compared at millimetre precision when breaking ties on equal weight,
# so that two routes differing only by floating-point noise resolve deterministically.
_TIE_PLACES = 3


def solve(distance_matrix, weights, max_distance):
    """Return (order, score, length) for the best route within the budget.

    distance_matrix : (n+2, n+2) distances; index 0 is the start, index n+1 the end
    weights         : (n,) weight collected at each candidate point
    max_distance    : budget, in the units of distance_matrix

    order is the list of visited points as indices into distance_matrix, so the full
    route is [0] + order + [n+1]. Returns ([], -inf, inf) when the budget admits no
    route that visits at least one point.
    """
    distance_matrix = np.asarray(distance_matrix, dtype=float)
    weights = np.asarray(weights, dtype=float)
    n = len(weights)
    if n == 0:
        return [], -np.inf, np.inf
    end = n + 1

    # reachable[mask][last] -> shortest distance from the start through mask,
    # finishing at last. Only states within the budget are carried forward.
    reachable: dict[int, dict[int, float]] = {}
    for j in range(1, n + 1):
        d = distance_matrix[0, j]
        if d <= max_distance:
            reachable.setdefault(1 << (j - 1), {})[j] = d

    prev: dict[tuple[int, int], int] = {}
    frontier = dict(reachable)
    while frontier:
        nxt_frontier: dict[int, dict[int, float]] = {}
        for mask, ends in frontier.items():
            for last, here in ends.items():
                for nxt in range(1, n + 1):
                    bit = 1 << (nxt - 1)
                    if mask & bit:
                        continue
                    cand = here + distance_matrix[last, nxt]
                    if cand > max_distance:
                        continue
                    new_mask = mask | bit
                    slot = reachable.setdefault(new_mask, {})
                    if cand < slot.get(nxt, np.inf):
                        slot[nxt] = cand
                        prev[(new_mask, nxt)] = last
                        nxt_frontier.setdefault(new_mask, {})[nxt] = cand
        frontier = nxt_frontier

    best_score, best_len, best_order = -np.inf, np.inf, []
    for mask, ends in reachable.items():
        closing, tail = np.inf, -1
        for last, here in ends.items():
            total = here + distance_matrix[last, end]
            if total < closing:
                closing, tail = total, last
        if closing > max_distance:
            continue
        score = float(weights[[j for j in range(n) if (mask >> j) & 1]].sum())

        better = score > best_score
        if not better and score == best_score:
            better = round(closing, _TIE_PLACES) < round(best_len, _TIE_PLACES)
        if not better:
            continue

        seq, cur, cur_mask = [], tail, mask
        while cur != -1:
            seq.append(cur)
            cur, cur_mask = prev.get((cur_mask, cur), -1), cur_mask & ~(1 << (cur - 1))
        seq.reverse()

        best_score, best_len, best_order = score, closing, seq

    return best_order, best_score, best_len
