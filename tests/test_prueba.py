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

import pytest  # buscar cómo arreglar este error en editor


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


def make_positive_position_test(
    lexer, string: str,final_position
):  # Refactoriza los test predefinidos para la posición
    s = Stream(string)
    lex_var = lexer(s)
    assert (
        s.get_posicion() == final_position
    )  # si identifica variable, posicion toma longitud de la cadena


def make_negative_position_test(
    lexer, string: str
):  # Refactoriza los test predefinidos para la posición
    s = Stream(string)
    lex_var = lexer(s)
    assert s.get_posicion() == 0  # verifica regreso a posición original



""" ***************** Test de Variable  ******************** """

@pytest.mark.parametrize(
    "stream,expected",
    [
        ("_cajas = 5", Variable("_cajas")),  # Prueba variables con guión
        ("cajas = 5", Variable("cajas")),
        ("caJas = 5", Variable("caJas")),  # prueba con mayúsculas
        ("c = 5", Variable("c")),  # prueba con una sola variable
    ]
)
def test_variable_positive(stream: str, expected: Variable):
    make_positive_test(lexer_variable, stream, expected)

@pytest.mark.parametrize( # Prueba cadenas con salida None
    "stream",
    [  
        "_",  # Prueba con guión
        "125caJas = 5",  # Prueba con dígitos
        "=$125caJas = 5",  # Prueba con simbolos no reconocidos
        "True",  # Prueba con booleanas
        "False",
        ""  # Prueba con cadena vacía
    ]
)
def test_variable_negative(stream: str):
    make_negative_test(lexer_variable, stream)


@pytest.mark.parametrize(
    "stream", ["_cajas = 5", "cajas = 5", "caJas = 5", "c = 5"]
)  # Prueba posicion para cadenas con salida Variable
def test_lexer_variable_positive_posicion(stream: str):
    lenght = len(lexer_variable(Stream(stream)).name)
    make_positive_position_test(lexer_variable, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "125caJas = 5", "=$125caJas = 5", "True", "False", ""]
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_variable_negative_posicion(stream: str):
    make_negative_position_test(lexer_variable, stream)


""" ***************** Test de Int  ******************** """

@pytest.mark.parametrize( # Prueba enteros positivos y negativos
    "stream,expected",
    [
        ("2", Int(2)), ("-3", Int(-3)), ("5569", Int(5569)), ("-869", Int(-869))  # Prueba variables con guión
        
    ]
)
def test_int_positive(stream: str, expected: Variable):
    make_positive_test(lexer_int, stream, expected)

@pytest.mark.parametrize( # Prueba cadenas con salida None
    "stream",
    [  
        "xtrs=56", "+xtrs=56", "", "_", "_4556", "$#"
    ]
)
def test_int_negative(stream: str):
    make_negative_test(lexer_int, stream)


@pytest.mark.parametrize(
    "stream", ["5", "589", "-8546s"]
)  # Prueba posicion para cadenas con salida Variable
def test_lexer_int_positive_posicion(stream: str):
    lenght = len(str(lexer_int(Stream(stream)).value))
    make_positive_position_test(lexer_int, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "caJas", "=$125caJas = 5", "True", "False"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_int_negative_posicion(stream: str):
    make_negative_position_test(lexer_int, stream)
    


""" ***************** Test de Operador  ******************** """

@pytest.mark.parametrize( # Prueba enteros positivos y negativos
    "stream,expected",
    [
        ("2", Int(2)), ("-3", Int(-3)), ("5569", Int(5569)), ("-869", Int(-869))  # Prueba variables con guión
        
    ]
)
def test_int_positive(stream: str, expected: Variable):
    make_positive_test(lexer_int, stream, expected)

@pytest.mark.parametrize( # Prueba cadenas con salida None
    "stream",
    [  
        "xtrs=56", "+xtrs=56", "", "_", "_4556", "$#"
    ]
)
def test_int_negative(stream: str):
    make_negative_test(lexer_int, stream)


@pytest.mark.parametrize(
    "stream", ["5", "589", "-8546s"]
)  # Prueba posicion para cadenas con salida Variable
def test_lexer_int_positive_posicion(stream: str):
    lenght = len(str(lexer_int(Stream(stream)).value))
    make_positive_position_test(lexer_int, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "caJas", "=$125caJas = 5", "True", "False"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_int_negative_posicion(stream: str):
    make_negative_position_test(lexer_int, stream)



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
