inputveclen = 420
num_logs = 250
nnlayerlen = 100
outputveclen = 2
lengesture = 20
num_features = 7

usefulframes_forgesture = [0]*lengesture
usefulwtrangeframes_forgesture = [0]*lengesture
steepfallidxs = [0]*lengesture
steepriseidxs = [0]*lengesture
numdetectptspeak_idx = [0]*lengesture


def findmin(a, b):
    if a < b:
        return a
    else:
        return b


def findmax(a, b):
    if a > b:
        return a
    else:
        return b


def getmaxidx_inarray(left_idx, right_idx, input):
    max_element = input[left_idx]
    maxelement_idx = left_idx
    for i in range(left_idx, right_idx + 1):
        if max_element < input[i]:
            max_element = input[i]
            maxelement_idx = i
    return maxelement_idx


def getminidx_inarray(left_idx, right_idx, input):
    min_element = input[left_idx]
    minelement_idx = left_idx
    for i in range(left_idx, right_idx + 1):
        if min_element > input[i]:
            min_element = input[i]
            minelement_idx = i

    return minelement_idx


def swipe_prediction(wt_range, wt_doppler, range_disp, vel_disp, instenergy, numdetectpts, angle):
    # Initializing Variables
    if (1):
        len_forsteepfall = 0
        len_forsteeprise = 0
        len_squaresdetected = 0
        firstsquareriseidx = -1
        firstsquarefallidx = -1
        secondsquareriseidx = -1
        secondsquarefallidx = -1
        doppler_crosssearchrange = 2
        count_Num_zerodopplerinmid = 0
        searchrange_forminmaxdoppler = 3
        count_posangle_atgesture = 0
        count_negangle_atgesture = 0
        searchrange_foranglerisefall = 3
        idx_initialanglecross = -1
        idx_finalanglecross = -1
        anglefall_leftidx = 0
        anglefall_rightidx = 0
        anglerise_leftidx = 0
        anglerise_rightidx = 0
        limit_lengesture = 20
        diff_inlengthforpartsofgesture = 5
        Thresh_changeinanglemag_anglecross = 5
        Thresh_foranglemag_atdoppcross = -5
        veldispminshift_numdetectpeak = 2
        wtrangeminshift_numdetectpeak = 2
        maxelement_idx = 0
        temp_val = 0
        falsedetection = 0
        idx_firstrangemin = 2
        idx_secondrangemin = 2
        idx_firstveldispmin = 2
        idx_secondveldispmin = 2
        angle_crosssearchrange = 2
        check_zerodoppleratnumdetectptspeaks = 1
        validate_initialcross = 0
        validate_finalcross = 0
        get_firstchangesign = 0
        findtwosquareframes_fornumdetectpts = 1
        gettwosquares = 1
        check_framesbetweensquares = 0
        checks_forweightedrange = 1
        check_rangeminwithnumdetectptsmax = 1
        checks_forveldisp = 1
        count_Num_wtrangeptswithnumdetectpts = 0
        usefulveldispframes_forgesture = [0]*lengesture
        check_veldispminwithnumdetectptsmax = 1
        checks_angleatnumdetectptspeaks = 1
        check_countposneganglesatgesture = 0
        check_angledirectionatdopplercrossing = 0
        check_anglemagatdopplercrossing = 0
        check_changeinangledirection = 1
        checkanglemag_duringcross = 0
        check_maxmindopplerposition = 1
        checklimit_fordifferentgestureparts = 1
        check_gesturelength = 1
        check_countofzerodopplerinmid = 0
        count_Num_veldispptswithnumdetectpts = 1
        checklimit_fornmaxmindopplerrise = 1
        usethresh_forwtrangenumdetectptscross = 0
        usethresh_forveldispnumdetectptscross = 0
        lowerthresh_maxmindopplerjump = 0.2
        max_element = 0
        numdetectpts_thresh = 0
        anglediff_posnegpts = 0
        upperthresh_forwtrange = 0.3
        upperthresh_forveldisp = 1.15
        usenumdetect_asbasis = 1
        find_gestureoccuringframes = 1
        maxelement_idx = 0
    if find_gestureoccuringframes:
        if usenumdetect_asbasis:
            maxelement_idx = getmaxidx_inarray(0, lengesture - 1, numdetectpts)
            max_element = numdetectpts[maxelement_idx]
            numdetectpts_thresh = 0.6 * max_element
            for i in range(lengesture):
                usefulframes_forgesture[i] = 0
                if numdetectpts[i] > numdetectpts_thresh:
                    usefulframes_forgesture[i] = 1
        if findtwosquareframes_fornumdetectpts:
            if gettwosquares:
                for i in range(lengesture - 1):
                    if (not usefulframes_forgesture[i]) & usefulframes_forgesture[i + 1]:
                        steepriseidxs[len_forsteeprise] = i + 1
                        len_forsteeprise += 1
                    if usefulframes_forgesture[i] & (not usefulframes_forgesture[i + 1]):
                        steepfallidxs[len_forsteepfall] = i
                        len_forsteepfall += 1
                for i in range(findmin(len_forsteepfall, len_forsteeprise)):
                    if steepfallidxs[i] >= steepriseidxs[i]:
                        numdetectptspeak_idx[len_squaresdetected] = getmaxidx_inarray(steepriseidxs[i],
                                                                                      steepfallidxs[i], numdetectpts)
                        len_squaresdetected += 1
                if len_squaresdetected >= 1:
                    return 1
                    firstmax_numdetectptsidx = 0
                    secondmax_numdetectptsidx = 0
                    for i in range(len_squaresdetected):
                        temp_val = numdetectptspeak_idx[i]
                        if numdetectpts[secondmax_numdetectptsidx] < numdetectpts[temp_val]:
                            if numdetectpts[firstmax_numdetectptsidx] < numdetectpts[temp_val]:
                                secondmax_numdetectptsidx = firstmax_numdetectptsidx
                                firstmax_numdetectptsidx = temp_val
                            else:
                                secondmax_numdetectptsidx = temp_val
                else:
                    return 0
            else:
                return 0
#To elminate false detections, incorporate this code
    #                 firstsquarenumdetectpts_peakidx = findmin(secondmax_numdetectptsidx, firstmax_numdetectptsidx)
    #                 secondsquarenumdetectpts_peakidx = findmax(secondmax_numdetectptsidx, firstmax_numdetectptsidx)
    #                 for i in range(findmin(len_forsteepfall, len_forsteeprise)):
    #                     if (steepfallidxs[i] >= firstsquarenumdetectpts_peakidx & steepriseidxs[i] <= firstsquarenumdetectpts_peakidx):
    #                         firstsquareriseidx = steepriseidxs[i]
    #                         firstsquarefallidx = steepfallidxs[i]
    #                     if (steepfallidxs[i] >= secondsquarenumdetectpts_peakidx & steepriseidxs[
    #                         i] <= secondsquarenumdetectpts_peakidx):
    #                         secondsquareriseidx = steepriseidxs[i]
    #                         secondsquarefallidx = steepfallidxs[i]
    #                 if (
    #                         firstsquarefallidx == -1 | firstsquareriseidx == -1 | secondsquarefallidx == -1 | secondsquareriseidx == -1):
    #                     print("false detection due to invalid squares")
    #                     falsedetection = 1
    #                     return not falsedetection
    #                 if (
    #                         firstsquarefallidx > secondsquareriseidx | firstsquareriseidx > firstsquarefallidx | secondsquareriseidx > secondsquarefallidx):
    #                     print("false detection due to invalid squares")
    #                     falsedetection = 1
    #                     return not falsedetection
    #             else:
    #                 print("false detection due to less squares")
    #                 falsedetection = 1
    #                 return not falsedetection
    #             if check_zerodoppleratnumdetectptspeaks:
    #                 for i in range(1, doppler_crosssearchrange + 1):
    #                     if not validate_initialcross:
    #                         leftidx_tostart = findmax(0, firstsquarenumdetectpts_peakidx - i)
    #                         rightidx_tostart = findmin(lengesture - 1, firstsquarenumdetectpts_peakidx + i)
    #                         if ((wt_doppler[leftidx_tostart] * wt_doppler[firstsquarenumdetectpts_peakidx]) > 0 & (
    #                                 wt_doppler[rightidx_tostart] * wt_doppler[firstsquarenumdetectpts_peakidx]) > 0):
    #                             validate_initialcross = 0
    #                         else:
    #                             validate_initialcross = 1
    #                     if not validate_finalcross:
    #                         leftidx_tostart = findmax(0, secondsquarenumdetectpts_peakidx - i)
    #                         rightidx_tostart = findmin(lengesture - 1, secondsquarenumdetectpts_peakidx + i)
    #                         if ((wt_doppler[leftidx_tostart] * wt_doppler[secondsquarenumdetectpts_peakidx]) > 0 & (
    #                                 wt_doppler[rightidx_tostart] * wt_doppler[secondsquarenumdetectpts_peakidx]) > 0):
    #                             validate_finalcross = 0
    #                         else:
    #                             validate_finalcross = 1
    #                 if (not validate_initialcross) | (not validate_finalcross):
    #                     print("false detection due to no zero doppler crossing beside numdetectpts peak")
    #                     falsedetection = 1
    #                     return not falsedetection
    #             if check_framesbetweensquares:
    #                 if (secondsquareriseidx - firstsquarefallidx) <= 2:
    #                     print("false detection due to less frames b/w two squares")
    #                     falsedetection = 1
    #                     return not falsedetection
    #             for i in range(firstsquarefallidx, secondsquareriseidx + 1):
    #                 if wt_doppler[i] >= 0 & wt_doppler[i + 1] <= 0:
    #                     idx_forzerodopplerinmid = i
    #                     count_Num_zerodopplerinmid += 1
    #             if check_countofzerodopplerinmid:
    #                 if count_Num_zerodopplerinmid != 1:
    #                     print("false detection due to inappropriate no. of zeroes in middle")
    #                     falsedetection = 1
    #                     return not falsedetection
    #             if count_Num_zerodopplerinmid >= 1:
    #                 leftidx_formaxmindopplersearch = findmax(0, firstsquareriseidx - searchrange_forminmaxdoppler)
    #                 rightidx_formaxmindopplersearch = findmin(lengesture - 1,
    #                                                           secondsquarefallidx + searchrange_forminmaxdoppler)
    #                 idx_forfirstdopplermax = getmaxidx_inarray(leftidx_formaxmindopplersearch, idx_forzerodopplerinmid,
    #                                                            wt_doppler)
    #                 idx_forfirstdopplermin = getminidx_inarray(leftidx_formaxmindopplersearch, idx_forzerodopplerinmid,
    #                                                            wt_doppler)
    #                 idx_forseconddopplermax = getmaxidx_inarray(idx_forzerodopplerinmid + 1,
    #                                                             rightidx_formaxmindopplersearch, wt_doppler)
    #                 idx_forseconddopplermin = getminidx_inarray(idx_forzerodopplerinmid + 1,
    #                                                             rightidx_formaxmindopplersearch, wt_doppler)
    #                 if check_maxmindopplerposition:
    #                     if ((idx_forfirstdopplermax - idx_forfirstdopplermin) <= 0 | (
    #                             idx_forseconddopplermax - idx_forseconddopplermin) <= 0):
    #                         print("false detection due to wrong position of max and min doppler")
    #                         falsedetection = 1
    #                         return not falsedetection
    #                 if checks_forweightedrange:
    #                     idx_firstrangemin = getminidx_inarray(idx_forfirstdopplermin, idx_forfirstdopplermax, wt_range)
    #                     idx_secondrangemin = getminidx_inarray(idx_forseconddopplermin, idx_forseconddopplermax,
    #                                                            wt_range)
    #                     if usethresh_forwtrangenumdetectptscross:
    #                         for i in range(lengesture):
    #                             usefulwtrangeframes_forgesture[i] = 0
    #                             if wt_range[i] < upperthresh_forwtrange:
    #                                 usefulwtrangeframes_forgesture[i] = 1
    #                         for i in range(firstsquareriseidx, firstsquarefallidx + 1):
    #                             if usefulwtrangeframes_forgesture[i]:
    #                                 count_Num_wtrangeptswithnumdetectpts = 1
    #                         if not count_Num_wtrangeptswithnumdetectpts:
    #                             print("false detection because of no wt range points in gesture region")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                         count_Num_wtrangeptswithnumdetectpts = 0
    #                         for i in range(secondsquareriseidx, secondsquarefallidx + 1):
    #                             if usefulwtrangeframes_forgesture[i]:
    #                                 count_Num_wtrangeptswithnumdetectpts = 1
    #                         if not count_Num_wtrangeptswithnumdetectpts:
    #                             print("false detection because of no wt range points in gesture region");
    #                             falsedetection = 1
    #                             return not falsedetection
    #                     if check_rangeminwithnumdetectptsmax:
    #                         if ((abs(
    #                                 firstmax_numdetectptsidx - idx_firstrangemin) > wtrangeminshift_numdetectpeak & abs(
    #                             firstmax_numdetectptsidx - idx_secondrangemin) > wtrangeminshift_numdetectpeak)
    #                                 | (abs(
    #                                     secondmax_numdetectptsidx - idx_firstrangemin) > wtrangeminshift_numdetectpeak & abs(
    #                                     secondmax_numdetectptsidx - idx_secondrangemin) > wtrangeminshift_numdetectpeak)):
    #                             print("false detection due to more difference b/w wt range min and numdetectpts max")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                 if checks_forveldisp:
    #                     idx_firstveldispmin = getminidx_inarray(idx_forfirstdopplermin, idx_forfirstdopplermax,
    #                                                             vel_disp)
    #                     idx_secondveldispmin = getminidx_inarray(idx_forseconddopplermin, idx_forseconddopplermax,
    #                                                              vel_disp)
    #                     if usethresh_forveldispnumdetectptscross:
    #                         for i in range(lengesture):
    #                             usefulveldispframes_forgesture[i] = 0
    #                             if vel_disp[i] < upperthresh_forveldisp:
    #                                 usefulveldispframes_forgesture[i] = 1
    #                         for i in range(firstsquareriseidx, firstsquarefallidx + 1):
    #                             if usefulveldispframes_forgesture[i]:
    #                                 count_Num_veldispptswithnumdetectpts = 1
    #                         if not count_Num_veldispptswithnumdetectpts:
    #                             print("false detection because of no vel disp points in gesture region1")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                         count_Num_veldispptswithnumdetectpts = 0
    #                         for i in range(secondsquareriseidx, secondsquarefallidx + 1):
    #                             if usefulveldispframes_forgesture[i]:
    #                                 count_Num_veldispptswithnumdetectpts = 1
    #                         if not count_Num_veldispptswithnumdetectpts:
    #                             print("false detection because of no vel disp points in gesture region2")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                     if check_veldispminwithnumdetectptsmax:
    #                         if ((abs(
    #                                 firstmax_numdetectptsidx - idx_firstveldispmin) > veldispminshift_numdetectpeak & abs(
    #                             firstmax_numdetectptsidx - idx_secondveldispmin) > veldispminshift_numdetectpeak)
    #                                 | (abs(
    #                                     secondmax_numdetectptsidx - idx_firstveldispmin) > veldispminshift_numdetectpeak & abs(
    #                                     secondmax_numdetectptsidx - idx_secondveldispmin) > veldispminshift_numdetectpeak)):
    #                             print("false detection due to more difference b/w vel disp min and numdetectpts max")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                 if checks_angleatnumdetectptspeaks:
    #                     validate_finalcross = 0
    #                     validate_initialcross = 0
    #                     for i in range(1, angle_crosssearchrange + 1):
    #                         if not validate_initialcross:
    #                             leftidx_tostart = findmax(0, firstsquarenumdetectpts_peakidx - i)
    #                             rightidx_tostart = findmin(lengesture - 1, firstsquarenumdetectpts_peakidx + i)
    #                             if angle[leftidx_tostart] * angle[firstsquarenumdetectpts_peakidx] > 0 & angle[
    #                                 rightidx_tostart] * \
    #                                     angle[firstsquarenumdetectpts_peakidx] > 0:
    #                                 validate_initialcross = 0
    #                             else:
    #                                 validate_initialcross = 1
    #                         if not validate_finalcross:
    #                             leftidx_tostart = findmax(0, secondsquarenumdetectpts_peakidx - i)
    #                             rightidx_tostart = findmin(lengesture - 1, secondsquarenumdetectpts_peakidx + i)
    #                             if angle[leftidx_tostart] * angle[secondsquarenumdetectpts_peakidx] > 0 & angle[
    #                                 rightidx_tostart] * \
    #                                     angle[secondsquarenumdetectpts_peakidx] > 0:
    #                                 validate_finalcross = 0
    #                             else:
    #                                 validate_finalcross = 1
    #                     if (not validate_initialcross) | (not validate_finalcross):
    #                         print("false detection due to no zero angle crossing beside numdetectpts peak")
    #                         falsedetection = 1
    #                         return not falsedetection
    #                     if check_countposneganglesatgesture:
    #                         for i in range(idx_forfirstdopplermax, idx_forseconddopplermin + 1):
    #                             if angle[i] > 0:
    #                                 count_posangle_atgesture += 1
    #                             if angle[i] < 0:
    #                                 count_negangle_atgesture += 1
    #                         if ((count_negangle_atgesture - count_posangle_atgesture) < (
    #                                 anglediff_posnegpts * (count_posangle_atgesture + count_negangle_atgesture))):
    #                             print("false detection due to less negative pts in angle data")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                     if check_angledirectionatdopplercrossing:
    #                         if angle[idx_forzerodopplerinmid] > 0 & angle[idx_forzerodopplerinmid + 1] > 0:
    #                             print("false detection due to non negative angle at zero crossing of doppler")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                     if check_anglemagatdopplercrossing:
    #                         if angle[idx_forzerodopplerinmid] > Thresh_foranglemag_atdoppcross & angle[idx_forzerodopplerinmid + 1] > Thresh_foranglemag_atdoppcross:
    #                             print("false detection due to big value of angle at zero doppler crossing")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                     if check_changeinangledirection:
    #                         for i in range(idx_forfirstdopplermin, idx_forfirstdopplermax + 1):
    #                             if not get_firstchangesign & wt_doppler[i] >= 0:
    #                                 idx_initialzerodoppcross = i
    #                                 get_firstchangesign = 1
    #                         get_firstchangesign = 0;
    #                         for i in range(idx_forseconddopplermin, idx_forseconddopplermax + 1):
    #                             if not get_firstchangesign & wt_doppler[i] >= 0:
    #                                 idx_finalzerodoppcross = i
    #                                 get_firstchangesign = 1
    #                         anglefall_leftidx = findmax(0, idx_initialzerodoppcross - searchrange_foranglerisefall)
    #                         anglefall_rightidx = findmin(lengesture - 1,
    #                                                      idx_initialzerodoppcross + searchrange_foranglerisefall - 1)
    #                         for i in range(anglefall_leftidx, anglefall_rightidx):
    #                             if angle[i] >= 0 & angle[i + 1] <= 0:
    #                                 idx_initialanglecross = i
    #                         anglerise_leftidx = findmax(0, idx_finalzerodoppcross - searchrange_foranglerisefall)
    #                         anglerise_rightidx = findmin(lengesture - 1,
    #                                                      idx_finalzerodoppcross + searchrange_foranglerisefall - 1)
    #                         for i in range(anglerise_leftidx, anglerise_rightidx):
    #                             if angle[i] <= 0 & angle[i + 1] >= 0:
    #                                 idx_finalanglecross = i
    #                         if idx_initialanglecross == -1 | idx_finalanglecross == -1:
    #                             print("false detection due to wrong angle direction")
    #                             falsedetection = 1
    #                             return not falsedetection
    #                         elif checkanglemag_duringcross:
    #                             if ((angle[idx_initialanglecross] - angle[
    #                                 idx_initialanglecross + 1]) < Thresh_changeinanglemag_anglecross
    #                                     | (angle[idx_finalanglecross] - angle[
    #                                         idx_finalanglecross + 1]) < Thresh_changeinanglemag_anglecross):
    #                                 print("false detection due to less magnitude jump in angle value at crossing")
    #                                 falsedetection = 1
    #                                 return not falsedetection
    #                 if checklimit_fornmaxmindopplerrise:
    #                     if (wt_doppler[idx_forfirstdopplermax] - wt_doppler[
    #                         idx_forfirstdopplermin]) < lowerthresh_maxmindopplerjump:
    #                         print("false detection due to less max and min doppler value difference");
    #                         falsedetection = 1
    #                         return not falsedetection
    #                     if (wt_doppler[idx_forseconddopplermax] - wt_doppler[
    #                         idx_forseconddopplermin]) < lowerthresh_maxmindopplerjump:
    #                         print("false detection due to less max and min doppler value difference")
    #                         falsedetection = 1
    #                         return (not falsedetection)
    #                     if (wt_doppler[idx_forfirstdopplermax] - wt_doppler[
    #                         idx_forseconddopplermin]) < lowerthresh_maxmindopplerjump:
    #                         print("false detection due to less max and min doppler value difference")
    #                         falsedetection = 1
    #                         return not falsedetection
    #                 if checklimit_fordifferentgestureparts:
    #                     if abs((idx_forfirstdopplermax - idx_forfirstdopplermin) - (
    #                             idx_forseconddopplermax - idx_forseconddopplermin)) > diff_inlengthforpartsofgesture:
    #                         print("false detection due to large difference in parts of gesture")
    #                         falsedetection = 1
    #                         return not falsedetection
    #                     if abs((idx_forseconddopplermin - idx_forfirstdopplermax) - (
    #                             idx_forfirstdopplermax - idx_forfirstdopplermin)) > (
    #                             2 * diff_inlengthforpartsofgesture):
    #                         print("false detection due to large difference in parts of gesture")
    #                         falsedetection = 1
    #                         return not falsedetection
    #                 if check_gesturelength:
    #                     if (idx_forseconddopplermax - idx_forfirstdopplermax) > limit_lengesture:
    #                         print("false detection due to large gesture")
    #                         falsedetection = 1
    #                         return not falsedetection
    #             else:
    #                 print("false detection due to zero doppler crossings in middle")
    #                 falsedetection = 1
    #                 return not falsedetection
    # return not falsedetection
