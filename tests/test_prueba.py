from typing import Optional, TypeVar, Callable

from STLC_proj.Lexer import (
    lexer_int,
    lexer_variable,
    lexer_operator,
    lexer_bool,
    lexer_unit,
    lexer_identifier,
    reader_lexer,
    lexer_leftP,
    lexer_rightP,
    lexer_arrowR,
    lexer_lineLambda,
    lexer_if,
    lexer_then,
    lexer_int_type,
    lexer_bool_type,
    lexer_unit_type,
    lexer_token,
    lexer,
    Stream,
    Variable,
    Int,
    Operator,
    Bool,
    UnitExp,
    LeftP,
    RightP,
    ArrowR,
    LineLambda,
    If,
    Then,
    IntType,
    BoolType,
    UnitType,
    Equals,
    TwoP
)

import pytest  # buscar cómo arreglar este error en editor

T = TypeVar("T")


def make_positive_test(
    lexer: Callable[[Stream], Optional[T]], string: str, value: T
):  # Refactoriza los test predefinidos
    result = lexer(Stream(string))
    print(result)
    print(value)
    assert result == value


def make_negative_test(
    lexer: Callable[[Stream], Optional[T]], string: str
):  # Refactoriza los test predefinidos a Fallo
    result = lexer(Stream(string))
    # print(result)
    # print(value)
    assert result is None


def make_positive_position_test(
    lexer: Callable[[Stream], Optional[T]],
    string: str,
    final_position: Optional[int],
):  # Refactoriza los test predefinidos para la posición
    s = Stream(string)
    lex_var = lexer(s)
    assert (
        s.get_posicion() == final_position
    )  # si identifica variable, posicion toma longitud de la cadena


def make_negative_position_test(
    lexer: Callable[[Stream], Optional[T]], string: str
):  # Refactoriza los test predefinidos para la posición
    s = Stream(string)
    lex_var = lexer(s)
    assert s.get_posicion() == 0  # verifica regreso a posición original


def make_positive_id_test(
    stream: str, symbol: str, value: str
):  # Refactoriza los test predefinidos para la identificación de cadenas
    found_lexer = lexer_identifier(symbol)
    result = found_lexer(Stream(stream))
    # print(found_lexer)
    # print(result)
    assert result == value


def make_negative_id_test(
    stream: str, symbol: str
):  # Refactoriza los test predefinidos para la identificación de cadenas
    found_lexer = lexer_identifier(symbol)
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
    "stream", ["_cajas", "cajas", "caJas", "c"]
)  # Prueba posicion para cadenas con salida Variable
def test_lexer_variable_positive_posicion(stream: str):
    lenght = len(stream)
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
def test_lexer_int_positive(stream: str, expected: Int):
    make_positive_test(lexer_int, stream, expected)


@pytest.mark.parametrize(  # Prueba cadenas con salida None
    "stream", ["xtrs=56", "+xtrs=56", "", "_", "_4556", "$#"]
)
def test_lexer_int_negative(stream: str):
    make_negative_test(lexer_int, stream)


@pytest.mark.parametrize(
    "stream", ["5", "589", "-8546"]
)  # Prueba posicion para cadenas con salida Variable
def test_lexer_int_positive_posicion(stream: str):
    lenght = len(stream)
    make_positive_position_test(lexer_int, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "caJas", "=$125caJas = 5", "True", "False"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_int_negative_posicion(stream: str):
    make_negative_position_test(lexer_int, stream)


""" ***************** Test de Identificador de cadenas  ******************** """


@pytest.mark.parametrize(
    "stream,expected",
    [
        ("+", "+"),  # Prueba operadores predefinidos
        ("- ", "- "),
        ("*", "*"),
        ("/", "/"),
        ("<", "<"),
        (">", ">"),
        ("<=", "<="),
        (">=", ">="),
        ("==", "=="),
        ("&", "&"),
        ("|", "|"),
        ("~", "~"),
        ("<=", "<"),  # Revisión de cadena operador incompleta
        (">=", ">"),
        ("- 589", "- "),
        ("True45", "True"),  # Prueba booleanos
        ("False45", "False"),
        ("unity", "unity"),  # Prueba unity
        ("if", "if"),  # Prueba if...then
        ("then", "then"),
        ("(if", "("),  # Prueba paréntesis
        (")then", ")"),
        ("->", "->"),  # Prueba arrow
        ("/", "/"),  # Prueba lineLambda
        ("=", "="),  # Prueba equals
        (":", ":"), # Prueba dos puntos
        ("Int('485')", "Int"),  # Prueba tipos
        ("Bool(False)", "Bool"),
        ("Unit(", "Unit"),
    ],
)
def test_identifier_function_positive(stream: str, expected: str):
    make_positive_id_test(stream, expected, expected)


@pytest.mark.parametrize(
    "stream,symbol",
    [
        (" ", "+"),  # Prueba salida None
        ("-1 ", "- "),
        ("&", "*"),
        ("unit", "unity"),
    ],
)
def test_identifier_function_negative(stream: str, symbol: str):
    make_negative_id_test(stream, symbol)


""" ***************** Test de Operador  ******************** """


@pytest.mark.parametrize(
    "stream, expected",
    [
        ("<=", Operator("<=")),
        (">=", Operator(">=")),
    ],  # Verificación de operadores
)
def test_lexer_operator_positive(stream: str, expected: Operator):
    make_positive_test(lexer_operator, stream, expected)


@pytest.mark.parametrize(
    "stream",
    ["-584", "="],  # verificación de no operadores
)
def test_lexer_operator_negative(stream: str):
    make_negative_test(lexer_operator, stream)


@pytest.mark.parametrize(
    "stream", ["+", "- ", "*", "/", "<", ">", "<=", ">=", "==", "&", "|", "~"]
)  # Prueba posicion para cadenas con salida operador
def test_lexer_operator_positive_posicion(stream: str):
    lenght = len(stream)
    make_positive_position_test(lexer_operator, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "caJas", "$125caJas = 5", "True", "False"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_operator_negative_posicion(stream: str):
    make_negative_position_test(lexer_operator, stream)


""" ***************** Test de Bool  ******************** """


@pytest.mark.parametrize(
    "stream, expected",
    [("True", Bool(True)), ("False", Bool(False))],  # Verificación de valores
)
def test_lexer_bool_positive(stream: str, expected: Bool):
    make_positive_test(lexer_bool, stream, expected)


@pytest.mark.parametrize(
    "stream",
    ["true", "false"],  # verificación de no operadores
)
def test_lexer_bool_negative(stream: str):
    make_negative_test(lexer_bool, stream)


@pytest.mark.parametrize(
    "stream", ["True", "False"]
)  # Prueba posicion para cadenas con salida bool
def test_lexer_bool_positive_posicion(stream: str):
    lenght = len(stream)
    make_positive_position_test(lexer_bool, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "caJas", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_bool_negative_posicion(stream: str):
    make_negative_position_test(lexer_bool, stream)


""" ***************** Test de unit ******************** """


@pytest.mark.parametrize(
    "stream, expected",
    [("unit", UnitExp())],  # Verificación
)
def test_lexer_unit_positive(stream: str, expected: UnitExp):
    make_positive_test(lexer_unit, stream, expected)


@pytest.mark.parametrize(
    "stream", ["unit"]
)  # Prueba posicion para cadenas con salida unit
def test_lexer_unit_positive_posicion(stream: str):
    lenght = len(stream)
    make_positive_position_test(lexer_unit, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_unit_negative_posicion(stream: str):
    make_negative_position_test(lexer_unit, stream)


""" ***************** Test de parentesis ******************** """


@pytest.mark.parametrize(
    "lexer,stream, expected",
    [
        (lexer_leftP, "(", LeftP()),
        (lexer_rightP, ")", RightP()),
    ],  # Verificación
)
def test_lexer_parenthesis_positive(
    lexer: Callable[[Stream], Optional[T]], stream: str, expected: T
):
    make_positive_test(lexer, stream, expected)


@pytest.mark.parametrize(
    "lexer,stream",
    [(lexer_leftP, "("), (lexer_rightP, ")")],  # Verificación
)  # Prueba posicion para cadenas con salida parentesis
def test_lexer_parenthesis_positive_posicion(
    lexer: Callable[[Stream], Optional[T]], stream: str
):
    lenght = len(stream)
    make_positive_position_test(lexer, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_leftP_negative_posicion(stream: str):
    make_negative_position_test(lexer_leftP, stream)


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_rightP_negative_posicion(stream: str):
    make_negative_position_test(lexer_rightP, stream)


""" ***************** Test de arrow******************** """


def test_lexer_arrowR_positive():
    make_positive_test(lexer_arrowR, "->", ArrowR())  # verificación


def test_lexer_arrowR_positive_posicion():
    make_positive_position_test(
        lexer_arrowR, "->", len("->")
    )  # Avance de posición


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_arrowR_negative_posicion(stream: str):
    make_negative_position_test(lexer_arrowR, stream)


""" ***************** Test de lineLambda******************** """


def test_lexer_lineLambda_positive():
    make_positive_test(lexer_lineLambda, "/", LineLambda())  # verificación


def test_lexer_lineLambda_positive_posicion():
    make_positive_position_test(
        lexer_lineLambda, "/", len("/")
    )  # Avance de posición


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_lineLambda_negative_posicion(stream: str):
    make_negative_position_test(lexer_lineLambda, stream)


""" ***************** Test de if..then ******************** """


@pytest.mark.parametrize(
    "lexer,stream, expected",
    [
        (lexer_if, "if", If()),
        (lexer_then, "then", Then()),
    ],  # Verificación
)
def test_lexer_if_then_positive(
    lexer: Callable[[Stream], Optional[T]], stream: str, expected: T
):
    make_positive_test(lexer, stream, expected)


@pytest.mark.parametrize(
    "lexer,stream",
    [
        (lexer_if, "if"),
        (lexer_then, "then"),
    ],
)  # Prueba posicion para cadenas con salida parentesis
def test_lexer_if_then_positive_posicion(
    lexer: Callable[[Stream], Optional[T]], stream: str
):
    lenght = len(stream)
    make_positive_position_test(lexer, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_if_negative_posicion(stream: str):
    make_negative_position_test(lexer_if, stream)


@pytest.mark.parametrize(
    "stream",
    ["_", "Unit", "$125caJas = 5", "+548", "-59"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_then_negative_posicion(stream: str):
    make_negative_position_test(lexer_then, stream)


""" ***************** Test de tipos ******************** """


@pytest.mark.parametrize(
    "lexer,stream, expected",
    [
        (lexer_int_type, "Int", IntType()),
        (lexer_bool_type, "Bool", BoolType()),
        (lexer_unit_type, "Unit", UnitType()),
    ],  # Verificación
)
def test_lexer_type_positive(
    lexer: Callable[[Stream], Optional[T]], stream: str, expected: T
):
    make_positive_test(lexer, stream, expected)


@pytest.mark.parametrize(
    "lexer,stream",
    [
        (lexer_int_type, "Int"),
        (lexer_bool_type, "Bool"),
        (lexer_unit_type, "Unit"),
    ],
)  # Prueba posicion para cadenas con salida parentesis
def test_lexer_type_positive_posicion(
    lexer: Callable[[Stream], Optional[T]], stream: str
):
    lenght = len(stream)
    make_positive_position_test(lexer, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["int", "unit", "bool" "$125caJas = 5", "+548", "-59", "()"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_intType_posicion(stream: str):
    make_negative_position_test(lexer_int_type, stream)


@pytest.mark.parametrize(
    "stream",
    ["int", "unit", "bool" "$125caJas = 5", "+548", "-59", "()"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_unitType_posicion(stream: str):
    make_negative_position_test(lexer_unit_type, stream)


@pytest.mark.parametrize(
    "stream",
    ["int", "unit", "bool" "$125caJas = 5", "+548", "-59", "()"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_boolType_posicion(stream: str):
    make_negative_position_test(lexer_bool_type, stream)


""" ***************** Test de literal******************** """


@pytest.mark.parametrize(
    "lexer, stream, expected",
    [
        (lexer_int_type, "Int", IntType()),
        (lexer_bool_type, "Bool", BoolType()),
        (lexer_unit_type, "Unit", UnitType()),
    ],  # Verificación
)
def test_lexer_literal_positive(
    lexer: Callable[[Stream], Optional[T]], stream: str, expected: T
):
    make_positive_test(lexer, stream, expected)


@pytest.mark.parametrize(
    "lexer,stream",
    [
        (lexer_int_type, "Int"),
        (lexer_bool_type, "Bool"),
        (lexer_unit_type, "Unit"),
    ],
)  # Prueba posicion para cadenas con salida parentesis
def test_lexer_literal_positive_posicion(
    lexer: Callable[[Stream], Optional[T]], stream: str
):
    lenght = len(stream)
    make_positive_position_test(lexer, stream, lenght)


@pytest.mark.parametrize(
    "stream",
    ["int", "unit", "bool" "$125caJas = 5", "+548", "-59", "()"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_intType_posicion(stream: str):
    make_negative_position_test(lexer_int_type, stream)


@pytest.mark.parametrize(
    "stream",
    ["int", "unit", "bool" "$125caJas = 5", "+548", "-59", "()"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_unitType_posicion(stream: str):
    make_negative_position_test(lexer_unit_type, stream)


@pytest.mark.parametrize(
    "stream",
    ["int", "unit", "bool" "$125caJas = 5", "+548", "-59", "()"],
)  # Prueba posicion 0 para cadenas con salida None
def test_lexer_boolType_posicion(stream: str):
    make_negative_position_test(lexer_bool_type, stream)


""" ***************** Test de función de token ******************** """
@pytest.mark.parametrize(
    "stream, expected",
    [
        ("   -15 +45 = 30 ", [Int(-15),Operator("+"),Int(45),Equals(),Int(30)]),
        ("r = -30", [Variable('r'),Equals(), Int(-30)]),
        ("( r = 30)", [LeftP(),Variable('r'),Equals(), Int(30), RightP()]), #No debe pasar en parser C.I.
        (" r : True", [Variable('r'),TwoP(), Bool(True)]),
        (" _variable : unit", [Variable('_variable'),TwoP(), UnitExp()]),
        (" variable : Unit", [Variable('variable'),TwoP(), UnitType()]),
        (" vaR : Int", [Variable('vaR'),TwoP(), IntType()]),
        ("_vaR : Int", [Variable('_vaR'),TwoP(), IntType()]),
        ("Int -> Bool", [IntType(),ArrowR(), BoolType()]),
        ("", []),
        (" ", []),
        ("/x = 5 ", [LineLambda(),Variable('x'), Equals(),Int(5)])        
    ],  # Verificación
)
def test_lexer_token_positive(stream: str, expected: T):
    make_positive_test(lexer, stream, expected)


