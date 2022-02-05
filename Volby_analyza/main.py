from preference import simple_list
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

kandidatka=simple_list()
tree=ET.parse("vysledky_kandid.xml")
root=tree.getroot()

def trans_rat(pref_dist,podle="STAN",kresel="all"):
    trans_dist={}
    other_dict={"STAN": "Piráti", "Piráti":"STAN"}
    other=other_dict[podle]
    if kresel=="all":
        all=True
    else:
        all=False
    for kraj in pref_dist.keys():
        if all:
            kresel=len(pref_dist[kraj][podle])
        trans_dist[kraj]={}
        trans_dist[kraj][podle]=sorted(pref_dist[kraj][podle])[::-1]
        
        celkem_podle=sum(trans_dist[kraj][podle])
        rel_dist=[hlasu/celkem_podle for hlasu in trans_dist[kraj][podle]]
        #print("sum r_dist:",sum(rel_dist))
        #input()
        trans_dist[kraj][other]=sorted(pref_dist[kraj][other])[::-1]
        celkem_other=sum(trans_dist[kraj][other])
        #print(sum(trans_dist[kraj][other]))
        for i in range(kresel):
            trans_dist[kraj][other][i]=int(rel_dist[i]*celkem_other )
        
        zbytek=sum(trans_dist[kraj][other][kresel:])
        s=sum(rel_dist[kresel:])
        if zbytek!=0:
            beta=s*celkem_other/zbytek
            for i in range(kresel,len(trans_dist[kraj][other])):
                trans_dist[kraj][other][i]=int(trans_dist[kraj][other][i]*beta)
        #print(sum(trans_dist[kraj][other]))
        #input()
        #print(kraj,"rel:",rel_dist)
        #print(kraj,"NewPir:",trans_dist[kraj][other])

    return trans_dist

def recount(pref_dist,max_mandaty):
    mandaty_dist={}
    mandaty={"Piráti":0,"STAN":0}
    for kraj,pdict in pref_dist.items():
        zisky=[]
        mandaty_dist[kraj]={"Piráti":0,"STAN":0}
        for strana,val in pdict.items():
            sval=sorted(val)[::-1]
            for i in range(max_mandaty[kraj]):
                zisky.append((sval[i],strana))
        zisky=sorted(zisky)[::-1]
        for (val,strana),_ in zip(zisky,range(max_mandaty[kraj])):
            mandaty_dist[kraj][strana]+=1
            mandaty[strana]+=1
        print(kraj,", zisky:",zisky)
        print(kraj,", mandaty: ",mandaty_dist[kraj])
    return mandaty_dist,mandaty
def get_data(root):
    res={}
    for child in root:
        jkraj=child.attrib["NAZ_KRAJ"]
        #print(kraj.tag,kraj.attrib)
        kandidati=child[2]
        #print(kandidati.tag)
        res[jkraj]={}
        for schild in kandidati:
            if schild.attrib["KSTRANA"]=="17":
                res[jkraj][schild.attrib["PORCISLO"]]=schild.attrib["HLASY"]
    return res
res=get_data(root)
vysledky=ET.parse("vysledky.xml").getroot()
wdict={}
#wres=get_data(vysledky,skip=True)
for child in vysledky:
    if "NAZ_KRAJ" in child.attrib:
        kraj=child.attrib["NAZ_KRAJ"]
        wdict[kraj]=[]
        for schild in child:
            #print(schild.attrib)
            if "KSTRANA" in schild.attrib:
                if schild.attrib["KSTRANA"]=="17":
                    for els in schild:
                        #print("pip",els.attrib)
                        if "PORADOVE_CISLO" in els.attrib:
                            wdict[kraj]+=[els.attrib["PORADOVE_CISLO"]]

pref_sums={}#"Starostové a Nezávislí":{},"Pirátská strana":{}}}
pref_dist={}
mand_dist={}
prop_sums={}
strany=["Piráti","STAN"]
for kraj,kdict in res.items():       
    #print(kraj)
    pref_sums[kraj]={}
    pref_dist[kraj]={}
    prop_sums[kraj]={strana:0 for strana in strany}
    mand_dist[kraj]={strana:0 for strana in strany}
    for cislo,hlasy in kdict.items():
        
        strana=kandidatka[kraj][cislo][1]
        #print(cislo,hlasy,kraj,strana)
        hlasy=int(hlasy)
        pref_sums[kraj][strana]=hlasy+pref_sums[kraj].get(strana,0)
        pref_dist[kraj][strana]=[hlasy]+pref_dist[kraj].get(strana,[])
        if cislo in wdict[kraj]:
                mand_dist[kraj][strana]+=1
        else:
            prop_sums[kraj][strana]+=hlasy
celkem={}
prop_celkem={}
count_dist={}
pref_celkem={}

for strana in strany:
    for kraj in pref_sums:
        celkem[strana]=pref_sums[kraj][strana]+celkem.get(strana,0)
        prop_celkem[strana]=prop_sums[kraj][strana]+prop_celkem.get(strana,0)
        pref_celkem[strana]=pref_dist[kraj][strana]+pref_celkem.get(strana,[])
        count_dist[kraj]={}
mand_celkem={kraj:(mand_dist[kraj]["Piráti"]+mand_dist[kraj]["STAN"]) for kraj in mand_dist}
#print(mand_celkem)
old_mand_dist={**mand_dist}
pref_dist=trans_rat(pref_dist,podle="Piráti",kresel=6)
mand_dist,mandaty=recount(pref_dist,mand_celkem)
print("mandaty_dist:",mand_dist)
print("mandaty celkem:",mandaty)

for kraj,kdict in kandidatka.items():
    lim=4
    for ind,(kandidat,data) in enumerate(kdict.items()):
        if ind==lim:
            break
        count_dist[kraj][data[1]]=1+count_dist[kraj].get(data[1],0)
#print("cd:",count_dist)
celkem_count={}
for strana in strany:
    for kraj in pref_sums:
        celkem_count[strana]=count_dist[kraj][strana]+celkem_count.get(strana,0)
#print("celkem count:",celkem_count)

#print("Preference:")
#print(pref_sums)
#print("prop_hlasy",prop_sums)
plist=[]
for kraj,val in prop_sums.items():
    plist.append((kraj,val["Piráti"]/prop_celkem["Piráti"]*100))
    #print(kraj,":",val["Piráti"]/prop_celkem["Piráti"]*100)
plist=sorted(plist,key=lambda x: x[1])
#for tup in plist:
#    print(tup[0]," : ",tup[1])
#exit()

fig,ax=plt.subplots(nrows=1)

x=np.arange(14)
ax.set_title("Počet preferenčních hlasů",fontsize=15)
#ax2.set_title("Počet mandátů")
#print(pref_sums["Středočeský"],prop_sums["Středočeský"])
cols="black","blue"
left, bottom, width, height = [0.6, 0.6, 0.1, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])

for ind,strana in enumerate(strany):
    vals=np.array([np.sort(pref_dist[kraj][strana])[::-1][:6] for kraj in pref_dist])
    bigfish=np.array([np.sort(pref_dist[kraj][strana])[::-1][:6] for kraj in pref_dist])
    bigfish=np.cumsum(vals,axis=1)
    ax.bar(x+0.4*ind,[pref_sums[kraj][strana] for kraj in pref_sums],width=0.4,color=cols[ind],label=strana)
    ax.bar(x+0.4*ind,[prop_sums[kraj][strana] for kraj in pref_sums],width=0.4,fill=False,hatch="\/",edgecolor="red",lw=2,label="Propadlé hlasy" if strana=="STAN" else None)
    ax2.bar([0+ind*0.4],[celkem[strana]],width=0.4,color=cols[ind],label=strana)
    ax2.bar([0+0.4*ind],[prop_celkem[strana]],width=0.4,fill=False,hatch="\/",edgecolor="red",label="Propadlé hlasy" if strana=="STAN" else None)
    ax2.set_xticks([0.2])
    ax2.set_xticklabels(["Celkem"],fontsize=12)
    for kind,kraj in enumerate(pref_sums):
        for mind in range(old_mand_dist[kraj][strana]):
            xpos,ypos=x[kind]+0.4*ind-0.2,bigfish[kind,mind]+prop_sums[kraj][strana]
            ax.plot((xpos,xpos+0.4),(bigfish[kind,mind]+prop_sums[kraj][strana],bigfish[kind,mind]+prop_sums[kraj][strana]),color="red",lw=2,label="Ziskané mandáty" if mind==kind==ind==0 else None)
            ax.text(xpos-0.12+0.53*ind,ypos-1000,mind+1,fontsize=13)
    
    #ax2.bar(x+0.4*ind,[mand_dist[kraj][strana] for kraj in pref_sums],width=0.4,label=strana)
    #labels=["Celkem"]+list(pref_sums.keys())
    labels=list(pref_sums.keys())
    labels[7]="Královéhrad."
    ax.set_xticks(x+0.2)
    ax.set_xticklabels(labels,fontsize=11)
    ax.legend(fontsize=15)

for scind in [0,1]:
    fig,ax=plt.subplots(nrows=1)

    #print("celkem",celkem)
    for ind,strana in enumerate(strany):
        vals=np.array([np.sort(pref_dist[kraj][strana])[::-1][:7] for kraj in pref_dist])
        vals=np.cumsum(vals,axis=1)
        #print(vals)
        
            
        #vals=[np.cumsum(np.sort(pref_dist[kraj][strana]))]
        #print(vals)
        if scind==0:
            scales=[pref_sums[kraj]["STAN"]/pref_sums[kraj]["Piráti"] for kraj in pref_sums]
        else:
            scales=[1  for kraj in pref_sums]
        
        ax.bar(x+0.4*ind,[pref_sums[kraj][strana]*(1 if ind==1 else scale) for scale,kraj in zip(scales,pref_sums)],width=0.4,color=cols[ind],label=strana)
        if scind==1:
            ax.set_title("Rozložení preferenčních hlasů",fontsize=13)
        else:
            ax.set_title("Hypotetické rozložení preferenčních hlasů, pokud by Piráti měli stejně hlasů jako STAN",fontsize=13)
        for i in range(0):#range(7):
            ax.bar(x+0.4*ind,vals.T[i]*(1 if ind==1 else scales),width=0.4,fill=False,edgecolor="red",color=cols[ind],lw=2,label="Preferenční hlasy" if i==ind==0 else None)
        bigfish=np.array([np.cumsum(np.sort(pref_dist[kraj][strana])[::-1]) for kraj in pref_dist])
        
        
        for kind,kraj in enumerate(pref_sums):
            for mind in range(len(bigfish[kind])):
                scale=(1 if ind==1 else scales[kind])
                xpos,ypos=x[kind]+0.4*ind-0.2,bigfish[kind][mind]
                #ax.plot((xpos,xpos+0.4),(ypos*scale,ypos*scale),color="red",lw=2,label="Preferenční hlasy" if mind==kind==ind==0 else None)
                ax.bar([x[kind]+0.4*ind],[ypos*scale],color="red",lw=2,width=0.4,fill=False,edgecolor="red",label="Preferenční hlasy" if mind==kind==ind==0 else None)
                #ax.text(xpos-0.12+0.53*ind,ypos-1000,mind+1,fontsize=13)
        #ax.bar(x+0.4*ind,[prop_sums[kraj][strana] for kraj in pref_sums],width=0.4,fill=False,hatch="/",edgecolor="red",label="Propadlé hlasy" if strana=="STAN" else None)
        #ax.bar(x+0.4*ind,[celkem[strana]]+[pref_sums[kraj][strana] for kraj in pref_sums],width=0.4,color=cols[ind],label=strana)
        #ax.bar(x+0.4*ind,[prop_celkem[strana]]+[prop_sums[kraj][strana] for kraj in pref_sums],width=0.4,fill=False,hatch="/",edgecolor="red",label="Propadlé hlasy" if strana=="STAN" else None)

        #ax2.bar(x+0.4*ind,[mand_dist[kraj][strana] for kraj in pref_sums],width=0.4,label=strana)
        #labels=["Celkem"]+list(pref_sums.keys())
        labels=list(pref_sums.keys())
        labels[7]="Královéhrad."
        ax.set_xticks(x)
        ax.set_xticklabels(labels,fontsize=11)
        ax.legend()

fig,ax=plt.subplots(nrows=1)

#print("celkem",celkem)

for ind,strana in enumerate(strany):
    ax.bar(x+0.4*ind,[mand_dist[kraj][strana] for kraj in pref_sums],width=0.4,label=strana)
    
    labels=list(pref_sums.keys())
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
#for kraj,dists in pref_dist.items():
#    for strana,vals in dists.items():
#        print(np.mean(vals),np.std(vals),np.std(vals)/np.mean(vals))
#print(pref_dist)
plt.show()