def line_count(sFilename_in):
    """Count the line number of a text-based file

    Args:
        sFilename_in (string): text filename

    Returns:
        int: line number
    """
    ifs=open(sFilename_in, 'rb') 
    lLine_count=0 
    sLine0=(ifs.readline())#.rstrip()
    sLine= sLine0.decode("utf-8", 'ignore')
    while len(sLine) > 0:
        lLine_count = lLine_count+1
        sLine0=(ifs.readline())
        sLine= sLine0.decode("utf-8", 'ignore')
        
        
    return lLine_count