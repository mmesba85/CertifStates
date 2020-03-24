import json

def main():
    f = open('sample.json')
    data = json.load(f)
    myDict = {}
    founded = set()
    dictFinal = {}
    for key,value in data.items():
            if value['publicKeyRaw'] not in myDict:
                myDict[value['publicKeyRaw']] = key
            else:
                dictFinal[key] = value
                founded.add(myDict[value['publicKeyRaw']])
    
    for i in founded:
        dictFinal[i] = data[i]
    
    print(dictFinal)
        
if __name__ == "__main__":
    main()