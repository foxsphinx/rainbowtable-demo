#! /usr/bin/env python
#coding=utf-8

import time
import hashlib 
import base64
import threading

#----------------------------------------------------------------------
def md5_twice(i):
    """H function"""
    m2 = hashlib.md5()  
    m2.update("%s" %i)
    i=m2.hexdigest()
    m2 = hashlib.md5()  
    m2.update("%s" %i)
    return m2.hexdigest()    

#----------------------------------------------------------------------
def reduction(s):
    """R function"""
    return md5_base64_first7(s)

#----------------------------------------------------------------------
def chain(start,length):
    """Calculate a chain"""
    s=start
    for i in range(length):
        s=md5_twice(s)
        s=reduction(s)
        #print "'%s'," %s
    return s



#----------------------------------------------------------------------
def preCal(origen,length):
    """Calculate hash values of origen in each position of chain"""
    vals=[]
    for i in range(length):
        origen=reduction(origen)
        vals.append(origen)
        origen=md5_twice(origen)
    return vals

    

#----------------------------------------------------------------------
def generateTable(chain_start,chain_end,chain_len,name):
    """"""
    t1=time.time()
    f=open(name,'w+')
    for i in range(chain_start,chain_end):
        f.writelines("%s\t%s\n" %(i,chain(i,chain_len)))
    f.close()
    t2=time.time()
    print t2-t1
    
#----------------------------------------------------------------------
def check(chain_start,chain_end,val,val_origen,chain_len):
    """check if the value is in the chain"""
    if chain_end==val:
        pre=chain_start
        post=md5_twice(pre)
        for i in range(chain_len):
            if post==val_origen:
                return pre
            else:
                pre=reduction(post)
                post=md5_twice(pre)
        return 1
    else:
        return 1

#----------------------------------------------------------------------
def rainbowCrack(toCrack,table_file,chain_len):
    """main"""
    f=open(table_file,"r")
    chains=f.readlines()
    preCalVal=preCal(toCrack,chain_len)
    for val in preCalVal:
        for chain in chains:
            tmp=chain.split()
            chain_start=tmp[0]
            chain_end=tmp[1]
            
            res=check(chain_start, chain_end, val, toCrack, chain_len)
            if res!=1:
                print res
                return
   
    print 'not found'
    return

#----------------------------------------------------------------------
def md5_first7(s):
    """md5 then taking first 7 characters """
    m2 = hashlib.md5()  
    m2.update("%s" %s)
    s=m2.hexdigest()    
    return s[0:7]     

#----------------------------------------------------------------------
def md5_base64_first7(s):            
    """md5 then using base64 encoding and taking first 7 characters """
    m2 = hashlib.md5()  
    m2.update("%s" %s)  
    s=base64.b64encode(m2.digest())
    return s[0:7]
    
    
    
    
if __name__=='__main__':
    toCrack="7f100197a2a1bb7bddf1e0f902e016f8"
    chain_len=100
    generateTable(1000000,2000000,chain_len)
    
    rainbowCrack(toCrack, "rainbowtable7",chain_len)

    
	#generateTable(23000000,24000000,100,r"rainbowtable23")
	#generateTable(29000000,30000000,100,r"rainbowtable29")
