from STLC_proj.lexer import lexer_int, lexer_variable, Variable, Int, Stream

def make_positive_test(lexer,string:str,value): #Refactoriza los test predefinidos
    result = lexer(Stream(string)) 
    #print(result)
    #print(value)
    assert result == value

def make_negative_test(lexer,string:str): #Refactoriza los test predefinidos a Fallo
    result = lexer(Stream(string)) 
    #print(result)
    #print(value)
    assert result is None

''' Test de variable '''
def test_lexer_variable_guion(): # Prueba variables con guión
    make_positive_test(lexer_variable,"_cajas = 5",Variable("_cajas"))
    
def test_lexer_variable_minusculas(): # Prueba variables en minúsculas
    make_positive_test(lexer_variable,"cajas = 5",Variable("cajas"))
    
def test_lexer_variable_mayusculas(): # Prueba variables en mayúscula
    make_positive_test(lexer_variable,"caJas = 5",Variable("caJas"))

def test_lexer_variable_unicaracter(): # Prueba variables con un solo caracter
    make_positive_test(lexer_variable,"c = 5",Variable("c"))
    
def test_lexer_variable_none(): # Prueba variables con salida None
    make_negative_test(lexer_variable,"_")
     
def test_lexer_variable_no_digito(): # Prueba variables que comiencen con dígitos
    make_negative_test(lexer_variable,"125caJas = 5")
    
def test_lexer_variable_no_otrosvalores(): # Prueba variables que comiencen con cualquier otro símbolo
    make_negative_test(lexer_variable,"=$125caJas = 5")

def test_lexer_variable_vacio(): # Prueba variable en cadena vacía
    make_negative_test(lexer_variable,"")
     
    
''' Test de Int '''
def test_lexer_int_digito(): # Prueba int positivo de un digito
    make_positive_test(lexer_int,"2",Int(2))

def test_lexer_int_negativo(): # Prueba int negativo con un dígito
    make_positive_test(lexer_int,"-3",Int(-3))

def test_lexer_int_digitos(): # Prueba int positivo de más de una cadena
    make_positive_test(lexer_int,"5569",Int(5569))

def test_lexer_int_negativos(): # Prueba int negativo de más de una cadena 
    make_positive_test(lexer_int,"-869",Int(-869))
     
def test_lexer_int_otrosvalores1(): # Prueba int con cadenas de letras
    make_negative_test(lexer_int,"xtrs=56")

def test_lexer_int_otrosvalores2(): # Prueba int con símbolos de operador
    make_negative_test(lexer_int,"+xtrs=56")
    
def test_lexer_int_vacio(): # Prueba int en cadena vacía
    make_negative_test(lexer_int,"")