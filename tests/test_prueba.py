from STLC_proj.lexer import (
    lexer_int,
    lexer_variable,
    lexer_operator,
    lexer_bool,
    lexer_unit,
    Stream,
    Variable,
    Int,
    Operator,
    Bool,
    UnitExp,
)


def make_positive_test(
    lexer, string: str, value
):  # Refactoriza los test predefinidos
    result = lexer(Stream(string))
    # print(result)
    # print(value)
    assert result == value


def make_negative_test(
    lexer, string: str
):  # Refactoriza los test predefinidos a Fallo
    result = lexer(Stream(string))
    # print(result)
    # print(value)
    assert result is None
    
def make_position_test(
    lexer, string: str
):  # Refactoriza los test predefinidos para la posición
    s = Stream(string)
    lex_var =lexer_variable(s)
    if lex_var is not None: # si identifica variable, posicion toma longitud de la cadena
        assert len(lex_var.name) == s.get_posicion()
    else: # en el caso contrario, posición original
        assert s.get_posicion() == 0


""" ***************** Test de Variable  ******************** """

def test_lexer_variable_guion():  # Prueba variables con guión
    make_positive_test(lexer_variable, "_cajas = 5", Variable("_cajas"))


def test_lexer_variable_minusculas():  # Prueba variables en minúsculas
    make_positive_test(lexer_variable, "cajas = 5", Variable("cajas"))


def test_lexer_variable_mayusculas():  # Prueba variables en mayúscula
    make_positive_test(lexer_variable, "caJas = 5", Variable("caJas"))


def test_lexer_variable_unicaracter():  # Prueba variables con un solo caracter
    make_positive_test(lexer_variable, "c = 5", Variable("c"))


def test_lexer_variable_none():  # Prueba variables con salida None
    make_negative_test(lexer_variable, "_")

def test_lexer_variable_no_digito():  # Prueba variables que comiencen con dígitos
    make_negative_test(lexer_variable, "125caJas = 5")

def test_lexer_variable_no_otrosvalores():  # Prueba variables que comiencen con cualquier otro símbolo
    make_negative_test(lexer_variable, "=$125caJas = 5")
    
def test_lexer_variable_True():  # Prueba variables Booleanas con salida None
    make_negative_test(lexer_variable, "True")
    
def test_lexer_variable_False():  # Prueba variables Booleanas  con salida None
    make_negative_test(lexer_variable, "False")

def test_lexer_variable_vacio():  # Prueba variable en cadena vacía
    make_negative_test(lexer_variable, "")

""" Test de Posicion en lexer Variable """
def test_lexer_variable_posicion_guion():  # Prueba posicion para variables con salida Variable
    make_position_test(lexer_variable, "_cajas = 5")

def test_lexer_variable_posicion_minusculas(): 
    make_position_test(lexer_variable, "cajas = 5")

def test_lexer_variable_posicion_mayusculas():
    make_position_test(lexer_variable, "caJas = 5")

def test_lexer_variable_posicion_unicaracter():
    make_position_test(lexer_variable, "c = 5")
  
def test_lexer_variable_position_none():  # Prueba posicion 0 para variables con salida None
    make_position_test(lexer_variable, "_")
    
def test_lexer_variable_position_no_digito():  
    make_position_test(lexer_variable, "125caJas = 5")

def test_lexer_variable_posicion_no_otrosvalores():  
    make_position_test(lexer_variable, "=$125caJas = 5")

def test_lexer_variable_posicion_True():  
    make_position_test(lexer_variable, "True")
    
def test_lexer_variable_posicion_False():
    make_position_test(lexer_variable, "False")
    
def test_lexer_variable_posicion_vacio():
    make_position_test(lexer_variable, "")




""" ***************** Test de Int  ******************** """


def test_lexer_int_digito():  # Prueba int positivo de un digito
    make_positive_test(lexer_int, "2", Int(2))


def test_lexer_int_negativo():  # Prueba int negativo con un dígito
    make_positive_test(lexer_int, "-3", Int(-3))


def test_lexer_int_digitos():  # Prueba int positivo de más de una cadena
    make_positive_test(lexer_int, "5569", Int(5569))


def test_lexer_int_negativos():  # Prueba int negativo de más de una cadena
    make_positive_test(lexer_int, "-869", Int(-869))


def test_lexer_int_otrosvalores1():  # Prueba int con cadenas de letras
    make_negative_test(lexer_int, "xtrs=56")


def test_lexer_int_otrosvalores2():  # Prueba int con símbolos de operador
    make_negative_test(lexer_int, "+xtrs=56")


def test_lexer_int_vacio():  # Prueba int en cadena vacía
    make_negative_test(lexer_int, "")




""" ***************** Test de Operador  ******************** """


def test_lexer_operador_vacio():
    make_negative_test(lexer_operator, "")


def test_lexer_operator_is_operador():
    operadores = ["+", "-", "*", "/", "<", ">", "<=", ">=", "==", "&", "|", "~"]
    for op in operadores:
        make_positive_test(lexer_operator, op, Operator(op))


def test_lexer_operador_negativo():
    make_negative_test(lexer_operator, "-1")


def test_lexer_operador_espacio():
    make_positive_test(lexer_operator, "- 589", Operator("-"))


def test_lexer_operador_caracteres():
    make_negative_test(lexer_operator, "asde + 5")


def test_lexer_operador_otrosvalores():
    make_negative_test(lexer_operator, "$'?")


def test_lexer_operador_igual():
    make_negative_test(lexer_operator, "= ")




""" ***************** Test de Bool  ******************** """


def test_lexer_bool_True():
    make_positive_test(lexer_bool, "True", Bool(True))


def test_lexer_bool_False():
    make_positive_test(lexer_bool, "False", Bool(False))


def test_lexer_bool_variable():
    make_negative_test(lexer_bool, "number")


def test_lexer_bool_variable2():
    make_negative_test(lexer_bool, "_number")


def test_lexer_bool_digit():
    make_negative_test(lexer_bool, "2545")


def test_lexer_bool_parentesis():
    make_negative_test(lexer_bool, "(True)")


def test_lexer_bool_otros_simbolos():
    make_negative_test(lexer_bool, "#$(True)")


# Faltan test de posición al fallo NO VARIABLE
