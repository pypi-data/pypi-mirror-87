#checks if a given Tuple is a Tandem array of a sequence
def is_tandem_array(sequence, i, repeat_type, k):
    
    #print(sequence, i, repeat_type, k)
    
    if k < 2:
        return False

    for j in range(k*len(repeat_type)):
        
        if sequence[(i-1)+j] != repeat_type[j % len(repeat_type)]:
            #print(sequence[(i-1)+j] , repeat_type[j % len(repeat_type)])
            return False
    
    return True


#helper function cleans tandem arrays right of the maximal tandem array
def remove_none_max_right(tandem_arrays):
    to_del = set([])

    for i in range(len(tandem_arrays)):
        for j in range(i+1,len(tandem_arrays)):

            if tandem_arrays[i][1] == tandem_arrays[j][1] and tandem_arrays[i][0] == tandem_arrays[j][0]:
                if tandem_arrays[i][2] > tandem_arrays[j][2]:
                    to_del.add(j)
                else:
                    to_del.add(i)

    for i in reversed(sorted(list(to_del))):
        del tandem_arrays[i]
    return tandem_arrays


#helper function cleans tandem arrays left of the maximal tandem array
def remove_none_max_left(tandem_arrays):
    to_del = set([])

    for i in range(len(tandem_arrays)):
        for j in range(i+1,len(tandem_arrays)):

            if tandem_arrays[i][1] == tandem_arrays[j][1]:
                steps = abs(tandem_arrays[i][2] - tandem_arrays[j][2])
                if tandem_arrays[i][0] + steps * len(tandem_arrays[i][1]):
                    to_del.add(j)

    for i in reversed(sorted(list(to_del))):
        del tandem_arrays[i]
    return tandem_arrays


#cleans a list of tandem arrays of non maximal tandem arrays
def maximize_tandem_array(tandem_arrays):
    tandem_arrays = remove_none_max_right(tandem_arrays)
    tandem_arrays = remove_none_max_left(tandem_arrays)
    return tandem_arrays
    
    
    
def findTandemArrays(log):

    tandem_arrays = []
    activity_classifier='concept:name'
    # print(activity_classifier)
    for trace in log:

        sequence = [event[activity_classifier] for event in trace]
        maxlen = int(len(sequence)/2)


        #itterate over all posible tandem repeat types
        for repeat_type_len in range(1,maxlen+1):
            for i in range(len(sequence)-2*repeat_type_len+1):

                repeat_type = [event[activity_classifier] for event in trace[i:i+repeat_type_len]]
                maxloop = int((len(sequence)-i)/len(repeat_type))

                for k in range(2, maxloop+1):

                    if is_tandem_array(sequence, i+1, repeat_type, k):
                        print("ta array = ", repeat_type)
                        tandem_arrays.append((i+1, repeat_type, k))
                    else:
                        break

    return maximize_tandem_array(tandem_arrays)
    
    
    
def findPrimitiveTandemArrays(log):
    tandem_arrays = findTandemArrays(log)
    primitives = []

    for array in tandem_arrays:
                    
        if len(array[1]) == 1:
            print("ta array primitve= ", array)
            primitives.append(array)
            continue
        
        for i in range(1,len(array[1])):
            
            loops = len(array[1])/i
             
            if int(loops) < loops:
                continue
                
            if not loops*i == len(array):
                continue
            
            if not is_tandem_array(array[1], 1, array[1][:i], int(len(array[1])/i)):
                print("ta array primitve= ", array)
                primitives.append(array)
    
    return primitives