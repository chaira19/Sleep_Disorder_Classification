# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 17:00:49 2015

@author: jsk
"""
from sys import exit
import numpy as np
import random

pattern_temp=[]
pattern=[]
correct_class=[]
temp_counter=0
file1 = open("breast_w.txt", "r")
for line in file1.readlines():
    line=line.split(',')
    pattern_temp.append([])
    pattern.append([])    
    for i in range(len(line)-1):
        pattern_temp[temp_counter].append(int(line[i]))
    if line[9][0:6]=='benign':
        pattern_temp[temp_counter].append(0)
    else:
        pattern_temp[temp_counter].append(1)
    temp_counter=temp_counter+1 
        
MAX_DEPTH=50 
max_depth=0
MAX_NUM_PATTERNS=2000
MAX_NUM_INPUTS=130
MAX_NUM_OUTPUTS=30
MAX_STR_LEN=10
max_label=0
npatterns=683
noutputs=2
ninputs=9
n_leafs=0
n_nodes=0
n_split=0
mincard=0
tot_iter=0
error=0
toler=0.000001
wait=40
eta=0.5
n_correct=0
class_1=range(MAX_NUM_PATTERNS)
correct_predicted={}
for i in range(MAX_NUM_PATTERNS):
    correct_predicted[i]=[0,0]
target={}
nodeatdepth=range(MAX_DEPTH)
card=range(MAX_NUM_OUTPUTS)

def bulidtargets():
    global target
    for i in range(npatterns):
        target[i]=range(noutputs)
        for j in range(noutputs):
            if j==correct_class[i]:
                target[i][j]=1.0
            else:
                target[i][j]=0
                
def makenode():
    global max_label
    node={'label':-1,'type':-1,'var':-1,'threshold':-1,'depth':-1,'pattern':range(MAX_NUM_PATTERNS),'weights':{},'children':{},'child_class':[]}
    
    for i in range(MAX_NUM_OUTPUTS):
        node['weights'][i]=[]
        for j in range(MAX_NUM_INPUTS+1):
            node['weights'][i].append(j)
    for i in range(MAX_NUM_PATTERNS):
        node['pattern'][i]=0        
        
    
    node['label']=max_label
    max_label=max_label+1
    node['type']=0
    for i in range(noutputs):
        node['child_class'].append(i)
        node['children'][i]={}
    return node


def freenode(node):
    global max_label
      
    max_label=max_label-1


def classify(node):
    max1=0
    for i in range(npatterns):
        if node['pattern'][i]==0:
            continue
        for j in range(noutputs):
            net=0
            for k in range(ninputs):
                net=net+pattern[i][k]*node['weights'][j][k]
            out=1/(1+np.exp(-1*net))
            if(j==0 or out>max1):
                max1=out
                index=j
        node['pattern'][i]=index+1
        
def splitcase(node):
    first=1
    for i in range(npatterns):
        if node['pattern'][i]==0:
            continue
        if first==1:
            class1=node['pattern'][i]
            first=0
        else:
            if class1!=node['pattern'][i]:
                return 0
    return 1

def init_w(node):
    bar=range(MAX_NUM_INPUTS+1)
    first=1
    cont=0
    for i in range(npatterns):
        if node['pattern'][i]==0:
            continue
        cont=cont+1
        if first==1:
            for j in range(ninputs):
                bar[j]=pattern[i][j]
        else:
            for j in range(ninputs):
                bar[j]=bar[j]+pattern[i][j]
        first=0
    for j in range(ninputs):
        bar[j]=bar[j]/cont
    
    for i in range(noutputs):
        for j in range(1,ninputs):
            node['weights'][i][j]=random.uniform(-1,1)
    for i in range(noutputs):
        sum1=0
        for j in range(1,ninputs):
            sum1=sum1-node['weights'][i][j]*bar[j]
        node['weights'][i][0]=sum1  
        
        
         

def calcard(node):
    global mincard
    global card
    first=1
    for i in range(noutputs):
        card[i]=0
    for p in range(npatterns):
        if node['pattern'][p]>0:
            card[correct_class[p]]=card[correct_class[p]]+1
    for i in range(noutputs):
        if(card[i]!=0 and (card[i]<mincard or first==1)):
            first=0
            mincard=card[i]
       
        
    
def perceptron(node):
    global tot_iter   
    global error
    current={}
    accum={}
    first=1
    counter=0
    init_w(node)
    classify(node)
    calcard(node)
    for i in range(noutputs):
        current[i]=range(ninputs)
        accum[i]=range(ninputs)
        for j in range(ninputs):
            current[i][j]=node['weights'][i][j]
    
    temp_cond=True
    while temp_cond:
        tot_iter=tot_iter+1
        
        tot_patterns=0
        av_delta=0
        for p in range(npatterns):
            if node['pattern'][p]:
                tot_patterns=tot_patterns+1
            else:
                continue
            pw=mincard*1.0/card[correct_class[p]]
            
            for i in range(noutputs):
                net=0
                for j in range(ninputs):
                    net=net+pattern[p][j]*current[i][j]
                out=1/(1+np.exp(-1*net))
                delta=target[p][i]-out
                av_delta=av_delta+abs(delta)
                for j in range(ninputs):
                    if tot_patterns==1:
                        accum[i][j]=pw*eta*delta*pattern[p][j]*out*(1-out)
                    else:
                        accum[i][j]=accum[i][j]+pw*eta*delta*pattern[p][j]*out*(1-out)
        for i in range(noutputs):
            for j in range(ninputs):
                current[i][j]=current[i][j]+accum[i][j]
        av_delta=av_delta/(noutputs*tot_patterns) 
        if (first==1 or (error-av_delta)>toler):
            for i in range(noutputs):
                for j in range(ninputs):
                    node['weights'][i][j]=current[i][j]
            error=av_delta
            counter=0
        counter=counter+1
        first=0
        if counter<=wait:
            temp_cond=True
        else:
            temp_cond=False
    return tot_patterns



def init_children(node):
    first=1
    global class_1
    if node['type']==0:
        for i in range(noutputs):
            child=makenode()
            node['children'][i]=child
            child['depth']=node['depth']+1
            count=0
            for p in range(npatterns):
                if node['pattern'][p]==(i+1):
                    child['pattern'][p]=i+1
                    count=count+1
                else:
                    child['pattern'][p]=0
            if count==0:
                freenode(child)
                child={}
                node['children'][i]={}
                node['child_class'][i]=i
                continue
            first=1
            flag=1
            for p in range(npatterns):
                if child['pattern'][p]==0:
                    continue
                if first==1:
                    class_1=correct_class[p]
                    first=0
                else:
                    if class_1!=correct_class[p]:
                        flag=0
                        break
            if flag==1:
                freenode(child)
                child={}
                node['children'][i]={}
                node['child_class'][i]=class_1
                continue
    else:
        left=makenode()
        right=makenode()
        node['children'][0]=left
        node['children'][1]=right
        left['depth']=node['depth']+1
        right['depth']=node['depth']+1
        for p in range(npatterns):
            if node['pattern'][p]==0:
                left['pattern'][p]=0
                right['pattern'][p]=0
            else:
                if pattern[p][node['var']]<=node['threshold']:
                    left['pattern'][p]=1
                    right['pattern'][p]=0
                else:
                    left['pattern'][p]=0
                    right['pattern'][p]=1
        
        for i in range(2):
            child=node['children'][i]
            first=1
            flag=1
            for p in range(npatterns):
                if child['pattern'][p]==0:
                    continue
                if first==1:
                    class_1=correct_class[p]
                    first=0
                else:
                    if class_1!=correct_class[p]:
                        flag=0
                        break
            if flag==1:
                freenode(child)
                child={}
                node['children'][i]={}
                node['child_class'][i]=class_1
                continue

def choosesplit(node):
    counter=range(MAX_NUM_OUTPUTS)
    bar={}
    for i in range(noutputs):
        counter[i]=0
        bar[i]=range(ninputs)
    for p in range(npatterns):
        if node['pattern'][p]==0:
            continue
        i=correct_class[p]
        if counter[i]==0:
            for j in range(ninputs):
                bar[i][j]=pattern[p][j]
        else:
            for j in range(ninputs):
                bar[i][j]=bar[i][j]+pattern[p][j]
        counter[i]=counter[i]+1
    
    for i in range(noutputs):
        if counter[i]!=0:
            for j in range(ninputs):
                bar[i][j]=bar[i][j]/counter[i]*1.0
    
    if counter[0]>counter[1]:
        max1=counter[0]
        max2=counter[1]
        best1=0
        best2=1
    else:
        max1=counter[1]
        max2=counter[0]
        best1=1
        best2=0
        
    for i in range(2,noutputs):
        if counter[i]>max1:
            max2=max1
            best2=best1
            max1=counter[i]
            best1=i
        else:
            if counter[i]>max2:
                max2=counter[i]
                best2=i
    bestvar=1
    maxd=abs(bar[best1][1]-bar[best2][1])
    for j in range(2,ninputs):
        d=abs(bar[best1][j]-bar[best2][j])
        if d>maxd:
            maxd=d
            bestvar=j
    if maxd==0:
        for j in range(1,ninputs):
            flag1=0
            flag2=0
            for p in range(npatterns):
                if node['pattern'][p]==0:
                    continue
                if pattern[p][j]<=bar[best1][j]:
                    flag1=flag1+1
                else:
                    flag2=flag2+1
                if flag1 and flag2:
                    break
            if flag1 and flag2:
                break
        if flag1==0 or flag2==0:
            return
        else:
            bestvar=j
    node['var']=bestvar
    node['threshold']=(bar[best1][bestvar]+bar[best2][bestvar])/2.0        
            
def nodesatdepth(node):
    global nodeatdepth
    nodeatdepth[node['depth']]=nodeatdepth[node['depth']]+1
    for i in range(noutputs):
        if len(node['children'][i])!=0:
            nodesatdepth(node['children'][i])

def processnode(node):
    global n_leafs
    global max_depth
    global n_nodes
    global n_split
    if len(node)==0:
        n_leafs=n_leafs+1
        return
    if node['depth']>=MAX_DEPTH:
        print "maximum depth reached.......exit\n"
        print "n_leafs=  "+str(n_leafs)+"\n"
        print "max_depth=  "+str(max_depth)+"\n"        
        print "n_nodes=  "+str(n_nodes)+"\n"        
        print "tot_iter=  "+str(tot_iter)+"\n"
        exit(0)
        
    if node['depth']>max_depth:
        max_depth=max_depth+1
        print "max_depth=  "+str(max_depth)+"\n"
    n_nodes=n_nodes+1
    n_pats=perceptron(node)
    classify(node)
    temp_num=splitcase(node)
    if temp_num==0:
        init_children(node)
        for i in range(noutputs):
            processnode(node['children'][i])
    if temp_num==1:
        choosesplit(node)
        node['type']=1
        n_split=n_split+1
        init_children(node)
        processnode(node['children'][0])
        processnode(node['children'][1])
        

            
def find_class(node,p):
    global n_correct
    pos=0
    out=range(MAX_NUM_OUTPUTS)
    
    if node['type']==1:
        if pattern[p][node['var']]<=node['threshold']:
            pos=0
        else:
            pos=1
    else:
        for i in range(noutputs):
            net=0
            for j in range(ninputs):
                net=net+pattern[p][j]*node['weights'][i][j]
            out[i]=1/(1+np.exp(-1.0*net))
        max_1=out[0]
        pos=0
        for i in range(noutputs):
            if out[i]>max_1:
                max_1=out[i]
                pos=i
    if len(node['children'][pos])==0:
        if node['child_class'][pos]==correct_class[p]:
            n_correct=n_correct+1
#        class_1[p]=node['child_class'][pos]
        correct_predicted[p][1]=node['child_class'][pos]
    else:
        find_class(node['children'][pos],p)
                
for itr in range(10):
    random.shuffle(pattern_temp)
    for j in range(temp_counter):
        for k in range(ninputs):
            pattern[j].append(pattern_temp[j][k])
        correct_class.append(pattern_temp[j][ninputs])
    ntrain=int(np.ceil(npatterns)*0.70) 
    ntest=npatterns-ntrain 
                
    bulidtargets()
    root=makenode()
    for i in range(ntrain):
        root['pattern'][i]=1
    root['depth']=1    
    processnode(root)
    nodesatdepth(root)
    print "simualation complete tree formed.......exit\n"
    print "n_leafs=  "+str(n_leafs)+"\n"   
    print "max_depth=  "+str(max_depth)+"\n"        
    print "n_nodes=  "+str(n_nodes)+"\n"        
    print "tot_iter=  "+str(tot_iter)+"\n"  
    for l in range(ntrain,npatterns):
        root['pattern'][l]=1
        find_class(root,l)
    del root
accuracy=n_correct*100/(ntest*10)
print accuracy
        
    
    
    
    
 
 
 
 
 
 
