import numpy as np

import datetime




def swat_convert_data_daily_2_monthly(aData_in,
                                      lJuliDay_end,
                                      lJuliDay_start, iFlag_mean_or_total_in=None,
                                      iFlag_outlier_in=None):

    if iFlag_mean_or_total_in is not None:
        iFlag_mean_or_total = iFlag_mean_or_total_in
    else:
        iFlag_mean_or_total = 0

    if iFlag_outlier_in is not None:
        iFlag_outlier = 1
    else:
        iFlag_outlier = 0

    #caldat, lJuliDay_start, iMonth_start, iDay_start, iYear_start
    #caldat, lJuliDay_end, iMonth_end, iDay_end, iYear_end

    lDt_start = julian.from_jd(lJuliDay_start, fmt='jd')
    iMonth_start = lDt_start.month
    iDay_start = lDt_start.day
    iYear_start = lDt_start.year

    lDt_end = julian.from_jd(lJuliDay_end, fmt='jd')
    iMonth_end = lDt_end.month
    iDay_end = lDt_end.day
    iYear_end = lDt_end.year

    # aData_month = MAKE_ARRAY(12, iYear_end-iYear_start+1, value = !values.f_nan)
    aData_month = np.full((iYear_end - iYear_start + 1, 12),  0.0, dtype=float)

    data_copy = np.array(aData_in)

    for iYear in range(iYear_start, iYear_end + 1):
        for iMonth in range(1, 13):
            # get the total day in this iMonth
            dayinmon = days_in_month(iYear, iMonth)

            dSimulation_start = datetime.datetime(
                iYear, iMonth, 1)  # year, month, day

            start_index = (julian.to_jd(dSimulation_start, fmt='jd'))

            #start_index = julday( iMonth, 1, iYear)
            if iMonth < 12:
                dSimulation_end = datetime.datetime(
                    iYear,  iMonth+1, 1)  # year, month, day
                end_index = (julian.to_jd(dSimulation_end, fmt='jd') - 1)
        #end_index =  julday( iMonth+1, 1, iYear) - 1
            else:
                dSimulation_end = datetime.datetime(
                    iYear, 12, 31)  # year, month, day
                end_index = (julian.to_jd(dSimulation_end, fmt='jd'))
        #end_index =  julday( iMonth, 31, iYear)

            dummy_data = data_copy[int(
                start_index - lJuliDay_start):int(end_index - lJuliDay_start)]

            #dummy_index = WHERE(FINITE(dummy_data) == 1, dummy_count)

            dummy_count = 1
            if dummy_count > 0:
                # ===================================
                # remove outlier
                # ===================================

                if iFlag_mean_or_total == 0:
                    aData_month[iYear-iYear_start,
                                iMonth-1] = np.mean(dummy_data)
                else:
                    aData_month[iYear-iYear_start,
                                iMonth-1] = np.sum(dummy_data)  

    return aData_month


if __name__ == '__main__':

    aData = np.full(1000,  0.0, dtype=float)
    lJuliDay_end = 434213
    lJuliDay_start = 234324
    convert_prms_data_daily_2_monthly(aData,
                                      lJuliDay_end,
                                      lJuliDay_start)
