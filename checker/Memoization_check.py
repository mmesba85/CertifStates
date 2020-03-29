import json
import sys
import pandas

def main():
    if len(sys.argv) < 2:
        print("Missing Argument: Enter file to process")
        sys.exit(1)
    
    with open(sys.argv[1], encoding='utf-8') as fh:
        data = json.load(fh)
    myDict = {}
    founded = set()
    dictFinal = {}
    #Browsing the Json only once
    for key,value in data.items():
            #Fill memory with what we need
            if value['publicKeyRaw'] not in myDict:
                myDict[value['publicKeyRaw']] = key
            #Collision found
            else:
                #check colision is not because it's the same certificat
                if(data[myDict[value['publicKeyRaw']]] != value):
                  dictFinal[key] = value
                  founded.add(myDict[value['publicKeyRaw']])
                  
    #Now that we have all the colision we need to regroup them by publicKey            
    listIndex = []
    listDict = []    
    for i in founded:
        d = {}
        d[i] = data[i]       
        listDict.append(d)
        listIndex.append(data[i]['publicKeyRaw'])     
    
    for key,value in dictFinal.items():        
        i = listIndex.index(value['publicKeyRaw'])   
        dictTemp = listDict[i]
        dictTemp[key]=value
        listDict[i] = dictTemp
    
    #Manip pas ouf pour avoir le bon output  
    listDf=[]
    for d in listDict:
        res = pandas.DataFrame(d)
        aux = res.transpose()
        listDf.append(aux)
    
    #output  
    with open("collisions.json", 'w') as fo:
        fo.write(json.dumps([df.transpose().to_dict() for df in listDf]))
if __name__ == "__main__":
    main()
