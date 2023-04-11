import sys
import ast


try:
    a = ast.literal_eval(sys.argv[1])
    b = ast.literal_eval(sys.argv[2])
except:
    sys.exit("pass all the arguments")


#sum function
def endpoint(a, b):
    return {"ouput":a+b}


print(endpoint(a,b))