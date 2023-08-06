# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:08:38 2019

@author: Soumitra
"""
def sayhello(name='Person'):
    print("Hi There Beautiful %s."% name)
def add(x,y):
    """"Simple Addition of two numbers."""
    print(x+y)
def minus(x,y):
    """"Simple Substraction of two numbers."""
    print(x-y)
def prod(x,y):
    """"Simple Multiplication of two numbers."""
    print(x*y)
def div(x,y):
    """"Simple Division of two numbers."""
    print(x/y)
def fldiv(x,y):
    """"Simple Floor Division of two numbers."""
    print(x//y)
def power(x,y):
    """Exponent Function."""
    print(x**y)


def fact(x):
    """
    factorial of a number.
    """
    if type(x)==int:
        flg="invalid for negative integers"
        if x>0:
            return fact(x-1)*x
        elif x<0:
            raise Exception(flg)
        else:
            return 1
    else:
        raise Exception("invalid for non-integers")


def strrev(s):
    """Reversing a String."""
    if type(s)==str:
        return s[::-1]
    else:
        raise Exception("Not a string")

def numrev(n):
    """Reversing a Number."""
    if type(n)==int:
        a=n
        rev=0
        while(a>0):
            rev=rev*10
            rev=rev+a%10
            a=a//10
        return rev
    else:
        raise Exception("Only positive integers allowed.")

        
def palindrome(x):
    """Function to check if a number/string is a palindrome."""
    if type(x)==int:
        if numrev(x)==x:
            return True
        else:
            return False
    elif type(x)==str:
        if strrev(x)==x:
            return True
        else:
            return False
    else:
        raise Exception("Only positive integers and strings allowed.")

def ncr(n,r):
    """
       Combination formula:
        ncr: r out of n combinations
    """
    if(n>r):
        p=fact(r)*fact(n-r)
        return int((fact(n)/p))
    else:
        raise Exception("First Argument Must be Greater than Second Argument")

def npr(n,r):
    """
    Permutation formula:
        npr: r out of n permutations
    """
    if(n>r):
        return int((fact(n)/fact(n-r)))
    else:
        raise Exception("First Argument Must be Greater than Second Argument")

def bubble(l):
    """
    Takes a list as the argument and returns a sorted array.

    """
    n=len(l)
    for i in range(n-1):
        for j in range(n-i-1):
            if(l[j]>l[j+1]):
                l[j]=l[j]+l[j+1]
                l[j+1]=l[j]-l[j+1]
                l[j]=l[j]-l[j+1]
    return l

    
def check_sorted(l):
    """
    Check if the array is sorted.
    """
    
    for i in range(len(l)-1):
        if l[i]<l[i+1]:
            continue
        else:
            return False
def linsearch(l,x):
    """
    Linear search for an elememnt in an array.
    Linsearch(l,x)-->l is the list and x is the item to be serached.
    """
    for i in range(len(l)):
        if x==l[i]:
            return i
        else: 
            return False

def binsearch(arr, x): 
    """
    Binary search:
        Takes an array and the item to be found.
    """
    l=0
    r=len(arr)
    # Check base case 
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # If element is present at the middle itself 
        if arr[mid] == x: 
            return mid 
          
        # If element is smaller than mid, then it  
        # can only be present in left subarray 
        elif arr[mid] > x: 
            return binsearch(arr, l, mid-1, x) 
  
        # Else the element can only be present  
        # in right subarray 
        else: 
            return binsearch(arr, mid + 1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1

def ciphertext(path,k):
    """Ciphertext(path,k) takes two aruguments. The first argument is the path for the text file. The second argument is the key for caesar cipher."""
    obj=open(path,'r')
    m=obj.read()
    coded=""
    for c in m:
        coded=coded+chr(ord(c)+(k))
    obj.close()
    obj=open(path,'w+')
    obj.write(coded)
    obj.close()
 
def deciphertext(path,k):
    """Deciphertext(path,k) takes two aruguments. The first argument is the path for the text file. The second argument is the key for caesar cipher."""
    obj=open(path,'r')
    coded=obj.read()
    decoded=""
    for d in coded:
        decoded=decoded+chr(ord(d)-(k))
    obj.close()
    obj=open(path,'w+')
    obj.write(decoded)
    obj.close()
    
def XOR(a,b):
    """XOR Operation"""
    if((type(a)!=int and type(a)!=bool) or (type(b)!=int and type(b)!=bool)):
        raise Exception("Invalid Data-types.")
    elif((a== True and b == True) or (a==False and b == False)):
        return False
    else:
        return True



def selsort(l):
    """Selection sort. Takes a list as argument."""
    m = len(l)
    s =[]
    for i in range(m):
        mini = l[i]
        for j in range(i+1,m):
            if(l[j]<mini):
                temp = mini
                mini = l[j]
                l[j] = temp
            else:
                continue
        s.append(mini)
    return s


def insertion(l):
    """"Insertion Sort. takes input as a list by reference."""
    m = len(l)
    for i in range(1,m):
        k= l[i]
        j=i-1
        while j>=0 and k<l[j]:
            l[j+1] = l[j]
            j-=1
            l[j+1] = k
    return l


def bintodec(x):
    """Convert Binary to Decimal. Input is a string and output is a positive integer."""
    num = 0
    n = len(x)
    for i in range(n):
        num = num + (2**i)*(int(x[n-i-1]))
    return num

def dectobin(x):
    """Convert Decimal to Binary. Input is a positive integer and output is a string."""
    ans=''
    while(x>1):
        tmp = x%2
        ans = str(tmp) + ans
        x = x//2
    ans = str(x) + ans
    return ans


def opcipher(s):
    """"Simple cipher that takes a string as input. Spaces allowed. output string has all lowercase letters. using the functio twice deciphers it."""
    a = 'abcdefghijklmnopqrstuvwxyz'
    r = ''
    for x in s:
        x = x.lower()
        if(x!=' '):
            x = a[25-a.index(x)]
        r+=x
    return r

