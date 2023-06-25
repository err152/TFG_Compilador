import os
import filecmp
import sys
from io import StringIO
from lox import Lox

dir_pruebas = "C:\\Users\\Eduardo\\Desktop\\Universidad\\2o Cuatri\\TFG_compilador\\Código (PyLox)\\pruebas"
dir_resultados = "C:\\Users\\Eduardo\\Desktop\\Universidad\\2o Cuatri\\TFG_compilador\\Código (PyLox)\\pruebas\\resultados"
test_pasados = 0

for prueba in os.listdir(dir_pruebas):
    if prueba.endswith('.lox'):
        path = os.path.join(dir_pruebas,prueba)
        a = Lox()
        
        
        captura = StringIO()
        sys.stdout = captura
        a.runFile(path)
        sys.stdout = sys.__stdout__
        resultado = captura.getvalue()
        
        path_output = os.path.join(dir_resultados, prueba.replace('.lox', '.out'))
        with open(path_output,'w') as output_file:
            output_file.write(resultado)
    
       
        path_resultado = os.path.join(dir_resultados, prueba.replace('.lox', '.test'))
        
        if filecmp.cmp(path_output,path_resultado):
            test_pasados = test_pasados + 1
        else:
            print(f'{prueba}: Test fallado.')

print(f'Se pasaron {test_pasados} tests exitosamente.')
    

