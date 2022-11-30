# frag1.py
from inspect import Parameter, Signature

class Descriptor:
    def __init__(self,name=None):
        self.name = name
        
    def __set__(self,instance,value):
        print("Set",value)
        instance.__dict__[self.name] = value

    def __delete__(self,instance):
        print("Delete",self.name)
        del instance.__dict__[self.name]

class Typed(Descriptor):
    ty = object #expected type
    def __set__(self,instance,value):
        if not isinstance(value,self.ty):
            raise TypeError("Expected %s" % self.ty)
        super().__set__(instance,value)

class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class String(Typed):
    ty = str

class Positive(Descriptor):
    def __set__(self,instance,value):
        if value < 0:
            raise ValueError('Must be >= 0')
        super().__set__(instance,value)

# Lenght Checking
class Sized(Descriptor):
    def __init__(self,*args,maxlen,**kwargs):
        self.maxlen = maxlen
        super().__init__(*args,**kwargs)

    def __set__(self,instance,value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance,value)

class SizedString(String,Sized):
    pass
    #super().__set__(instance,value)

import re

# Pattern matching
class Regex(Descriptor):
    def __init__(self,*args,pat,**kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args,**kwargs)

    def __set__(self,instance,value):
        if not self.pat.match(value):
            raise ValueError('Invalid string')
        super().__set__(instance,value)

class SizedRegexString(SizedString,Regex):
    pass

class PositiveInteger(Integer,Positive):
    pass

class PositiveFloat(Float,Positive):
    pass

def make_signature(names):
    return Signature(
        Parameter(name,Parameter.POSITIONAL_OR_KEYWORD)
        for name in names)

from collections import OrderedDict

class StructMeta(type):
    @classmethod
    def __prepare__(cls,name,bases):
        return OrderedDict()

    def __new__(cls,clsname,bases,clsdict):
        fields = [key for key, val in clsdict.items()
                  if isinstance(val,Descriptor)]
        for name in fields:
            clsdict[name].name = name

        clsobj = super().__new__(cls,clsname,bases,dict(clsdict))
        sig = make_signature(fields)
        setattr(clsobj,'__signature__',sig)
        return clsobj
    
class Structure(metaclass=StructMeta):
    _fields = []
    def __init__(self, *args,**kwargs):
        bound = self.__signature__.bind(*args,**kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
            
class Stock(Structure):
    name = SizedRegexString(pat='[A-Z]+$',maxlen=8)
    shares = PositiveInteger()
    price = PositiveFloat()

class Point(Structure):
    _fields = ['x','y']

