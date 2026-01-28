# Buggy Calculator Module
# This file has multiple code quality issues

def add(x,y):
    return x+y

def subtract( x, y ):
    result=x-y
    return result

def multiply(a, b):
    """Multiply two numbers"""
    return a*b

def divide(x,y):
    return x/y

class calculator:
    def __init__(self,value):
        self.value=value
    
    def add(self,x):
        self.value=self.value+x
        return self.value
    
    def get_value(self):
        return self.value

def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)

def power(base,exp):
    result=1
    for i in range(exp):
        result=result*base
    return result
