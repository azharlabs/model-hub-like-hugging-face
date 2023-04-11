import sys
import ast


try:
    a = ast.literal_eval(sys.argv[1])
    b = ast.literal_eval(sys.argv[1])
except:
    sys.exit("pass all the arguments")


#sum function
def sum(a, b):
    return {"ouput":a+b}


endpoint(a,b)