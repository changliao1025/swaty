fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    aDischarge_monthly.shape = (12* nyear)
    ax.plot(dates, aDischarge_monthly)
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    ax.set_xlabel('Time')
    ax.set_ylabel('Stream discharge (units: cubic meter)')
    
    # round to nearest years...
    #datemin = np.datetime64(dates[0], 'Y')
    #datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
    #ax.set_ylim(0.0, max(aDischarge_simulation) * 0.3 )
    #ax.set_xlim(datemin, datemax)
    
    ax.yaxis.set_major_formatter(formatter)
    
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    #ax.fmt_ydata  = time_series
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    
    #plt.show()
    sFilename_out = sWorkspace_simulation + slash + 'discharge_monthly.png'
    fig.savefig(sFilename_out)   # save the figure to file