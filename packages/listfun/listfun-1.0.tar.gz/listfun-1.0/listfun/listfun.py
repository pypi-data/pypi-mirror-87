class Listoper:
    '''
    Functions to  more easily manage python lists
    
    List of functions:
             listadd (a,b):          Returns list of Elementwise addition of lists "a" and "b"
             listsub (a,b):          Returns list of Elementwise difference of lists "a" and "b"
             listelemwisemult (a,b): Returns list of elementwise products of lists "a" and "b"
             listelemwisediv (a,b):  Returns list of elementwise division of lists "a" and "b" as a[i]/b[i]
             listpow (a,b):          Returns list of a**b for each element in a, or vice versa 
             listsum (a):            Returns the sum of numbers in the list "a"
             listdot (a,b):          Returns the scalar or dot product of elements in lists "a" and "b"
             listmean (a):           Returns the arithmetic mean of the elements in list "a" 
             listabs (a):            Returns list of absolute values of elements in list "a"
             listscal(a,b):          Returns list of the product of scalar "a" with list "b" if "a" is scalar, or other way around.
             listel(a,ind_list):     Returns list of elements in "a" referenced by index list "ind_list"
             listindfind(a,cndn):    Returns list of indices in "a" satisfying condition "cndn" entered as string, e.g. cndn='>3'
             listelfind(a,cndn):     Returns list of elements in "a" satisfying condition "cndn" entered as string, e.g. cndn='>3'
             listnum(a,b):           Returns list of number "a" of length "b"
             listcountel(a):         Returns dictionary with elements as keys and counts as values
     '''
        
    def listadd (a,b):
        c=[x+y for x,y in zip(a,b)]
        return (c)

    def listdiff (a,b):
        c=[x-y for x,y in zip(a,b)]
        return (c)

    def listelemwisemult (a,b):
        c=[x*y for x,y in zip(a,b)]
        return (c)

    def listelemwisediv (a,b):
        c=[x/y for x,y in zip(a,b)]
        return (c)

    def listpow (a,b):
        if type(a)==list:
            c=[x**b for x in a]
        else:
            c=[x**a for x in b]
        return (c)

    def listsum (a):
        c=0
        for x in a:
            c=c+x
        return (c)

    def listdot (a,b):
        c=0
        for x in range(0,len(a)):
            c=c+a[x]*b[x]
        return c

    def listmean (a):
        c=0
        for x in a:
            c=c+x
        c=c/len(a)
        return c

    def listabs(a):
        c=[-x if x < 0 else x for x in a ]
        return c

    def listscale(a,b):
        if type(a)==list and (type(b)==int or type(b)==float):
            c=[b*x for x in a]
            return c
        elif type(b)==list and (type(a)==int or type(a)==float):
            c=[a*x for x in b]
            return c
        else:
            print('One input must be list and another scalar')

    def listel(a,ind_list):
        c=[a[x] for x in ind_list]
        return c

    def listindfind(a,cndn):
        c=[]
        for i in range(0,len(a)):
            if eval('a[i]'+str(cndn)):
                c.append(i)
        return c

    def listelfind(a,cndn):
        c=[x for x in a if eval('x'+str(cndn))]
        return c

    def listnum(a,b):
        c=[]
        for i in range(0,b):
            c.append(a)
        return c

    def listcountel(a):
        a.sort()
        dictcountel={}
        for el in set(a):
            dictcountel[el]=1
        for i in range(len(a)-1):
            if a[i+1]==a[i]:
                el=a[i]
                dictcountel[el]=dictcountel[el]+1
        return dictcountel

