import json
import sys

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
    listFinal = []    
    for i in founded:
        listT = [dict([(i, data[i])])]        
        listFinal.append(listT)
        listIndex.append(data[i]['publicKeyRaw'])     
        
    for key,value in dictFinal.items():
        dictT = dict([(key, value)])
        i = listIndex.index(value['publicKeyRaw'])                
        listFinal[i].append(dictT)
    #output
    with open("collisions.json", 'w') as fo:
        fo.write(json.dumps(listFinal))
    
if __name__ == "__main__":
    main()
