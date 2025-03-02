def flatList(lst):
    flist=[]
    for i in lst:
        if isinstance(lst,list):
            flatList(lst)
        else:
            flist.append()
    return flist