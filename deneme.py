import math 

def convertInteger(binaryArray):
    lnght = len(binaryArray)
    if lnght==1:
        return int(binaryArray[0])
    elif lnght>1:
        num = 0
        for i in range(lnght):
            num += math.pow(2,i) * binaryArray[i] 
        return int(num)

def convertBinary(intNum):
    binaryArr = []
    while(intNum):
        binaryArr.append(intNum %2 )
        intNum = int(intNum / 2) 
    for i in range(16-len(binaryArr)):
        binaryArr.append(0)
    return binaryArr

def convertBinaryArraySize(intNum , Size):
    return convertBinary(intNum)[0:Size]



print(convertBinaryArraySize(8,10))