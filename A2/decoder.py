import argparse
import numpy as np





if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--states",type=str,required=True)
    parser.add_argument("--value-policy",type=str,required=True)
    args = parser.parse_args()

    try:
        statefile = open(args.states,'r')
        valuePolicyfile = open(args.value_policy,'r')
    except IOError:
        print("Please check the path of the provided files")
        exit(1)

    lines = statefile.readlines()
    lines = [int(x.strip()) for x in lines]
    lines_ = valuePolicyfile.readlines()
    lines_ = [x.strip() for x in lines_]
    for i in range(len(lines)):
        linesy = lines_[i].split(" ")
        if int(linesy[1])==3:
            print(str(f'{lines[i]:04}') + str(" ") + "4" + str(" ") + linesy[0])
        elif int(linesy[1])==4:
            print(str(f'{lines[i]:04}') + str(" ") + "6"+ str(" ") + linesy[0])
        else:
            print(str(f'{lines[i]:04}') + str(" ") + linesy[1]+ str(" ") + linesy[0])
    
