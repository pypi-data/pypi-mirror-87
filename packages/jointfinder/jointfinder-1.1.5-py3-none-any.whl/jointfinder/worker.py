import numpy as np
from copy import deepcopy
from math import acos, sqrt, copysign, degrees
# pd alias is reserved, do not use for pandas


def vfunc(a, b, q, qd, c, d, p, pd, t, at):
        
    # initialize
    tol, ang_tol = t, at
    ab_depth = np.array([qd, qd, qd])
    cd_depth = np.array([pd, pd, pd])
    
    # --------------------------------------- INPUT CHECK -----------------------------------------------

    # plane vector must be unit
    if not 0.99 <= np.linalg.norm(q) <= 1 or not 0.99 <= np.linalg.norm(p) <= 1:
        return -1, -1, -1, -1, -1
    
    # ab MUST be within cd's depth
    pcd1, pab1 = np.dot(c, p), np.dot(a, p)
    pcd2, pab2 = pcd1 + np.dot(cd_depth, p), pab1 + np.dot(ab_depth, p)
    if pcd1 > pcd2:
        pcd1 += tol
        pcd2 -= tol
    else:
        pcd1 -= tol
        pcd2 += tol
    pabcds = np.sort(np.array([pcd1, pcd2, pab1, pab2]))
    pabs = np.sort(np.array([pab1, pab2]))
    if not np.array_equal(pabcds[1:3], pabs):
        return -1, -1, -1, -1, -1
    
    # ab and cd must NOT be points
    ab, cd = b - a, d - c
    ab_mag, cd_mag = np.linalg.norm(ab), np.linalg.norm(cd)
    if ab_mag == 0 or cd_mag == 0:
        return -1, -1, -1, -1, -1
    
    # p cross cd and p cross ab MUST be real
    pcd, pab = np.cross(p, cd), np.cross(p, ab)
    pcd_mag, pab_mag = np.linalg.norm(pcd), np.linalg.norm(pab)
    if pcd_mag == 0 or pab_mag == 0:
        return -1, -1, -1, -1, -1

    # ----------------------------------------- CONSTANTS ------------------------------------------------

    # unit vectors
    uab, upab = ab/ab_mag, pab/pab_mag
    ucd, upcd = cd/cd_mag, pcd/pcd_mag

    # pcd offset baseline
    pcd_from_origin = np.dot(c, upcd)

    # a and b along pcd vector
    a_from_origin_along_pcd = np.dot(a, upcd)
    b_from_origin_along_pcd = np.dot(b, upcd)
    a_from_pcd = a_from_origin_along_pcd - pcd_from_origin
    b_from_pcd = b_from_origin_along_pcd - pcd_from_origin

    # a and b shadows after applying its depth
    _a, _b = ab_depth * q + a, ab_depth * q + b

    # get offsets accounting ab's depth
    _a_from_origin_along_pcd = np.dot(_a, upcd)
    _b_from_origin_along_pcd = np.dot(_b, upcd)
    _a_from_pcd = _a_from_origin_along_pcd - pcd_from_origin
    _b_from_pcd = _b_from_origin_along_pcd - pcd_from_origin

    # pab offset baseline
    pab_from_origin = np.dot(a, upab)

    # c and d along pab vector
    c_from_origin_along_pcd = np.dot(c, upab)
    d_from_origin_along_pcd = np.dot(d, upab)
    c_from_pab = c_from_origin_along_pcd - pab_from_origin
    d_from_pab = c_from_origin_along_pcd - pab_from_origin

    # where c and d along its own vector, a and b on cd's vector
    a_from_origin_along_cd = np.dot(a, ucd)
    b_from_origin_along_cd = np.dot(b, ucd)
    c_from_origin_along_cd = np.dot(c, ucd)
    d_from_origin_along_cd = np.dot(d, ucd)

    # where a and b along its own vector, c and d on ab's vector
    a_from_origin_along_ab = np.dot(a, uab)
    b_from_origin_along_ab = np.dot(b, uab)
    c_from_origin_along_ab = np.dot(c, uab)
    d_from_origin_along_ab = np.dot(d, uab)

    # i_offset_along_ab and i_offset_along_cd set later

    # ------------------------------------------- FLAGS ---------------------------------------------------

    # ab cd angle, abcd_theta is cos of ab with cd
    abcd_theta = np.dot(ab, cd) / (ab_mag * cd_mag)

    # to avoid math domain error when acos
    if abs(abcd_theta) > 1:
        abcd_theta = copysign(1, abcd_theta)

    # 90 - 270 degress has cos theta value as negative
    if abcd_theta < 0:
        is_oblique = True
    else:
        is_oblique = False

    # limit if not right angle
    lim = tol if abcd_theta == 0 else tol / abs(abcd_theta)

    # maximum is 10 billion, not max of float64
    if lim > 1E10:
        lim = 1E10

    # convert to degrees, then determine if parallel and perpendicular
    abcd_theta = degrees(acos(abcd_theta)) % 360
    if a_from_pcd - b_from_pcd == 0 or abs(abcd_theta % 180) <= ang_tol:
        is_parallel, is_perpendicular = True, False
    else:
        is_parallel = False
        if abs(abcd_theta % 90) <= ang_tol:
            is_perpendicular = True
        else:
            is_perpendicular = False

    # --------------------------------------- TAB AND INSIDE -----------------------------------------------

    # parallel and not parallel have different undertakings
    # to determine tab and left right boundaries
    #
    # tab is t in vector equation r = r0 + t * n
    # r0 is origin, n is vector which r and r0 on, t is offset
    # r0 here being a, r is intersection point with cd, t is offset of n (ab) from origin (a)
    #
    # whether the boundaries fall on left or right will be determined later
    # determine i0 and i1 first, i0 is closest to a
    if is_parallel:
        # parallel does not actually have tab
        # line up to check later if a and b is within c and d (with tolerace)
        s = np.sort(np.array([a_from_origin_along_cd, 
                            b_from_origin_along_cd, 
                            c_from_origin_along_cd - tol, 
                            d_from_origin_along_cd + tol]))
        # a and b to lined up as well
        s_ab = np.sort(np.array([a_from_origin_along_cd, b_from_origin_along_cd]))
        # check if lined up ab on either end, it needs to overlap a little not just touching
        if np.array_equal(s[:2], s_ab) or np.array_equal(s[-2:], s_ab):
            # ab not overlapping cd, along cd's vector
            # non-overlapping parallel
            tab = -1
            if a_from_origin_along_ab < b_from_origin_along_ab:
                if c_from_origin_along_ab < a_from_origin_along_ab:
                    i0, i1 = 0, 0
                else:
                    i0, i1 = 1, 1
            else:
                if c_from_origin_along_ab > a_from_origin_along_ab:
                    i0, i1 = 0, 0
                else:
                    i0, i1 = 1, 1
        else:
            # overlapping parallel
            # check if parallel near pcd depth/tolerance
            pcd_l, pcd_u = pcd_from_origin - tol, pcd_from_origin + tol
            # line up upper and lower limits, a and b along pcd vectors
            a_or_b = a_from_origin_along_pcd \
                    if abs(a_from_origin_along_pcd) >= abs(b_from_origin_along_pcd) else \
                    b_from_origin_along_pcd
            # account a and b depth
            _a_or_b = _a_from_origin_along_pcd \
                    if abs(_a_from_origin_along_pcd) >= abs(_b_from_origin_along_pcd) else \
                    _b_from_origin_along_pcd
            s = np.sort(np.array([pcd_l, pcd_u, a_or_b, _a_or_b]))
            s_aabb = np.sort(np.array([a_or_b, _a_or_b]))
            # touching is fine
            if s[1] != s[2] and (np.array_equal(s[:2], s_aabb) or np.array_equal(s[2:], s_aabb)):
                # far parallel
                tab = -2
            else:
                # true parallel
                tab = -3
            # line up without tolerance
            s = np.sort(np.array([a_from_origin_along_ab, b_from_origin_along_ab, 
                                c_from_origin_along_ab, d_from_origin_along_ab]))
            s_ab = np.sort(np.array([a_from_origin_along_ab, b_from_origin_along_ab]))
            # must not just touch
            if np.array_equal(s[:2], s_ab) or np.array_equal(s[-2:], s_ab):
                if a_from_origin_along_ab < b_from_origin_along_ab:
                    if c_from_origin_along_ab < a_from_origin_along_ab:
                        i0, i1 = 0, 0
                    else:
                        i0, i1 = 1, 1
                else:
                    if c_from_origin_along_ab > a_from_origin_along_ab:
                        i0, i1 = 0, 0
                    else:
                        i0, i1 = 1, 1
            else:
                i0, i1 = (s[1] - a_from_origin_along_ab) / ab_mag, (s[2] - a_from_origin_along_ab) / ab_mag
    else:
        # not parallel, intersection only exists here
        tab = a_from_pcd / (a_from_pcd - b_from_pcd)
        # i is intersection, then check if intersection within cd, apply tolerance
        # original value to tab is essential to find intersection
        intersection = a + tab * ab
        i_from_origin_along_ab = np.dot(intersection, uab)
        i_from_origin_along_cd = np.dot(intersection, ucd)
        # accounting ab's depth
        _i = intersection + ab_depth * q
        _i_from_origin_along_cd = np.dot(_i, ucd)
        # check if crossing between cd
        if c_from_origin_along_cd < d_from_origin_along_cd:
            s = np.sort(np.array([c_from_origin_along_cd - lim, d_from_origin_along_cd + lim, 
                                i_from_origin_along_cd, _i_from_origin_along_cd]))
            # limit of right angle is equal to tolerance
            s_cd = np.sort(np.array([c_from_origin_along_cd - lim, d_from_origin_along_cd + lim]))
        else:
            s = np.sort(np.array([c_from_origin_along_cd + lim, d_from_origin_along_cd - lim, 
                                i_from_origin_along_cd, _i_from_origin_along_cd]))
            # limit of right angle is equal to tolerance
            s_cd = np.sort(np.array([c_from_origin_along_cd + lim, d_from_origin_along_cd - lim]))
        # just touching is fine
        # if is_offside or (s[1] != s[2] and (s[:2] == s_io or s[2:] == s_io)):
        if s[1] != s[2] and (np.array_equal(s[:2], s_cd) or np.array_equal(s[2:], s_cd)):
            # outside
            tab = -1
        # tab can be changed after finding intersection
        else:
            # within cd, simplify t
            if tab < 0:
                tab = 0
            elif tab > 1:
                tab = 1
        # finding inside
        if is_perpendicular:
            i0, i1 = -1, -1
        else:
            # line up abcdi along ab
            s = np.sort(np.array([a_from_origin_along_ab, b_from_origin_along_ab, 
                                c_from_origin_along_ab, d_from_origin_along_ab]))
            # see where cd are
            # s_cd = sorted([c_offset_along_ab, d_offset_along_ab])
            s_cd = np.sort(np.array([c_from_origin_along_ab, d_from_origin_along_ab]))
            if np.array_equal(s[:2], s_cd) or np.array_equal(s[-2:], s_cd):
                # at the ends, no inside, no i0 i1
                if np.array_equal(s[:2], s_ab) or np.array_equal(s[-2:], s_ab):
                    if a_from_origin_along_ab < b_from_origin_along_ab:
                        if c_from_origin_along_ab < a_from_origin_along_ab:
                            i0, i1 = 0, 0
                        else:
                            i0, i1 = 1, 1
                    else:
                        if c_from_origin_along_ab > a_from_origin_along_ab:
                            i0, i1 = 0, 0
                        else:
                            i0, i1 = 1, 1
            else:
                # at neither end
                i0, i1 = (s[1] - a_from_origin_along_ab) / ab_mag, (s[2] - a_from_origin_along_ab) / ab_mag

    # ------------------------------------- SIDE AND ACCUMULATOR -------------------------------------------

    # to determine side
    # side_determiner variable is distance and (most importantly, direction) from pab
    if i0 > 0 or i1 > 0:
        # determine side chooser, either c or d
        if is_parallel:
            if tab == -3:
                # true parallel, near
                if not is_oblique:
                    # ab and cd same direction, pab and pcd relatively similar
                    # as cd is sequenced left thumb-wise (thumb is normal, finger is cd)
                    # set positive value to make a and b inward, left side of pab
                    side_determiner = 1
                else:
                    # pab and pcd same opposing direction, put side_determiner left side of pab
                    side_determiner = -1
            else:
                # far parallel, either c or d will do
                side_determiner = c_from_pab
        else:
            # not parallel cases
            # check if c and d the same side of ab
            if copysign(1, c_from_pab) == copysign(1, d_from_pab):
                # both c and d same side of pab, either c or d will do
                side_determiner = c_from_pab
            elif c_from_pab == 0:
                # c touching ab, set as d's side
                side_determiner = d_from_pab
            elif d_from_pab == 0:
                # d touching ab, set as c's side
                side_determiner = c_from_pab
            else:
                # different sides exist, not perpendicular
                # if perpendicular, i0 and i1 both 0, will not reach here
                side_determiner = None
        # check crossing
        if side_determiner is None:
            # cd crosses ab, may or may not be inside ab
            if a_from_origin_along_ab <= i_from_origin_along_ab <= b_from_origin_along_ab:
                # cd crosses ab inside ab
                i05 = (i_from_origin_along_ab - a_from_origin_along_ab) / ab_mag
                # pab upright p direction ab, splits space into left right
                # left: true > near to far, cancel > far to near
                # right: true > far to near, cancel > near to far
                if c_from_pab > d_from_pab:
                    # cd left to right
                    if is_oblique:
                        # left cancel, right true
                        # far to near
                        l0, l1, r0, r1 = i1, i05, i05, i0
                    else:
                        # left true, right cancel
                        # near to far
                        l0, l1, r0, r1 = i0, i05, i05, i1
                else:
                    # cd right to left
                    if is_oblique:
                        # left cancel, right true
                        # far to near
                        l0, l1, r0, r1 = i05, i0, i1, i05
                    else:
                        # left true, right cancel
                        # near to far
                        l0, l1, r0, r1 = i05, i1, i0, i05
            else:
                # cd crosses outside ab
                if a_from_origin_along_ab <= c_from_origin_along_ab <= b_from_origin_along_ab:
                    # c is within ab
                    if c_from_pab < 0:
                        # right side only
                        if is_oblique:
                            # true bound
                            l0, l1, r0, r1 = -1, -1, i1, i0
                        else:
                            # cancelling bound
                            l0, l1, r0, r1 = -1, -1, i0, i1
                    else:
                        # left only
                        if is_oblique:
                            # cancelling bound
                            l0, l1, r0, r1 = i1, i0, -1, -1
                        else:
                            # true bound
                            l0, l1, r0, r1 = i0, i1, -1, -1
                elif a_from_origin_along_ab <= d_from_origin_along_ab <= b_from_origin_along_ab:
                    # d is within ab
                    if d_from_pab < 0:
                        # right side only
                        if is_oblique:
                            # true bound
                            l0, l1, r0, r1 = -1, -1, i1, i0
                        else:
                            # cancelling bound
                            l0, l1, r0, r1 = -1, -1, i0, i1
                    else:
                        # left only
                        if is_oblique:
                            # cancelling bound
                            l0, l1, r0, r1 = i1, i0, -1, -1
                        else:
                            # true bound
                            l0, l1, r0, r1 = i0, i1, -1, -1
                else:
                    # crossing is outside ab
                    if i_from_origin_along_ab > b_from_origin_along_ab:
                        # beyond b
                        if c_from_origin_along_ab > b_from_origin_along_ab:
                            # c is beyond, use d
                            side_determiner = d_from_pab
                        else:
                            # d is beyond, use c
                            side_determiner = c_from_pab
                    else:
                        # under a
                        if c_from_origin_along_ab < a_from_origin_along_ab:
                            # c is under, use d
                            side_determiner = d_from_pab
                        else:
                            # d is under, use c
                            side_determiner = c_from_pab
                    if side_determiner < 0:
                        # right side only
                        if is_oblique:
                            # true bound
                            l0, l1, r0, r1 = -1, -1, i1, i0
                        else:
                            # cancelling bound
                            l0, l1, r0, r1 = -1, -1, i0, i1
                    else:
                        # left only
                        if is_oblique:
                            # cancelling bound
                            l0, l1, r0, r1 = i1, i0, -1, -1
                        else:
                            # true bound
                            l0, l1, r0, r1 = i0, i1, -1, -1
        else:
            # one side only (c or d touching ab), or parallel
            if side_determiner < 0:
                # right side only
                if is_oblique:
                    # true bound
                    l0, l1, r0, r1 = -1, -1, i1, i0
                else:
                    # cancelling bound
                    l0, l1, r0, r1 = -1, -1, i0, i1
            else:
                # left only
                if is_oblique:
                    # cancelling bound
                    l0, l1, r0, r1 = i1, i0, -1, -1
                else:
                    # true bound
                    l0, l1, r0, r1 = i0, i1, -1, -1
    else:
        l0, l1, r0, r1 = -1, -1, -1, -1

    return tab, l0, l1, r0, r1
