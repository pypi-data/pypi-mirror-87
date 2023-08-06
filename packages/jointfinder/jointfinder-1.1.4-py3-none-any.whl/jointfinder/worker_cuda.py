import platform
from numba import float64, guvectorize
from math import acos, sqrt, copysign, degrees


@guvectorize([(float64, float64, float64, float64, float64, float64, float64, float64, float64, float64,
               float64[:], float64[:], float64[:], float64[:], float64[:], float64[:], float64[:], float64[:], float64[:], float64[:], 
               float64, float64, 
               float64[:,:], float64[:,:])], 
             '(),(),(),(),(),(),(),(),(),(),(n),(n),(n),(n),(n),(n),(n),(n),(n),(n),(),(),(n,c5)->(n,c5)', 
             target='cuda', nopython=False if platform.system() in ['Darwin'] else True)
def vfunc(ax, ay, az, bx, by, bz, qx, qy, qz, depth_ab, 
          cxs, cys, czs, dxs, dys, dzs, pxs, pys, pzs, pds, 
          tol, ang_tol, ph, res):
    # iterate over the vector, ax ~ qd are scalar
    for i in range(ph.shape[0]):
        cx, cy, cz, dx, dy, dz, px, py, pz, depth_cd = cxs[i], cys[i], czs[i], dxs[i], dys[i], dzs[i], pxs[i], pys[i], pzs[i], pds[i]
        is_exit = False

        # --------------------------------------- INPUT CHECK -----------------------------------------------

        # plane vectors MUST be unit vectors
        if not 0.95 <= sqrt(px ** 2 + py ** 2 + pz ** 2) <= 1 or not 0.95 <= sqrt(qx ** 2 + qy ** 2 + qz ** 2) <= 1:
            is_exit = True

        # check a AND b inside cd's depth
        # cd_l and cd_u are the thickness of cd's shape
        cd_l = cx * px + cy * py + cz * pz
        cd_u = (cx + (px * depth_cd)) * px + (cy + (py * depth_cd)) * py + (cz + (pz * depth_cd)) * pz
        # determine top and bottom, then apply tolerance
        if cd_l < cd_u:
            cd_l, cd_u = cd_l - tol, cd_u + tol
        else:
            cd_l, cd_u = cd_u - tol, cd_l + tol
        # find a and b to check if it is inside cd's thickness/depth
        ap_1 = ax * px + ay * py + az * pz
        ap_2 = (ax + (qx * depth_ab)) * px + (ay + (qy * depth_ab)) * py + (az + (qz * depth_ab)) * pz
        
        # sort
        s0, s1, s2, s3 = cd_l, cd_u, ap_1, ap_2
        _s0, _s1 = ap_1, ap_2 
        if s0 >= s1 >= s2 >= s3: pass
        elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
        elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
        elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
        elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
        elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
        elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
        elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
        elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
        elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
        elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
        elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
        elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
        elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
        elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
        elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
        elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
        elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
        elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
        elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
        elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
        elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
        elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
        else: s0, s1, s2, s3 = s3, s2, s1, s0
        if _s1 > s0:
            _s0, _s1 = _s1, _s0

        # just touching is ok
        if s1 != s2 and ((s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1)):
            is_exit = True
            
        bp_1 = bx * px + by * py + bz * pz
        bp_2 = (bx + (qx * depth_ab)) * px + (by + (qy * depth_ab)) * py + (bz + (qz * depth_ab)) * pz

        # sort
        s0, s1, s2, s3 = cd_l, cd_u, bp_1, bp_2
        _s0, _s1 = bp_1, bp_2 
        if s0 >= s1 >= s2 >= s3: pass
        elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
        elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
        elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
        elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
        elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
        elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
        elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
        elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
        elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
        elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
        elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
        elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
        elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
        elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
        elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
        elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
        elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
        elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
        elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
        elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
        elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
        elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
        else: s0, s1, s2, s3 = s3, s2, s1, s0
        if _s1 > s0:
            _s0, _s1 = _s1, _s0

        # just touching is ok
        if s1 != s2 and ((s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1)):
            is_exit = True
        # possible to complicate; instead of must pass BOTH a and b, pass either
        # partial planar

        # ab is line, cd is boundary
        abx, aby, abz, cdx, cdy, cdz = bx - ax, by - ay, bz - az, dx - cx, dy - cy, dz - cz
        ab_mag, cd_mag = sqrt(abx ** 2 + aby ** 2 + abz ** 2), sqrt(cdx ** 2 + cdy ** 2 + cdz ** 2)
        if ab_mag == 0 or cd_mag == 0:
            is_exit = True

        # ab and cd on cd's surface vectors
        # pcd is cross of p and cd, pab is cross of p and ab
        pcd_x, pcd_y, pcd_z = py * cdz - pz * cdy, pz * cdx - px * cdz, px * cdy - py * cdx
        pab_x, pab_y, pab_z = py * abz - pz * aby, pz * abx - px * abz, px * aby - py * abx
        pcd_mag = sqrt(pcd_x ** 2 + pcd_y ** 2 + pcd_z ** 2)
        pab_mag = sqrt(pab_x ** 2 + pab_y ** 2 + pab_z ** 2)
        if pab_mag == 0 or pcd_mag == 0:
            # need to revisit pab again if partial planar is loosened
            is_exit = True

        if is_exit:
            res[i, 0] = -1
            res[i, 1] = -1
            res[i, 2] = -1
            res[i, 3] = -1
            res[i, 4] = -1
        else:
            # a and b are now within cd's depth (with tolerance)

            # ----------------------------------------- CONSTANTS ------------------------------------------------

            # unit vectors of ab and pab
            uabx, uaby, uabz = abx / ab_mag, aby / ab_mag, abz / ab_mag
            u_pab_x, u_pab_y, u_pab_z = pab_x / pab_mag, pab_y / pab_mag, pab_z / pab_mag

            # unit vectors of cd and pcd
            ucdx, ucdy, ucdz = cdx / cd_mag, cdy / cd_mag, cdz / cd_mag
            u_pcd_x, u_pcd_y, u_pcd_z = pcd_x / pcd_mag, pcd_y / pcd_mag, pcd_z / pcd_mag
            # pcd offset baseline
            pcd_offset = cx * u_pcd_x + cy * u_pcd_y + cz * u_pcd_z
            # a and b from pcd vector
            a_offset_along_pcd = ax * u_pcd_x + ay * u_pcd_y + az * u_pcd_z
            b_offset_along_pcd = bx * u_pcd_x + by * u_pcd_y + bz * u_pcd_z
            # a and b from pcd vector, negative is possible
            a_from_pcd = a_offset_along_pcd - pcd_offset
            b_from_pcd = b_offset_along_pcd - pcd_offset

            # where c and d along its own vector, a and b on cd's vector
            a_offset_along_cd = ucdx * ax + ucdy * ay + ucdz * az
            b_offset_along_cd = ucdx * bx + ucdy * by + ucdz * bz
            c_offset_along_cd = ucdx * cx + ucdy * cy + ucdz * cz
            d_offset_along_cd = ucdx * dx + ucdy * dy + ucdz * dz

            # where a and b along its own vector, c and d on ab's vector
            a_offset_along_ab = uabx * ax + uaby * ay + uabz * az
            b_offset_along_ab = uabx * bx + uaby * by + uabz * bz
            c_offset_along_ab = uabx * cx + uaby * cy + uabz * cz
            d_offset_along_ab = uabx * dx + uaby * dy + uabz * dz

            # a and b properties accounting ab's depth
            _ax, _ay, _az = (depth_ab * qx) + ax, (depth_ab * qy) + ay, (depth_ab * qz) + az
            _bx, _by, _bz = (depth_ab * qx) + bx, (depth_ab * qy) + by, (depth_ab * qz) + bz
            _a_from_pcd = _ax * u_pcd_x + _ay * u_pcd_y + _az * u_pcd_z - pcd_offset
            _b_from_pcd = _bx * u_pcd_x + _by * u_pcd_y + _bz * u_pcd_z - pcd_offset

            # pab offset baseline
            pab_offset = ax * u_pab_x + ay * u_pab_y + az * u_pab_z
            # c and d from pab vector, negative is possible
            c_from_pab = u_pab_x * cx + u_pab_y * cy + u_pab_z * cz - pab_offset
            d_from_pab = u_pab_x * dx + u_pab_y * dy + u_pab_z * dz - pab_offset

            # i_offset_along_ab and i_offset_along_cd set later

            # ------------------------------------------- FLAGS ---------------------------------------------------

            # ab cd angle, abcd_theta is cos of ab with cd
            abcd_theta = (abx * cdx + aby * cdy + abz * cdz) / (ab_mag * cd_mag)
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
            # maximum is 10 billion
            if lim > 1E10:
                lim = 1E10

            # convert to degrees, then determine if parallel and perpendicular
            abcd_theta = degrees(acos(abcd_theta)) % 360
            # if a_from_pcd - b_from_pcd == 0 or \
            #         abs(abcd_theta) <= ang_tol or \
            #         abs(abs(abcd_theta) - 180) <= ang_tol:
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

                # sort
                s0, s1, s2, s3 = a_offset_along_cd, b_offset_along_cd, c_offset_along_cd - tol, d_offset_along_cd + tol
                _s0, _s1 = a_offset_along_cd, b_offset_along_cd
                if s0 >= s1 >= s2 >= s3: pass
                elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
                elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
                elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
                elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
                elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
                elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
                elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
                elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
                elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
                elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
                elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
                elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
                elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
                elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
                elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
                elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
                elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
                elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
                elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
                elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
                elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
                elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
                else: s0, s1, s2, s3 = s3, s2, s1, s0
                if _s1 > s0:
                    _s0, _s1 = _s1, _s0

                # check if lined up ab on either end, it needs to overlap a little not just touching
                if (s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1):
                    # ab not overlapping cd, along cd's vector
                    # non-overlapping parallel
                    tab = -1
                    if a_offset_along_ab < b_offset_along_ab:
                        if c_offset_along_ab < a_offset_along_ab:
                            i0, i1 = 0, 0
                        else:
                            i0, i1 = 1, 1
                    else:
                        if c_offset_along_ab > a_offset_along_ab:
                            i0, i1 = 0, 0
                        else:
                            i0, i1 = 1, 1
                else:
                    # overlapping parallel
                    # get offsets accounting ab's depth
                    _a_offset_along_pcd = _ax * u_pcd_x + _ay * u_pcd_y + _az * u_pcd_z
                    _b_offset_along_pcd = _bx * u_pcd_x + _by * u_pcd_y + _bz * u_pcd_z
                    # check if parallel near pcd depth/tolerance
                    pcd_l, pcd_u = pcd_offset - tol, pcd_offset + tol
                    # line up upper and lower limits, a and b along pcd vectors
                    a_or_b = a_offset_along_pcd if abs(a_offset_along_pcd) >= abs(b_offset_along_pcd) else \
                        b_offset_along_pcd
                    # account a and b depth
                    _a_or_b = _a_offset_along_pcd if abs(_a_offset_along_pcd) >= abs(_b_offset_along_pcd) else \
                        _b_offset_along_pcd

                    # sort
                    s0, s1, s2, s3 = pcd_l, pcd_u, a_or_b, _a_or_b
                    _s0, _s1 = a_or_b, _a_or_b
                    if s0 >= s1 >= s2 >= s3: pass
                    elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
                    elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
                    elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
                    elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
                    elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
                    elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
                    elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
                    elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
                    elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
                    elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
                    elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
                    elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
                    elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
                    elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
                    elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
                    elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
                    elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
                    elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
                    elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
                    elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
                    elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
                    elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
                    else: s0, s1, s2, s3 = s3, s2, s1, s0
                    if _s1 > s0:
                        _s0, _s1 = _s1, _s0

                    # touching is fine
                    if s1 != s2 and ((s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1)):
                        # far parallel
                        tab = -2
                    else:
                        # true parallel
                        tab = -3
                    # line up without tolerance

                    # sort
                    s0, s1, s2, s3 = a_offset_along_ab, b_offset_along_ab, c_offset_along_ab, d_offset_along_ab
                    _s0, _s1 = a_offset_along_ab, b_offset_along_ab
                    if s0 >= s1 >= s2 >= s3: pass
                    elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
                    elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
                    elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
                    elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
                    elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
                    elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
                    elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
                    elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
                    elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
                    elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
                    elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
                    elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
                    elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
                    elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
                    elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
                    elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
                    elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
                    elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
                    elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
                    elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
                    elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
                    elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
                    else: s0, s1, s2, s3 = s3, s2, s1, s0
                    if _s1 > s0:
                        _s0, _s1 = _s1, _s0

                    # must not just touch
                    if (s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1):
                        if a_offset_along_ab < b_offset_along_ab:
                            if c_offset_along_ab < a_offset_along_ab:
                                i0, i1 = 0, 0
                            else:
                                i0, i1 = 1, 1
                        else:
                            if c_offset_along_ab > a_offset_along_ab:
                                i0, i1 = 0, 0
                            else:
                                i0, i1 = 1, 1
                    else:
                        i0, i1 = (s1 - a_offset_along_ab) / ab_mag, (s2 - a_offset_along_ab) / ab_mag
            else:
                # not parallel
                # finding tab to find intersection
                tab = a_from_pcd / (a_from_pcd - b_from_pcd)
                # i is intersection, then check if intersection within cd, apply tolerance
                # original value to tab is essential to find intersection
                ix, iy, iz = ax + tab * abx, ay + tab * aby, az + tab * abz
                i_offset_along_ab = uabx * ix + uaby * iy + uabz * iz
                i_offset_along_cd = ucdx * ix + ucdy * iy + ucdz * iz
                # accounting ab's depth
                _ix, _iy, _iz = ix + (depth_ab * qx), iy + (depth_ab * qy), iz + (depth_ab * qz)
                _i_offset_along_cd = ucdx * _ix + ucdy * _iy + ucdz * _iz
                # check if crossing between cd

                # sort
                s0, s1, s2, s3 = c_offset_along_cd - lim, d_offset_along_cd + lim, i_offset_along_cd, _i_offset_along_cd
                _s0, _s1 = c_offset_along_cd - lim, d_offset_along_cd + lim
                if s0 >= s1 >= s2 >= s3: pass
                elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
                elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
                elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
                elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
                elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
                elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
                elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
                elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
                elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
                elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
                elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
                elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
                elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
                elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
                elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
                elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
                elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
                elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
                elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
                elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
                elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
                elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
                else: s0, s1, s2, s3 = s3, s2, s1, s0
                if _s1 > s0:
                    _s0, _s1 = _s1, _s0

                # just touching is fine
                # if is_offside or (s[1] != s[2] and (s[:2] == s_io or s[2:] == s_io)):
                if s1 != s2 and ((s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1)):
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
                    i0, i1 = 0, 0
                else:
                    # line up abcdi along ab

                    # sort
                    s0, s1, s2, s3 = a_offset_along_ab, b_offset_along_ab, c_offset_along_ab, d_offset_along_ab
                    _s0, _s1 = c_offset_along_ab, d_offset_along_ab
                    if s0 >= s1 >= s2 >= s3: pass
                    elif s0 >= s1 >= s3 >= s2: s0, s1, s2, s3 = s0, s1, s3, s2
                    elif s0 >= s2 >= s1 >= s3: s0, s1, s2, s3 = s0, s2, s1, s3
                    elif s0 >= s2 >= s3 >= s1: s0, s1, s2, s3 = s0, s2, s3, s1
                    elif s0 >= s3 >= s1 >= s2: s0, s1, s2, s3 = s0, s3, s1, s2
                    elif s0 >= s3 >= s2 >= s1: s0, s1, s2, s3 = s0, s3, s2, s1
                    elif s1 >= s0 >= s2 >= s3: s0, s1, s2, s3 = s1, s0, s2, s3
                    elif s1 >= s0 >= s3 >= s2: s0, s1, s2, s3 = s1, s0, s3, s2
                    elif s1 >= s2 >= s0 >= s3: s0, s1, s2, s3 = s1, s2, s0, s3
                    elif s1 >= s2 >= s3 >= s0: s0, s1, s2, s3 = s1, s2, s3, s0
                    elif s1 >= s3 >= s0 >= s2: s0, s1, s2, s3 = s1, s3, s0, s2
                    elif s1 >= s3 >= s2 >= s0: s0, s1, s2, s3 = s1, s3, s2, s0
                    elif s2 >= s0 >= s1 >= s3: s0, s1, s2, s3 = s2, s0, s1, s3
                    elif s2 >= s0 >= s3 >= s1: s0, s1, s2, s3 = s2, s0, s3, s1
                    elif s2 >= s1 >= s0 >= s3: s0, s1, s2, s3 = s2, s1, s0, s3
                    elif s2 >= s1 >= s3 >= s0: s0, s1, s2, s3 = s2, s1, s3, s0
                    elif s2 >= s3 >= s0 >= s1: s0, s1, s2, s3 = s2, s3, s0, s1
                    elif s2 >= s3 >= s1 >= s0: s0, s1, s2, s3 = s2, s3, s1, s0
                    elif s3 >= s0 >= s1 >= s2: s0, s1, s2, s3 = s3, s0, s1, s2
                    elif s3 >= s0 >= s2 >= s1: s0, s1, s2, s3 = s3, s0, s2, s1
                    elif s3 >= s1 >= s0 >= s2: s0, s1, s2, s3 = s3, s1, s0, s2
                    elif s3 >= s1 >= s2 >= s0: s0, s1, s2, s3 = s3, s1, s2, s0
                    elif s3 >= s2 >= s0 >= s1: s0, s1, s2, s3 = s3, s2, s0, s1
                    else: s0, s1, s2, s3 = s3, s2, s1, s0
                    if _s1 > s0:
                        _s0, _s1 = _s1, _s0

                    if (s0 == _s0 and s1 == _s1) or (s2 == _s0 and s3 == _s1):
                        # at the ends, no inside, no i0 i1
                        i0, i1 = 0, 0
                    else:
                        # at neither end
                        i0, i1 = (s1 - a_offset_along_ab) / ab_mag, (s2 - a_offset_along_ab) / ab_mag

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
                    if a_offset_along_ab <= i_offset_along_ab <= b_offset_along_ab:
                        # cd crosses ab inside ab
                        i05 = (i_offset_along_ab - a_offset_along_ab) / ab_mag
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
                        if a_offset_along_ab <= c_offset_along_ab <= b_offset_along_ab:
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
                        elif a_offset_along_ab <= d_offset_along_ab <= b_offset_along_ab:
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
                            if i_offset_along_ab > b_offset_along_ab:
                                # beyond b
                                if c_offset_along_ab > b_offset_along_ab:
                                    # c is beyond, use d
                                    side_determiner = d_from_pab
                                else:
                                    # d is beyond, use c
                                    side_determiner = c_from_pab
                            else:
                                # under a
                                if c_offset_along_ab < a_offset_along_ab:
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

            res[i, 0] = tab
            res[i, 1] = l0
            res[i, 2] = l1
            res[i, 3] = r0
            res[i, 4] = r1
