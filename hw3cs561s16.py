import copy
import sys
from collections import OrderedDict
from decimal import Decimal
def EnumerationAsk(X,e,bn):
    ec=copy.deepcopy(e)
    Qx=[]
    ec[X]='+'
    Qx.append(EnumerationAll(bn.keys(),ec))
    ec[X]='-'
    Qx.append(EnumerationAll(bn.keys(),ec))
    return Qx
def EnumerationAll(Vars,e):
    if len(Vars)==0:
        return 1.0
    Y=Vars[0]
    if Y in e:
        a=val(Y,e)*EnumerationAll(Vars[1:],e)
        return a
    else:
        temp=[]
        Yval=['+','-']
        ec=copy.deepcopy(e)
        for y in Yval:
            ec[Y]=y
            temp.append(val(Y,ec)*EnumerationAll(Vars[1:],ec))
        s=sum(temp)
        return float(s)

def val(Y,e):
    if Bayesian[Y]['probability']==5.0:
        l=[]
        for b in Bayesian[Y]['parents']:
            if b not in Bayesian and b not in e:
                return  1
            l.append(e[b])


        key = " ".join(l)
        x = float(Bayesian[Y]['condprob'][key])
    else:
        x=float(Bayesian[Y]['probability'])
    if e[Y]=='+':
        return x
    else:
        return 1-x

def myroundoff(number):
  if '.' in number and len(number[number.index('.'):])>3:
    x=number.index('.')
    y=number[x+2:x+3]
    y1=int(y)
    z=number[x+3:x+4]
    z1=int(z)
    if z1<5:
        return number[:x+3]
    else:
        y1=y1+1
        return number[:x+2]+str(y1)
  else:
      return number

def roundofffloattointeger(number):
    str1=str(number)
    indot=str1.find('.')
    decinum=str1[indot+1:indot+2]
    decinum2=str1[indot+2:indot+3]
    if str1[0]=='-':
        if int(decinum)==5:
            if decinum2==0 or decinum2=='':
                ans=int(number)
            else:
                ans=int(number)-1
        elif int(decinum)<5:
            ans=int(number)
        else:
            ans=int(number)-1
    else:
        if int(decinum)<5:
            ans=int(number)
        else:
            ans=int(number)+1

    return ans

Bayesian={}
def main():
    global noq
    global output_file
    global QueryList
    global Bayesian
    input_file = open(sys.argv[2], 'r')
    output_file=open('output.txt','w')
    lookup='******'
    filelist=[]
    for line in input_file:
        filelist.append(line.rstrip('\n'))
    for num,x in enumerate(filelist,0):
        if x=='******':
            sixstar=num
            break
    ii=0
    QueryList=[]
    while ii<sixstar:
        QueryList.append(filelist[ii])
        ii+=1
    BnList=[]
    BnList=filelist[sixstar:]
    nos=0
    ios=[]
    for num,x in enumerate(BnList,0):
        if x=='******' or x=='***':
            ios.append(num)
            nos+=1
    BB=[]
    while len(ios) >1 :
        BB.append(BnList[ios[0]:ios[1]])
        ios.pop(0)
    BB.append(BnList[ios[0]:])
    jj=0
    while jj<len(BB):
        BB[jj].pop(0)
        jj=jj+1
    jj=0
    BB1=[]
    while jj<len(BB):
        BB1.append(BB[jj][0])
        BB[jj].pop(0)
        jj=jj+1
    jj=0
    BB1DN=[]
    BB1PN=[]
    while jj<len(BB1):
        if BB1[jj].find("|")!=-1:
            BB1DN.append(BB1[jj].split('|')[0][:-1])
            BB1PN.append(BB1[jj].split('|')[1])
        else:
            BB1DN.append(BB1[jj])
            BB1PN.append('chirag')
        jj=jj+1
    jj=0
    Bayesian=OrderedDict()
    DecisionNodes=[]
    while (jj<len(BB1DN)):
        Bayesian[BB1DN[jj]]={}
        Bayesian [BB1DN[jj]]['parents']=[]
        if BB1PN[jj]!='chirag':
            Bayesian[BB1DN[jj]]['parents']=BB1PN[jj].split()
        if len(BB[jj])==1 and BB[jj][0]!='decision':
            Bayesian[BB1DN[jj]]['probability']=float(BB[jj][0])
        if len(BB[jj])==1 and BB[jj][0]=='decision':
            DecisionNodes.append(BB1DN[jj])
            del Bayesian[BB1DN[jj]]
        if len(BB[jj])>1:
            kk=0
            Bayesian[BB1DN[jj]]['probability']=5.0
            Bayesian[BB1DN[jj]]['condprob']={}
            while kk<len(BB[jj]):
                temp=BB[jj][kk].split()
                temp1=temp.pop(0)
                temp2=" ".join(str(x) for x in temp)
                Bayesian[BB1DN[jj]]['condprob'][temp2]=temp1
                kk=kk+1
        jj=jj+1
    for query in QueryList:
        if query[0]=='P':
            q1=query[2:-1].split(' | ')
            p1=q1[0].split(', ')
            pest={}
            for p in p1:
                ind=p.index(' = ')
                pest[p[:ind]]=p[ind+3:]
            evpest={}
            denompest={}
            if ('|') in query:
                p2=q1[1].split(', ')
                p55=p1+p2
                for x in p2:
                    index=x.index(' = ')
                    denompest[x[:index]]=x[index+3:]
                for p in p55:
                    ind1=p.index(' = ')
                    evpest[p[:ind1]]=p[ind1+3:]
                X=pest.keys()[0]
                denom=denompest.keys()[0]
                bb=EnumerationAsk(denom,denompest,Bayesian)
                if denompest[denom]=='+':
                    bbc=bb[0]
                else:
                    bbc=bb[1]
                a=EnumerationAsk(X,evpest,Bayesian)
                if pest[X]=='+':
                    result=a[0]/bbc
                else:
                    result=a[1]/bbc
                if set(denompest.keys()).issubset(set(DecisionNodes)):
                    result=result*bbc
                res=myroundoff(str(result))
                output_file.write(str(res)+'\n')
            else:
                X=pest.keys()[0]
                evpest=copy.deepcopy(pest)
                a=EnumerationAsk(X,evpest,Bayesian)
                if a[0]>1 or a[1]>1:
                    s=sum(a)
                    a[0]=a[0]/s
                    a[1]=a[1]/s
                if pest[X]=='+':
                    result=a[0]
                else:
                    result=a[1]
                res=Decimal(result).quantize(Decimal('.01'))
                output_file.write(str(res)+'\n')
        if query[0]=='E':
            q1=query[3:-1].split(' | ')
            p1=q1[0].split(', ')
            pest={}
            for p in p1:
                ind=p.index(' = ')
                pest[p[:ind]]=p[ind+3:]
            evpest={}
            denominatorevpest={}
            if ('|') in query:
                p2=q1[1].split(', ')
                p1=q1[0].split(', ')
                p55=p1+p2
                for p in p1:
                    ind=p.index(' = ')
                    evpest[p[:ind]]=p[ind+3:]
                for p in p2:
                    ind1=p.index(' = ')
                    evpest[p[:ind1]]=p[ind1+3:]
                    denominatorevpest[p[:ind1]]=p[ind1+3:]
                aaa=EnumerationAsk('utility',evpest,Bayesian)
                aaaa=aaa[0]
                denom=denominatorevpest.keys()[0]
                bbb=EnumerationAsk(denom,evpest,Bayesian)
                if bbb[0]>1 or bbb[1]>1 :
                    bbb[0]=bbb[0]/sum(bbb)
                    bbb[1]=bbb[1]/sum(bbb)
                if denominatorevpest[denom]=='+':
                    bbbb=bbb[0]
                else:
                    bbbb=bbb[1]
                fans=aaaa/bbbb
                if set(denominatorevpest.keys()).issubset(set(DecisionNodes)):
                    fans=aaaa
                fansf=roundofffloattointeger(fans)
                output_file.write(str(fansf)+'\n')
            else:
                evpest=copy.deepcopy(pest)
                X='utility'
                fa=EnumerationAsk(X,evpest,Bayesian)
                result=fa[0]
                xx=evpest.keys()[0]
                fad=EnumerationAsk(xx,evpest,Bayesian)
                if evpest[xx]=='+':
                    r2=fad[0]
                else:
                    r2=fad[1]
                finalwalaresult=result/r2
                finalans=roundofffloattointeger(finalwalaresult)
                output_file.write(str(finalans)+'\n')
        if query[0]=='M':
            V1=['+','-']
            V2=[['+','+'],['+','-'],['-','+'],['-','-']]
            V3=[['+','+','+'],['+','+','-'],['+','-','+'],['-','+','+'],['+','-','-'],['-','-','+'],['-','+','-'],['-','-','-']]
            q1=query[4:-1].split(' | ')
            p1=q1[0].split(', ')
            if '|' in query:
                p2=q1[1].split(', ')
                Mevpest={}
                Cevpest={}
                for p in p2:
                    mind=p.index(' = ')
                    Mevpest[p[0:mind]]=p[mind+3:]
                    Cevpest[p[0:mind]]=p[mind+3:]
                evlist=copy.deepcopy(Mevpest.keys())
            else:
                Cevpest={}
                ccf=1
            if len(p1)==1:
                resultlist=[]
                for s in range(len(V1)):
                    Cevpest[p1[0]]=V1[s]
                    if '|' in query:
                        Mevpest[p1[0]]=V1[s]
                        c1=evlist[0]
                        cc=EnumerationAsk(c1,Mevpest,Bayesian)
                        if cc[0]>1 or cc[1]>1:
                            cc[0]=cc[0]/sum(cc)
                            cc[1]=cc[1]/sum(cc)
                        if(Mevpest[c1]=='+'):
                            ccf=cc[0]
                        else:
                            ccf=cc[1]
                        if set(Mevpest.keys()).issubset(set(DecisionNodes)):
                            ccf=1
                    else:
                        ccf=1
                    temp=EnumerationAsk('utility',Cevpest,Bayesian)
                    tempf=temp[0]/ccf
                    resultlist.append(tempf)
                mans=max(resultlist)
                mansindex=resultlist.index(mans)
                fmans=roundofffloattointeger(mans)
                signs=' '.join(V1[mansindex])
                output_file.write(str(signs+' '+str(fmans))+'\n')
            if len(p1)==2:
                resultlist=[]
                for s in range(len(V2)):
                    Cevpest[p1[0]]=V2[s][0]
                    Cevpest[p1[1]]=V2[s][1]
                    if '|' in query:
                        Mevpest[p1[0]]=V2[s][0]
                        Mevpest[p1[1]]=V2[s][1]
                        c1=evlist[0]
                        cc=EnumerationAsk(c1,Mevpest,Bayesian)
                        if cc[0]>1 or cc[1]>1:
                            cc[0]=cc[0]/sum(cc)
                            cc[1]=cc[1]/sum(cc)
                        if(Mevpest[c1]=='+'):
                            ccf=cc[0]
                        else:
                            ccf=cc[1]
                        if set(Mevpest.keys()).issubset(set(DecisionNodes)):
                            ccf=1
                    else:
                        ccf=1
                    temp=EnumerationAsk('utility',Cevpest,Bayesian)
                    tempf=temp[0]/ccf
                    resultlist.append(tempf)
                mans=max(resultlist)
                mansindex=resultlist.index(mans)
                fmans=roundofffloattointeger(mans)
                signs=' '.join(V2[mansindex])
                output_file.write(str(signs+' '+str(fmans))+'\n')
            if len(p1)==3:
                resultlist=[]
                for s in range(len(V3)):
                    Cevpest[p1[0]]=V3[s][0]
                    Cevpest[p1[1]]=V3[s][1]
                    Cevpest[p1[2]]=V3[s][2]
                    if '|' in query:
                        Mevpest[p1[0]]=V3[s][0]
                        Mevpest[p1[1]]=V3[s][1]
                        Mevpest[p1[2]]=V3[s][2]
                        c1=evlist[0]
                        cc=EnumerationAsk(c1,Mevpest,Bayesian)
                        if cc[0]>1 or cc[1]>1:
                            cc[0]=cc[0]/sum(cc)
                            cc[1]=cc[1]/sum(cc)
                        if(Mevpest[c1]=='+'):
                            ccf=cc[0]
                        else:
                            ccf=cc[1]
                        if set(Mevpest.keys()).issubset(set(DecisionNodes)):
                            ccf=1
                    else:
                        ccf=1
                    temp=EnumerationAsk('utility',Cevpest,Bayesian)
                    tempf=temp[0]/ccf
                    resultlist.append(tempf)
                mans=max(resultlist)
                mansindex=resultlist.index(mans)
                fmans=roundofffloattointeger(mans)
                signs=' '.join(V3[mansindex])
                output_file.write(str(signs+' '+str(fmans))+'\n')
if __name__ == '__main__':
    main()