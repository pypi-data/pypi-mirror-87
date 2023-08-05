import copy as copyLib
    

def copy(val):
    """crates a copy of a list or dict

    this is a fix for the problem that when coping a list it of a list it dosnt copy second dim list

    a = [[1,2],[3,4]]
    b = copy.copy(a)

    a[0] = 10
    in this case b is [[1,2],[3,4]]

    but if we
    a[1][0] = 10
    b is [[1,2],[10,4]] but if we replace copy.copy with this function b would be [[1,2],[3,4]]

    parmeters:
    ------------
    val: pyobject
         what we want to copy

    outputs:
    copy: pyobject
            a true copy of val

    """
    if isinstance(val, list):
        output = []
        for element in val:
            output.append(copy(element))
        return output

    elif isinstance(val, dict):
        output ={}
        for element in val:
            print(element, val[element])
            output[copy(element)] = copy(val[element])
        return output

    return copyLib.copy(val)
    
