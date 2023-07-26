from STLC_proj.lexer import (
    lexer_int,
    lexer_variable,
    lexer_operator,
    lexer_bool,
    lexer_unit,
    id_lexer,
    reader_lexer,
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
    print(result)
    print(value)
    assert result == value


def make_negative_test(
    lexer, string: str
):  # Refactoriza los test predefinidos a Fallo
    result = lexer(Stream(string))
    # print(result)
    # print(value)
    assert result is None


def make_positive_position_test(
    lexer, string: str, final_position
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


def make_positive_id_test(
    string: str, stream: str, value
):  # Refactoriza los test predefinidos para la identificación de cadenas
    found_lexer = id_lexer(string)
    result = found_lexer(Stream(stream))
    #print(found_lexer)
    #print(result)
    assert result == value


def make_negative_id_test(
    string: str, stream:str
):  # Refactoriza los test predefinidos para la identificación de cadenas
    found_lexer = id_lexer(string)
    result = found_lexer(Stream(stream))
    assert result is None


""" ***************** Test de Variable  ******************** """


@pytest.mark.parametrize(
    "stream,expected",
    [
        ("_cajas = 5", Variable("_cajas")),  # Prueba variables con guión
        ("cajas = 5", Variable("cajas")),
        ("caJas = 5", Variable("caJas")),  # prueba con mayúsculas
        ("c = 5", Variable("c")),  # prueba con una sola variable
    ],
)
def test_variable_positive(stream: str, expected: Variable):
    make_positive_test(lexer_variable, stream, expected)


@pytest.mark.parametrize(  # Prueba cadenas con salida None
    "stream",
    [
        "_",  # Prueba con guión
        "125caJas = 5",  # Prueba con dígitos
        "=$125caJas = 5",  # Prueba con simbolos no reconocidos
        "True",  # Prueba con booleanas
        "False",
        "",  # Prueba con cadena vacía
    ],
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
    "stream", ["_", "125caJas = 5", "=$125caJas = 5", "True", "False", ""]
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_variable_negative_posicion(stream: str):
    make_negative_position_test(lexer_variable, stream)


""" ***************** Test de Int  ******************** """


@pytest.mark.parametrize(  # Prueba enteros positivos y negativos
    "stream,expected",
    [
        ("2", Int(2)),
        ("-3", Int(-3)),
        ("5569", Int(5569)),
        ("-869", Int(-869)),  # Prueba variables con guión
    ],
)
def test_lexer_int_positive(stream: str, expected: Variable):
    make_positive_test(lexer_int, stream, expected)


@pytest.mark.parametrize(  # Prueba cadenas con salida None
    "stream", ["xtrs=56", "+xtrs=56", "", "_", "_4556", "$#"]
)
def test_lexer_int_negative(stream: str):
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
"""

@pytest.mark.parametrize(  # Prueba operadores predefinidos
    "stream,expected",
    [
        ("+", Operator("+")),
        ("- ", Operator("- ")),
        ("*", Operator("*")),
        ("/", Operator("/")),
        ("<", Operator("<")),
        (">", Operator(">")),
        ("<=", Operator("<=")),
        (">=", Operator(">=")),
        ("==", Operator("==")),
        ("&", Operator("&")),
        ("|", Operator("|")),
        ("~", Operator("~")), 
        ("- 589", Operator("- ")),
    ],
)
def test_lexer_operator_positive(stream: str, expected: Variable):
    make_positive_test(lexer_operator, stream, expected)


@pytest.mark.parametrize(  # Prueba cadenas con salida None
    "stream", ["", "-1", "", "_", "asde + 5", "$#", "= "]
)
def test_lexer_operator_negative(stream: str):
    make_negative_test(lexer_operator, stream)


@pytest.mark.parametrize(
    "stream",
    ["+", "- ", "*", "/", "<", ">", "<=", ">=", "==", "&", "|", "~", "- 8546s"],
)  # Prueba posicion para cadenas con salida Operador
def test_lexer_operator_positive_posicion(stream: str):
    lenght = len(str(lexer_operator(Stream(stream)).name))
    make_positive_position_test(lexer_operator, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["", "_", "caJas", "=$125caJas = 5", "True", "False", "-8546s"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_operator_negative_posicion(stream: str):
    make_negative_position_test(lexer_operator, stream)
"""

""" *****************Test identificador de cadenas ***************************** """


"""@pytest.mark.parametrize(  # Prueba operadores aislados
    "stream,expected",
    [
        ("+", Operator("+")),
        ("- ", Operator("- ")),
        ("*", Operator("*")),
        ("/", Operator("/")),
        ("<", Operator("<")),
        (">", Operator(">")),
        ("<=", Operator("<=")),
        (">=", Operator(">=")),
        ("==", Operator("==")),
        ("&", Operator("&")),
        ("|", Operator("|")),
        ("~", Operator("~")),  # Prueba operadores aislados
        ("- 589", Operator("- ")),
    ],
)
def test_lexer_operator_positive(stream: str, expected: Variable):
    make_positive_id_test(lexer_operator,stream, expected)"""


@pytest.mark.parametrize(  # Prueba identificación de bool
    "stream,symbol,expected",
    [
        ("True", "True", "True"),
        ("False ", "False", "False"),
        ("True45s45a", "True", "True"),
        ("False+-g ", "False", "False"),
    ],
)
def test_lexer_bool_positive(stream: str, symbol: str, expected: str):
    make_positive_id_test(symbol, stream, expected)

@pytest.mark.parametrize(  # Prueba identificación de bool con salida None
    "stream,symbol",
    [
        ("False ", "True"),
        ("True ", "False"),
        ("Tre45s45a", "True"),
        (" False+-g ", "False"),
        (" ", "False"),
        ("58False", "False"),
    ],
)
def test_lexer_bool_negative(stream: str, symbol: str):
    make_negative_id_test(symbol, stream)

""" ***************** Test de Bool, Unit, Parentesis, puntos, flecha, if..then   ******************** """
"""

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
"""

# Faltan test de posición al fallo NO VARIABLE
