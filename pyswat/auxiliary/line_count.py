def line_count(fname):
    ifs=open(fname, 'rb') 
    i=0 
    sLine0=(ifs.readline())#.rstrip()
    sLine= sLine0.decode("utf-8", 'ignore')
    while len(sLine) > 0:
        i = i+1
        sLine0=(ifs.readline())
        sLine= sLine0.decode("utf-8", 'ignore')
        
        
    return i