fig, ax = plt.subplots(figsize=(50, 10))
        ax.plot(dates, aPrec)

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)

        # round to nearest years...
        datemin = np.datetime64(dates[0], 'Y')
        datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
        ax.set_xlim(datemin, datemax)


        # format the coords message box
       
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.format_ydata = time_series
        ax.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

        plt.show()
        sFilename_out =  sWorkspace_data_project + slash \
                + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
                + aSiteName[iSite].zfill(8) + '.png' 
        fig.savefig(sFilename_out)   # save the figure to file
        print( sum(aPrec) )


         years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')


        fig = plt.figure(figsize=(12,9),  dpi=100 )
        fig.set_figheight(9)
        fig.set_figwidth(12)             
        axgr = AxesGrid(fig, 111,
                nrows_ncols=(1,1),
                axes_pad=0.6,    
                label_mode='')  # note the empty label_mode
        for i, ax in enumerate(axgr):                   
            ax.axis('on')   
            ax.xaxis.set_major_locator(years)
            ax.xaxis.set_major_formatter(yearsFmt)
            ax.xaxis.set_minor_locator(months)
            ax.set_aspect(4)
            ax.set_xmargin(0.05)
            ax.set_ymargin(0.10)
            
            ax.set_ylim(0, 80)
            
            ax.set_yticks(np.linspace(0, 100, 5))
            ax.set_xlabel('Anisotropy')
            ax.set_ylabel('WTD (m)')
            ax.set_title('Relationship between Anisotropy and Water Table Depth', loc='center')

            # round to nearest years...
            datemin = np.datetime64(dates[0], 'Y')
            datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
            ax.set_xlim(datemin, datemax)
            ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            ax.format_ydata = time_series

            x1 = dates
            y1 = aPrec
            
            ax.plot( x1, y1, color = 'red', linestyle = '--' , marker="+", markeredgecolor='blue')
        sFilename_jpg = sWorkspace_data_project + slash \
                + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
                + aSiteName[iSite].zfill(8) +    sExtension_jpg 
        plt.savefig(sFilename_jpg) #, bbox_inches = 'tight')
                       
        
        plt.close('all')