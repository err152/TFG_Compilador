# frag1.py
from inspect import Parameter, Signature

def _make_init(fields):
    '''
    Give a list of field names,make an __init__method
    '''
    code = 'def __init__(self,%s):\n' % ','.join(fields)

    for name in fields:
        code += '   self.%s = %s\n' % (name,name)
    return code

def _make_setter(dcls):
    code = 'def __set__(self,instance,value):\n'
    for d in dcls.__mro__:
        if 'set_code' in d.__dict__:
            for line in d.set_code():
                code += '   '+line+'\n'
    return code

class DescriptorMeta(type):
    def __init__(self,clsname,bases,clsdict):
        super().__init__(clsname,bases,clsdict)
        if '__set__' in clsdict:
            raise TypeError('use set_code(), not __set__()')
        
        #Make the set code
        code = _make_setter(self)
        exec(code,globals(),clsdict)
        setattr(self,'__set__',clsdict['__set__'])
        
class Descriptor(metaclass=DescriptorMeta):
    def __init__(self,name=None):
        self.name = name
        
    @staticmethod
    def set_code():
        return [
            'instance.__dict__[self.name] = value'
            ]

    def __delete__(self,instance):
        print("Delete",self.name)
        del instance.__dict__[self.name]

class Typed(Descriptor):
    ty = object #expected type
    @staticmethod
    def set_code():
        return [
            ' if not isinstance(value,self.ty):',
            '   raise TypeError("Expected %s" % self.ty)'
            ]

class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class String(Typed):
    ty = str

class Positive(Descriptor):
    @staticmethod
    def set_code():
        return [
            'if value < 0:',
            '   raise ValueError("Must be >= 0")'
            ]

class MyDescriptor(Descriptor):
    def __set__(self,instance,value):
        pass
    
# Lenght Checking
class Sized(Descriptor):
    def __init__(self,*args,maxlen,**kwargs):
        self.maxlen = maxlen
        super().__init__(*args,**kwargs)

    @staticmethod
    def set_code():
        return [
            'if len(value) > self.maxlen:',
            '   raise ValueError("Too big")'
            ]
    
class SizedString(String,Sized):
    pass
    #super().__set__(instance,value)

import re

# Pattern matching
class Regex(Descriptor):
    def __init__(self,*args,pat,**kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args,**kwargs)

    @staticmethod
    def set_code():
        return [
            'if not self.pat.match(value):',
            '   raise ValueError("Invalid string")'
            ]

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

        if fields:
            init_code = _make_init(fields)
            exec(init_code,globals(),clsdict)
            
        clsobj = super().__new__(cls,clsname,bases,dict(clsdict))
        
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

