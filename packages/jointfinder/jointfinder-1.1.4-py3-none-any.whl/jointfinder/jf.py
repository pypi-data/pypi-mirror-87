import concurrent.futures
import multiprocessing
import pandas as pd
import numpy as np
# import swifter
import numbers
import pickle
import sys
from itertools import chain, product
from functools import reduce
from copy import deepcopy
from math import ceil
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")

is_import = True


class JointFinder:
    def __init__(self, data, tolerance=0.001, angular_tolerance=0.001, select_only=None, engine=0):
        '''
        Arg input (data) is pandas dataframe (df) or list of dictionary(ies). 
        Pandas columns: name, x0, y0, z0, x1, y1, z1, nx, ny, nz, thickness (all float/int)
        Line is [x0, y0, z0] to [x1, y1, z1], must be on a plane
        Depth vector is [nx, ny, nz], always perpendicular to plane
        Dictionary elements: name, points, [depth (unit vector), thickness] - optional
        Points/lines must be sequential, right turn (with depth vector upright to plane)
        Method find_joint() returns processed dataframe
        Property df returns original input dataframe
        '''
        self._t = float(tolerance)
        self._at = float(angular_tolerance)
        if type(data) == list:
            data = self._to_dataframe(data)
        # elif type(data) == dict:
        #     pass
        self._df = data.astype(float).reset_index(drop=True)
        self._these_only = select_only if select_only is not None else None
        self._engine = engine
        if engine == 2:
            from . import worker_cuda
            self._vfunc = worker_cuda.vfunc
        elif engine == 1:
            from . import worker_numba
            self._vfunc = worker_numba.vfunc
            # import worker_numba_loop
            # self._vfunc = worker_numba_loop.vfunc
        else:
            from . import worker
            self._vfunc = worker.vfunc

    @property
    def df(self):
        return self._df

    def _find_ab_vector(self, coords):
        coords = np.array(coords)
        coords = np.append(coords, coords[:1], axis=0)
        ab = np.array(list(map(lambda z: z[1] - z[0], zip(coords[:-1], coords[1:]))))
        ab = np.append(ab, ab[:1], axis=0)
        return ab

    def _find_depth_vector(self, ab):
        crosses = np.cross(ab[:-1], ab[1:], axis=1)
        cross_mags = np.array(list(map(np.linalg.norm, crosses)))
        u_cross = np.array(list(map(lambda z: z[0] / z[1], zip(crosses, cross_mags))))
        depth_vector = np.copysign(np.abs(u_cross[0]), np.sum(crosses, axis=0)) * -1
        return depth_vector

    def _one_part(self, part_dict):
        # name
        try:
            name = float(part_dict['name'])
        except (KeyError, ValueError):
            print(f"No name or incorrect name (integer/floating number only): {part_dict}")
            return pd.DataFrame()
        is_numeric = lambda ax: isinstance(ax, numbers.Number)
        # coordinates
        try:
            coords = list(part_dict['points'])
            n_unique_member = len({tuple(coord) for coord in coords})
            if n_unique_member < 3 and n_unique_member != len(coords):
                # minimum three and unique points
                raise ValueError
            if True in [len(coord) != 3 for coord in coords]:
                # all must have three axes
                raise ValueError
            if False in [is_numeric(ax) for coord in coords for ax in coord]:
                # must be either integer or float
                raise ValueError
        except (KeyError, ValueError, TypeError):
            print(f"No coordinates or incorrect points for {name}")
            return pd.DataFrame()
        # depth vector
        ab = self._find_ab_vector(coords)
        try:
            depth = part_dict['depth']
        except KeyError:
            # discover depth vector
            depth = self._find_depth_vector(ab)
        try:
            if len(depth) != 3:
                # must have three elements
                raise ValueError
            if False in [is_numeric(ax) for ax in depth]:
                # must be either integer or float
                raise ValueError
            depth = np.array(depth)
            if np.any((depth < -1) | (depth > 1)) or not 0.999 <= np.linalg.norm(depth) <= 1:
                # any is smaller than 0 or larger than 1 or sum is not 1
                raise ValueError
            # sorted unique levels
            levels = sorted(list({np.dot(depth, coord) for coord in coords}))
            # sum of sorted difference
            if sum(np.diff(levels)) > self._t:
                raise ValueError
            # TODO: must right turn
            zipped = zip(np.cross(ab[:-1], depth * -1), np.linalg.norm(ab[:-1], axis=1))
            turn = np.array(list(map(lambda z: z[0] / z[1], zipped)))
            next = list(coords[2:]) + list(coords[:2])
            is_right_turn = np.sum(np.sum(turn * next, axis=1) - np.sum(turn * coords, axis=1)) < 0
            if not is_right_turn:
                raise ValueError
        except ValueError:
            print(f"No depth vector specified or incorrect depth vector or coordinates for {name}")
            return pd.DataFrame()
        # depth/thickness
        try:
            thickness = part_dict['thickness']
            if not is_numeric(thickness):
                raise KeyError
        except KeyError:
            print(f"No or incorrect thickness specified for {name}, setting 0 as default")
            thickness = 0
        lines = coords + coords[:1]
        lines = zip(lines[:-1], lines[1:])
        lines = list(map(lambda line: [name, *line[0], *line[1], *depth, thickness], lines))
        columns = 'name', 'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 'nx', 'ny', 'nz', 'depth'
        return pd.DataFrame(lines, columns=columns)

    def _to_dataframe(self, data):
        if False in [type(datum) == dict for datum in data]:
            # non-dictionary member exists
            pass
        df = pd.concat([self._one_part(part_dict) for part_dict in data], 
                       sort=False, ignore_index=True)
        return df

    def _line_iterator(self, row, masks):
        _, args = row
        name, x0, y0, z0, x1, y1, z1, nx, ny, nz, qdepth, Xx, Xy, Xz, abx, aby, abz, a_offset, b_offset = args.to_numpy()
        length = np.linalg.norm([x1 - x0, y1 - y0, z1 - z0])
        tol = qdepth + self._pdepth + self._t
        # crossing or near ab line
        cross = np.array([Xx, Xy, Xz])
        # cross (thumb) is cross product of plane vector (index) and line vector (middle)
        offset = np.dot(cross, [x0, y0, z0])
        # negative is "right" side, positive is "left" side
        c_from_ab, d_from_ab = np.sum(cross * self._c, axis=1) - offset, np.sum(cross * self._d, axis=1) - offset
        # crossing if sign is different
        part_mask_1 = np.copysign(1, c_from_ab) * np.copysign(1, d_from_ab) <= 0
        # near if under tolerance
        part_mask_1 |= (np.abs(c_from_ab) <= tol) | (np.abs(d_from_ab) <= tol)
        # either is acceptable
        part_mask_1 = np.isin(self._names_flat, np.unique(self._names_flat[part_mask_1]))
        # overlapping or near ab ends
        ab = np.array([abx, aby, abz])
        # ab is unit vector, find offsets along ab vector
        c_from_a, c_from_b = np.sum(ab * self._c, axis=1) - a_offset, np.sum(ab * self._c, axis=1) - b_offset
        d_from_a, d_from_b = np.sum(ab * self._d, axis=1) - a_offset, np.sum(ab * self._d, axis=1) - b_offset
        # see if c and d on different "sides" of a, or b (overlapping)
        part_mask_2 = ((np.copysign(1, c_from_a) * np.copysign(1, d_from_a)) <= 0) | ((np.copysign(1, c_from_b) * np.copysign(1, d_from_b)) <= 0)
        # or c/d near a/b
        part_mask_2 |= (np.abs(c_from_a) <= tol) | (np.abs(c_from_b) <= tol) | (np.abs(d_from_a) <= tol) | (np.abs(d_from_b) <= tol)
        part_mask_2 = np.isin(self._names_flat, np.unique(self._names_flat[part_mask_2]))
        # near cd plane mask, near or crossing ab mask, near or overlapping ab ends mask
        masks &= part_mask_1 & part_mask_2
        # masks must contain True
        if not np.any(masks):
            return []
        # guvfunc
        if self._engine == 2:
            # res = self._vfunc(x0, y0, z0, x1, y1, z1, nx, ny, nz, qdepth, 
            #                   self._cx[masks], self._cy[masks], self._cz[masks], self._dx[masks], self._dy[masks], self._dz[masks], 
            #                   self._px[masks], self._py[masks], self._pz[masks], self._pdepth[masks],
            #                   self._t, self._at, self._ph[masks])

            res = self._vfunc(x0, y0, z0, x1, y1, z1, nx, ny, nz, qdepth, 
                              np.ascontiguousarray(self._cx[masks]), 
                              np.ascontiguousarray(self._cy[masks]), 
                              np.ascontiguousarray(self._cz[masks]), 
                              np.ascontiguousarray(self._dx[masks]), 
                              np.ascontiguousarray(self._dy[masks]), 
                              np.ascontiguousarray(self._dz[masks]), 
                              np.ascontiguousarray(self._px[masks]), 
                              np.ascontiguousarray(self._py[masks]), 
                              np.ascontiguousarray(self._pz[masks]), 
                              np.ascontiguousarray(self._pdepth[masks]),
                              self._t, self._at, 
                              np.ascontiguousarray(self._ph[masks]))

        elif self._engine == 1:
            ph = deepcopy(self._ph)[masks]
            
            # res = self._vfunc(x0, y0, z0, x1, y1, z1, nx, ny, nz, qdepth, 
            #                   self._c[masks], self._d[masks], self._p[masks], self._pdepth[masks], 
            #                   self._t, self._at, ph)
            
            # numba map line
            res = list(map(lambda z: self._vfunc(np.ascontiguousarray([x0, y0, z0]), 
                                                 np.ascontiguousarray([x1, y1, z1]), 
                                                 np.ascontiguousarray([nx, ny, nz]), 
                                                 qdepth, 
                                                 np.ascontiguousarray(z[0]), 
                                                 np.ascontiguousarray(z[1]), 
                                                 np.ascontiguousarray(z[2]), 
                                                 z[3], 
                                                 self._t, self._at, 
                                                 np.ascontiguousarray([-1] * 5)), 
                           zip(self._c[masks], self._d[masks], self._p[masks], self._pdepth[masks])))

            # numba for loop
            # res = self._vfunc(x0, y0, z0, x1, y1, z1, nx, ny, nz, qdepth, 
            #                   np.ascontiguousarray(self._c[masks]), 
            #                   np.ascontiguousarray(self._d[masks]), 
            #                   np.ascontiguousarray(self._p[masks]), 
            #                   np.ascontiguousarray(self._pdepth[masks]), 
            #                   self._t, self._at, 
            #                   np.ascontiguousarray(ph))
        else:
            res = list(map(lambda z: self._vfunc(np.ascontiguousarray([x0, y0, z0]), 
                                        np.ascontiguousarray([x1, y1, z1]), 
                                        np.ascontiguousarray([nx, ny, nz]), 
                                        qdepth, 
                                        np.ascontiguousarray(z[0]), 
                                        np.ascontiguousarray(z[1]), 
                                        np.ascontiguousarray(z[2]), 
                                        z[3], 
                                        self._t, self._at), 
                           zip(self._c[masks], self._d[masks], self._p[masks], self._pdepth[masks])))
            res = np.array(res)

        # give name, give index here later if important
        res = np.append(res, self._names[masks], axis=1)
        # remove those will all 5 elements == -1
        resf = res[res[:, 5] != name]
        resf = resf[~reduce(lambda a, b: a & b, [resf[:, i] == -1 for i in range(5)])]
        resf = resf[~reduce(lambda a, b: a | b, [np.isnan(resf[:, i]) for i in range(5)])]
        # values
        tab, _l0, _l1, _r0, _r1, mate = [resf[:, i:i+1] for i in range(6)]
        # left and right
        left, right = np.append(_l0, _l1, axis=1), np.append(_r0, _r1, axis=1)
        left, right = np.append(left, tab, axis=1), np.append(right, tab, axis=1)
        left, right = np.append(left, mate, axis=1), np.append(right, mate, axis=1)
        # remove if both l0/r0 and l1/r1 are -1
        left = left[(tab[:, 0] != -1) & (left[:, 0] != -1) & (left[:, 1] != -1)]
        right = right[(tab[:, 0] != -1) & (right[:, 0] != -1) & (right[:, 1] != -1)]

        # find same mates for left and right
        def _mate_iterator(m):
            # for every mate, extract side bound pairs for left and right
            lm, rm = left[left[:, 3] == m, :2], right[right[:, 3] == m, :2]
            # for each left and right, flatten then sort as ticks
            lticks, rticks = sorted(list(set(lm.flatten()))), sorted(list(set(rm.flatten())))
            # create slots/segments in between ticks, fill with default False
            lflippers, rflippers = [False] * (len(lticks) - 1), [False] * (len(rticks) - 1)
            # sort bound pair, then toggle the segment
            for elm in lm:
                elm0, elm1 = sorted(elm)
                for i in range(lticks.index(elm0), lticks.index(elm1)):
                    lflippers[i] = not lflippers[i]
            for erm in rm:
                erm0, erm1 = sorted(erm)
                for i in range(rticks.index(erm0), rticks.index(erm1)):
                    rflippers[i] = not rflippers[i]
            # group the segments
            temp, lgroup = [], []
            for els in lflippers:
                if len(temp) == 0:
                    temp = [els]
                elif els == temp[0]:
                    temp.append(els)
                else:
                    lgroup.append(temp)
                    temp = [els]
            else:
                if len(temp) != 0:
                    lgroup.append(temp)
            temp, rgroup = [], []
            for ers in rflippers:
                if len(temp) == 0:
                    temp = [ers]
                elif ers == temp[0]:
                    temp.append(ers)
                else:
                    rgroup.append(temp)
                    temp = [ers]
            else:
                if len(temp) != 0:
                    rgroup.append(temp)
            # bool to range (0 to 1)
            lsegments, skipper = [], 0
            for i, g in enumerate(lgroup):
                if g[0]:
                    lsegments.append((lticks[i+skipper], lticks[i+skipper+len(g)]))
                    skipper += len(g) - 1
            rsegments, skipper = [], 0
            for i, g in enumerate(rgroup):
                if g[0]:
                    rsegments.append((rticks[i+skipper], rticks[i+skipper+len(g)]))
                    skipper += len(g) - 1
            # lr combo then sort
            lr_combo = map(lambda p: sorted(p, key=lambda k: k[0]), product(lsegments, rsegments))
            lr_combo = filter(lambda lrc: lrc[0][1] > lrc[1][0], lr_combo)
            lr_combo = list(map(lambda flrc: sorted([*flrc[0], *flrc[1]])[1:3], lr_combo))
            # if False:
            #     print(name, '|', x0, y0, z0, '->', x1, y1, z1)
            #     print(res)
            #     print(masks)
            #     print(left)
            #     print(right)
            #     print(lflippers)
            #     print(rflippers)
            #     print(lgroup)
            #     print(rgroup)
            #     print(lsegments)
            #     print(rsegments)
            #     print(lticks)
            #     print(rticks)
            #     print(lr_combo)
            #     print(self._c[masks])
            #     print(self._d[masks])
            #     pass
            joints = []
            for bgn, end in lr_combo:
                r0, r1 = np.array([x0, y0, z0]), np.array([x1, y1, z1])
                r = r1 - r0
                r0, r1 = r0 + bgn * r, r0 + end * r
                if np.linalg.norm(r1 - r0) < self._t:
                    # under tolerance
                    continue
                ut = r1 - r0
                ut /= np.linalg.norm(ut)
                # get index of parallel
                parallel = np.unique(self._cd[masks][(res[:, 0] == -3) & (res[:, 5] == m)], axis=0)
                if parallel.shape[0] > 0:
                    offset0, offset1 = np.dot(r0, ut), np.dot(r1, ut)
                    # butt joint only
                    for p in parallel:
                        p0, p1 = np.dot(p[3:], ut), np.dot(p[:3], ut)
                        # s has 2 or 3 or 4 members
                        s = sorted(list({offset0, offset1, p0, p1}))
                        # trim
                        s = s[s.index(offset0):s.index(offset1)+1]
                        if len(s) == 2:
                            # member of 2, either butt joint or else
                            if p0 < p1:
                                if s[0] >= p0 and s[1] <= p1:
                                    # p0 s[0] s[1] p1
                                    joints.append((name, m, *r0, *r1, x0, y0, z0, x1, y1, z1, *p[3:], *p[:3], 1))
                                else:
                                    if s[0] < s[1] <= p0 < p1 or p0 < p1 <= s[0] < s[1]:
                                        joints.append((name, m, *r0, *r1, x0, y0, z0, x1, y1, z1, *[np.nan for _ in range(6)], 0))
                                    else:
                                        continue
                            else:
                                if s[0] >= p1 and s[1] <= p0:
                                    # p1 s[0] s[1] p0
                                    joints.append((name, m, *r0, *r1, x0, y0, z0, x1, y1, z1, *p[3:], *p[:3], 1))
                                else:
                                    if s[0] < s[1] <= p1 < p0 or p1 < p0 <= s[0] < s[1]:
                                        joints.append((name, m, *r0, *r1, x0, y0, z0, x1, y1, z1, *[np.nan for _ in range(6)], 0))
                                    else:
                                        continue
                        else:
                            # combination of joint type
                            if len(s) == 4:
                                # center is parallel
                                joint_type = [0, 1, 0]
                            else:
                                # length is 3, either p0 or p1 is outside/bordering
                                if offset0 < p0 < offset1:
                                    # p1 is outside/bordering
                                    if p1 <= offset0:
                                        # towards offset0
                                        joint_type = [1, 0]
                                    else:
                                        # towards offset1
                                        joint_type = [0, 1]
                                else:
                                    # p0 is outside/bordering
                                    if p0 <= offset0:
                                        # towards offset0
                                        joint_type = [1, 0]
                                    else:
                                        # towards offset1
                                        joint_type = [0, 1]
                            # after finding joint type
                            for i, jt in zip(range(len(s)-1), joint_type):
                                r0_ = r0 + ut * (s[i] - offset0)
                                r1_ = r0 + ut * (s[i+1] - offset0)
                                # if split butt and t-joint
                                if jt == 1:
                                    # both trimmed point are within p0 and p1
                                    joints.append((name, m, *r0_, *r1_, x0, y0, z0, x1, y1, z1, *p[3:], *p[:3], 1))
                                else:
                                    joints.append((name, m, *r0_, *r1_, x0, y0, z0, x1, y1, z1, *[np.nan for _ in range(6)], 0))
                        # break, important, stop looking
                        break
                else:
                    # t-joint only
                    joints.append((name, m, *r0, *r1, x0, y0, z0, x1, y1, z1, *[np.nan for _ in range(6)], 0))
            return joints

        # return
        mates = set(left[:, 3]).intersection(set(right[:, 3]))
        to_return = []
        # for mate in mates:
        #     to_return.append(_mate_iterator(mate))
        to_return = tuple(map(_mate_iterator, mates))
        return to_return

    def _part_iterator(self, sdf):
        mask = self._df['name'].to_numpy() != sdf['name'].to_numpy()[0]
        # near cd plane
        n = sdf[['nx', 'ny', 'nz']].to_numpy()[0]
        depth = sdf['depth'].to_numpy()[0]
        n_offset = np.dot(n, sdf[['x0', 'y0', 'z0']].to_numpy()[0])
        tol = depth + self._t + self._pdepth
        c_from_n = np.abs(np.sum(n * self._c, axis=1) - n_offset) <= tol
        d_from_n = np.abs(np.sum(n * self._d, axis=1) - n_offset) <= tol 
        part_mask_1 = (c_from_n | d_from_n)
        part_mask_1 = np.isin(self._names_flat, np.unique(self._names_flat[part_mask_1]))
        # crossing cd plane
        c_from_n, d_from_n = np.sum(n * self._c, axis=1) - n_offset, np.sum(n * self._d, axis=1) - n_offset
        # if negative, crossing (on different sides)
        part_mask_2 = (np.copysign(1, c_from_n) * np.copysign(1, d_from_n)) <= 0
        part_mask_2 = np.isin(self._names_flat, np.unique(self._names_flat[part_mask_2]))
        # near cd plane mask, near or crossing ab mask, near or overlapping ab ends mask
        mask &= part_mask_1 | part_mask_2
        # pass the mask
        joints = []
        # for row in sdf.iterrows():
        #     joints.append(self._line_iterator(row, deepcopy(mask)))
        joints = list(map(self._line_iterator, sdf.iterrows(), [deepcopy(mask) for _ in range(sdf.shape[0])]))
        return joints

    def find_joint(self):
        if self._engine == 2:
            self._cx, self._cy, self._cz = self._df['x0'].to_numpy(), self._df['y0'].to_numpy(), self._df['z0'].to_numpy()
            self._dx, self._dy, self._dz = self._df['x1'].to_numpy(), self._df['y1'].to_numpy(), self._df['z1'].to_numpy()
            self._px, self._py, self._pz = self._df['nx'].to_numpy(), self._df['ny'].to_numpy(), self._df['nz'].to_numpy()
        else:
            pass
        #
        self._c = self._df[['x0', 'y0', 'z0']].to_numpy()
        self._d = self._df[['x1', 'y1', 'z1']].to_numpy()
        self._p = self._df[['nx', 'ny', 'nz']].to_numpy()
        self._cd = self._df[['x0', 'y0', 'z0', 'x1', 'y1', 'z1']].to_numpy()
        #
        cds = self._d - self._c
        ucds = cds / np.linalg.norm(cds, axis=1).reshape(-1, 1)
        cross = np.cross(self._p, ucds, axis=1)
        self._df['Xx'], self._df['Xy'], self._df['Xz'] = cross[:, 0], cross[:, 1], cross[:, 2]
        self._df['a_offset'], self._df['b_offset'] = np.sum(ucds * self._c, axis=1), np.sum(ucds * self._d, axis=1)
        self._df['abx'], self._df['aby'], self._df['abz'] = ucds[:, 0], ucds[:, 1], ucds[:, 2]
        #
        self._pdepth = self._df['depth'].to_numpy()
        self._ph = np.ones((self._df.shape[0], 5)).astype(float) * -1
        self._names_flat = self._df['name'].to_numpy()
        self._names = self._names_flat.reshape(-1, 1)
        #
        columns = ['name', 'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 'nx', 'ny', 'nz', 'depth', 'Xx', 'Xy', 'Xz']
        columns += ['abx', 'aby', 'abz', 'a_offset', 'b_offset']
        if self._these_only is not None:
            select = self._df.loc[self._df['name'].isin(self._these_only), columns]
        else:
            select = self._df.loc[:, columns]
        select = select.reset_index(drop=True)
        joints = []

        # if import, use process/thread-pool or linear
        # else, use pandas group apply
        if is_import:
            # only use half of virtual cores (multithreading turns one physical core into two virtual cores)
            n_worker = multiprocessing.cpu_count() // 2
            if n_worker == 0:
                n_worker = 1
            wait_for = []
            try:
                # gpu uses threadpool
                if self._engine == 2:
                    raise Exception
                with concurrent.futures.ProcessPoolExecutor(n_worker) as executor:
                    for i, g in select.groupby('name'):
                        wait_for.append(executor.submit(self._part_iterator, g))
                    for f in tqdm(concurrent.futures.as_completed(wait_for), total=len(wait_for)):
                        joints.append(f.result())
            except:
                # gpu uses threadpool
                if self._engine != 2:
                    print('Unable to processpool')
                try:
                    with concurrent.futures.ThreadPoolExecutor(n_worker) as executor:
                        for i, g in select.groupby('name'):
                            wait_for.append(executor.submit(self._part_iterator, g))
                        for f in tqdm(concurrent.futures.as_completed(wait_for), total=len(wait_for)):
                            joints.append(f.result())
                except:
                    print('Unable to threadpool')
                    for i, g in tqdm(select.groupby('name')):
                        joints.append(self._part_iterator(g))
        else:
            # run
            joints = select.groupby('name', group_keys=False).apply(self._part_iterator)

        # linear iteration
        # for i, g in tqdm(select.groupby('name')):
        #     joints.append(self._part_iterator(g))

        # process pool
        # wait_for = []
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     for i, g in select.groupby('name'):
        #         wait_for.append(executor.submit(self._part_iterator, g))
        #     for f in tqdm(concurrent.futures.as_completed(wait_for), total=len(wait_for)):
        #         joints.append(f.result())
        
        # pandas group apply
        # if is_import:
        #     tqdm.pandas()
        #     joints = select.groupby('name', group_keys=False).progress_apply(self._part_iterator)
        # else:
        #     joints = select.groupby('name', group_keys=False).apply(self._part_iterator)
        
        # flatten
        joints = filter(lambda joint: len(joint) > 0, joints)
        joints = chain.from_iterable(joints)
        joints = chain.from_iterable(joints)
        joints = chain.from_iterable(joints)
        # return list(joints)
        return pd.DataFrame(list(joints), columns=['A_name', 'B_name', 
                                                   'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 
                                                   'A_x0', 'A_y0', 'A_z0', 'A_x1', 'A_y1', 'A_z1', 
                                                   'B_x0', 'B_y0', 'B_z0', 'B_x1', 'B_y1', 'B_z1', 
                                                   'type'])


# if not import (run through shell)
def main(data, chunk, tol, angtol, engine):
    # bridging function to invoke object method
    return JointFinder(data, tolerance=tol, angular_tolerance=angtol, select_only=chunk, engine=engine).find_joint()


if __name__ == '__main__':
    is_import = False

    # system arguments
    config = {'dpath': 'data.pkl', 'tpath': 'joints.pkl', 'tol': 0.001, 'angtol': 0.001, 'batch': 100, 'engine': 0, 'select': None}
    sysvar = sys.argv
    if len(sysvar) > 1:
        for k, v in dict(map(lambda var: var.split('='), sysvar[1:])).items():
            if k in ['dpath', 'tpath', 'select']:
                config[k] = str(v)
            elif k in ['batch', 'tol', 'angtol', 'engine']:
                config[k] = int(v)
            else:
                print(f"{k} is not a valid variable")
    dpath, tpath = config['dpath'], config['tpath']
    tol, angtol = config['tol'], config['angtol']
    batch, engine = config['batch'], config['engine']
    if engine not in [0, 1, 2]:
        print('Engine option invalid, select 0 or 1 or 2')
        print('Default 1 is set')
        engine = 1

    if config['select'] is not None:
        config['select'] = int(config['select'])

    with open(dpath, 'rb') as f:
        data = pickle.load(f)

    if config['select'] is None:
        names = np.unique(data['name'].to_numpy())
        big = names.shape[0] % batch
        small = batch - big
        col = ceil(names.shape[0] / batch)
        if big:
            b = names[:big*col].reshape((big, col)).tolist()
            s = names[big*col:].reshape((batch - big, col - 1)).tolist()
            chunked = b + s
        else:
            # all same size
            chunked = names[:batch*col].reshape((batch, col)).tolist()
    else:
        chunked = [[config['select']]]
    # print(chunked)

    joints = []
    if config['select'] is None:
        # only use half of virtual cores (multithreading turns one physical core into two virtual cores)
        n_worker = multiprocessing.cpu_count() // 2
        if n_worker == 0:
            n_worker = 1
        try:
            wait_for = []
            with concurrent.futures.ProcessPoolExecutor(n_worker) as executor:
                for chunk in chunked:
                    wait_for.append(executor.submit(main, data, chunk, tol, angtol, engine))
                for f in tqdm(concurrent.futures.as_completed(wait_for), total=len(chunked)):
                    joints.append(f.result())
        except:
            print('Unable to processpool')
            try:
                with concurrent.futures.ThreadPoolExecutor(n_worker) as executor:
                    for chunk in chunked:
                        wait_for.append(executor.submit(main, data, chunk, tol, angtol, engine))
                    for f in tqdm(concurrent.futures.as_completed(wait_for), total=len(chunked)):
                        joints.append(f.result())
            except:
                print('Unable to threadpool')
                for chunk in tqdm(chunked):
                    joints.append(main(data, chunk, tol, angtol, engine))
    else:
        for chunk in tqdm(chunked):
            joints.append(main(data, chunk, tol, angtol, engine))

    joints = pd.concat(joints, sort=False).reset_index(drop=True)
    print('Result:')
    print(joints)
    print(f"Saved as: {tpath}")
    
    with open(tpath, 'wb') as f:
        pickle.dump(joints, f)
