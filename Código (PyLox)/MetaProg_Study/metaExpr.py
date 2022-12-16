# metaExpr.py
# Copiar para ejecutar código
# GenerateAst("C:/Users/Eduardo/Desktop/Universidad/2o Cuatri/TFG_compilador/Código (PyLox)")

import os
    
def defineAst(self, outputDir:str, baseName:str, types:[]):
    path = outputDir + "/" + baseName + ".py"
    assert os.path.isfile(path)
    with open(path,'w')as f:
        f.write("import Token from Token" + "\n")
        f.write("import ABC, abstractmethod from abc" + "\n\n")
        f.write("class " + baseName + "(self,ABC):" + "\n")
        
        f.write("   @abstractmethod"+"\n")
        f.write("   def accept(Visitor):"+"\n")
        f.write("       pass"+"\n\n")

        defineVisitor(self,f,baseName,types)

        for tipe in types:
            className = tipe.split(":")[0].strip()
            fields = tipe.split(":")[1].strip()
            defineType(self,f,baseName,className,fields)
 
        f.close()

def defineVisitor(self, f, baseName:str, types:[]):
    f.write("class Visitor(ABC):"+"\n")

    for tipe in types:
        typeName = tipe.split(":")[0].strip()
        f.write("   @abstractmethod"+"\n")
        f.write("   def visit_"+typeName.lower()+"_"+baseName.lower()+"(self, "+baseName.lower()+": '"+baseName+"'):"+"\n")
        f.write("       pass"+"\n\n")

    f.write("\n")
    

def defineType(self, f, baseName:str, className:str, fieldList:str):
    f.write("class " + className + "(" + baseName + "):" + "\n")

    fields = fieldList.split(", ")
    # init method (Constructor)
    f.write("   " + "def __init__(self")
    for field in fields:
        name = field.split(" ")[1]
        tipe = field.split(" ")[0]
        f.write(","+name+":"+tipe)

    f.write("):" + "\n")

    # store params in fields
    for field in fields:
        name = field.split(" ")[1]
        f.write("       self." + name + " = " + name + "\n")

    # define acepta method
    f.write("\n   " + "def acepta(self, visitor: Visitor):" + "\n")
    f.write("       return visitor.visit_"+className.lower()+"_"+baseName.lower()+"(self)"+"\n")
    
    f.write("\n")

class GenerateAst:
    def __init__(self,*args,**kwargs):
        if len(args) != 1:
            print("Error: generate_ast <output directory>")
        outputDir = args[0]
        
        defineAst(self,outputDir,"Expr",["Binary : Expr left, Token operator, Expr right",
                                "Grouping : Expr expression",
                                "Literal : Object value",
                                "Unary : Token operator, Expr right"])
    
