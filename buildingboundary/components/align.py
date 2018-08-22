# -*- coding: utf-8 -*-
"""

@author: Chris Lucas
"""

import numpy as np


def align_by_intercept(segments, max_diff):
    d = {}
    for s in segments:
        if round(s.slope, 4) in d:
            d[round(s.slope, 4)].append(s)
        else:
            d[round(s.slope, 4)] = [s]

    for v in d.values():
        intercepts = np.array([x.intercept for x in v])
        order = np.argsort(intercepts)
        intercepts_sorted = intercepts[order]
        diff_idx = [0]+list(np.where(np.diff(intercepts_sorted) >
                                     max_diff)[0] + 1)+[len(v)]

        clusters = [order[x:y] for x, y in
                    zip(diff_idx[:-1], np.roll(diff_idx, -1)[:-1])]

        for c in clusters:
            if len(c) > 1:
                new_intercept = np.mean(intercepts[c])
                for i in c:
                    v[i].change_intercept(new_intercept)
