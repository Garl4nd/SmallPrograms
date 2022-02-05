import re
import numpy as np
def get_candidates():
    with open("preference.txt",encoding="utf-8") as file:
        content=file.readlines()

    jmena,strany,kraje,hlasy=[content[4+i::4] for i in range(4)]
    zaznamy=[[strana,hlas] for strana,hlas in zip(strany,hlasy)]

    hlasdict={}
    for strana,hlas in zaznamy:
        hlasdict[strana]=int(hlas)+hlasdict.get(strana,0)

   # print(hlasdict)
    with open("Kandidatky.txt",encoding="utf-8") as content:
        lines=[line for line in content.readlines() if line!="\n"]


    #print(lines,len(lines))
    kraj=""
    i=0
    kandidati={}
    while i<len(lines):
        line=lines[i].strip()
        if line.startswith("Kraj"):
            kraj=lines[i].strip("Kraj").strip()
            kandidati[kraj]={}
            num=0
        
            last="Kraj"
        else:
            
            if last in ["Kraj","strana"]:
                jmeno=line
                if len(jmeno.split())>=2 and not ".jpg" in jmeno and not jmeno[0].isdigit():
                    
                    #for title in ["Mgr","et","Bc","Ing","PhD","CSc","doc","Judr","Phdr","Pharmdr","arch","MUDr"]:
                    #    jmeno=jmeno.replace(title+". ","")
                    words=jmeno.split()
                    jmeno=" ".join(word for word in words if not ("." in word or word in ["et"]))
                
                    num+=1
                    kandidati[kraj][num]=[jmeno]
                    last="jmeno"
            elif last=="jmeno":
                #print(line)
                if line in ["Pirátská strana","Starostové a nezávislí"]:
                    #print(line)
                    kandidati[kraj][num]+=[line]
                    
                    last="strana"
            
                    
        i+=1

        
    return kandidati

def simple_list():
    fields=np.loadtxt("Jmensez.txt",encoding="utf-8",dtype=str,delimiter="\t")
    print(fields)
    kdict={}
    for field in fields:
        if field[1] not in kdict:
            kdict[field[1]]={}
        kdict[field[1]][field[2]]=[field[3],field[5]]
    return(kdict)