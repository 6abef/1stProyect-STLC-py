# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:10:34 2023

@author: Moisés
Definición de clases
"""
from dataclasses import dataclass
from typing import Union, Optional, TypeVar, Callable
from collections.abc import Sequence


Token = Union[
    "Variable",
    "Int",
    "IntType",
    "Operator",
    "Bool",
    "BoolType",
    "LeftP",
    "RightP",
    "TokenError",
    "ArrowR",
    "LineLambda",
    "TwoP",
    "UnitType",
    "UnitExp",
    "If",
    "Then",
    "Else",
    "Equals",
    "Space"
]


@dataclass
class Variable:
    name: str


@dataclass
class Int:
    value: int


@dataclass
class IntType:
    pass


@dataclass
class Operator:
    name: str


@dataclass
class Bool:
    value: bool


@dataclass
class BoolType:
    pass


@dataclass
class UnitExp:
    pass


@dataclass
class UnitType:
    pass


@dataclass
class LeftP:
    pass


@dataclass
class RightP:
    pass

@dataclass
class TwoP:
    pass

@dataclass
class ArrowR:
    pass


@dataclass
class LineLambda:
    pass


@dataclass
class If:
    pass


@dataclass
class Then:
    pass

@dataclass
class Else:
    pass


@dataclass
class Equals:
    pass


@dataclass
class Literal:
    pass


@dataclass
class Space:
    pass


@dataclass
class TokenError:
    error: str


@dataclass
class Stream:
    value: str
    pos: int

    def __init__(self, value: str):
        self.pos = 0
        self.value = value

    def get_char(self) -> Optional[str]:
        if len(self.value) > self.pos:
            return self.value[self.pos]
        else:
            # Esta parte podria saltarse y dejar que solo retorne None
            return None

    def consume(self):
        self.pos += 1

    def get_posicion(self):
        return self.pos

    def colocar_posicion(self, new_pos):
        self.pos = new_pos


def is_digit(string: str) -> bool:
    """Esta funcion verifica el primer caracter de un string sea un dígito"""
    if len(string) > 0:
        digit = string[0]
        if digit >= "0" and digit <= "9":
            return True
        return False  # Se podría quitar y dejar que regrese False en cualquier caso. >Dejarlo da claridad
    else:
        return False


def lexer_identifier(
    string: str,
) -> Callable[
    [Stream], Optional[str]
]:  # buscador del lexer de una cadena reconocible
    def lexer(stream: Stream) -> Optional[str]:
        position = stream.get_posicion()
        s = stream.value[position:]
        # print("\tcadena a leer: ",s, "desde posición: ", position)
        # print("\tsímbolo a comparar: ",string)
        # Sprint("\tEvaluación: ",s.startswith(string))
        if s.startswith(string):
            # print("\tSi se encontró")
            # print("\t__________________________________")
            return string
        else:
            # print("\tNo se encontró")
            # print("\t__________________________________")
            return None

    return lexer


"""l = Stream("True")
lexer_l = lexer_identifier("True")
print(l.value, lexer_l(l))"""


T = TypeVar("T")


def reader_lexer(
    symbol: str, varType: T
) -> Callable[
    [Stream], Optional[T]
]:  # ejecutor de lexer para cadena identificada
    lexer = lexer_identifier(
        symbol
    )  # Cuidado: En símbolos dobles (<=), reconocerá el símbolo unitario (<)

    def evaluator(stream: Stream) -> Optional[T]:
        evaluation = lexer(stream)
        # print("Resultado de la evaluación de",stream.value,"vs",symbol," | ",evaluation)
        if evaluation is None:
            return None
        else:
            stream.colocar_posicion(
                stream.get_posicion() + len(symbol)
            )  # cambia la posición una vez que se identifica un tipo
            # print("\tSe envía: ", varType)
            return varType

    return evaluator


"""l = Stream("- 546")
reader_l = reader_lexer("- ",Operator("- "))
print(l.value, reader_l(l))

l = Stream("<= 5")
reader_l = reader_lexer("<=",Operator("<="))
print(l.value, reader_l(l))
"""


def lexer_variable(
    stream: Stream,
) -> Optional[Variable]:  # buscador de variables
    acc: list[str] = []
    orig_post = stream.get_posicion()
    char = stream.get_char()
    if char is None:
        return None
    else:
        if (
            (char == "_")
            or (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
        ):
            acc.append(char)
            stream.consume()
            char = stream.get_char()
            if char is None:
                if (acc[0] >= "a" and acc[0] <= "z") or (
                    acc[0] >= "A" and acc[0] <= "Z"
                ):
                    return Variable(acc[0])
                stream.colocar_posicion(orig_post)
                return None
            while (char >= "a" and char <= "z") or (
                char >= "A" and char <= "Z"
            ):
                acc.append(char)
                stream.consume()
                char = stream.get_char()
                if char is None:
                    break

            final_str = "".join(acc)
            if final_str == "_":
                return None
            elif final_str == "True":
                stream.colocar_posicion(orig_post)
                return None
            elif final_str == "False":
                stream.colocar_posicion(orig_post)
                return None
            return Variable("".join(acc))
        else:
            return None


def lexer_int(stream: Stream) -> Optional[Int]:  # buscador de enteros
    acc: list[str] = []
    orig_post = stream.get_posicion()
    num = stream.get_char()
    if num is None:
        stream.colocar_posicion(orig_post)
        return None
    else:
        if num == "-":
            acc.append(num)
            stream.consume()
            num = stream.get_char()
            if num is None:
                stream.colocar_posicion(orig_post)
                return None
            if is_digit(num):
                while is_digit(num):
                    acc.append(num)
                    stream.consume()
                    num = stream.get_char()
                    if num is None:
                        break
            else:
                stream.colocar_posicion(orig_post)
                return None
        elif is_digit(num):
            while is_digit(num):
                acc.append(num)
                stream.consume()
                num = stream.get_char()
                if num is None:
                    break
        else:
            stream.colocar_posicion(orig_post)
            return None
    return Int(int("".join(acc)))


def lexer_operator(
    stream: Stream,
) -> Optional[Operator]:  # buscador de operadores
    operator_symbols = [
        "+",
        "- ",
        "*",
        "/",
        "<=",
        ">=",
        "==",
        "<",
        ">",
        "&",
        "|",
        "~",
    ]  # compara  <=, >= antes que < e > para evitar errores
    for op in operator_symbols:
        lexer = reader_lexer(op, Operator(op))
        evaluation = lexer(stream)
        # print(stream.value, "comparado con", Operator(op), "es:",comparation)
        if evaluation is not None:
            # print("Se acabó")
            return evaluation
    return None


"""l = Stream("     <= 5")
l.colocar_posicion(5)
print(l.value, lexer_operator(l))
print("posición final:", l.get_posicion())"""

"""operador=["+", "- ", "*", "/", "<", ">", "<=", ">=", "==", "&", "|","~"]
for op in operador:
    print(op," es operador: ",lexer_operator(Stream(op)))"""

"""l = Stream("asaf <= 5")
print(l.value, lexer_operator(l))
print("posición final:", l.get_posicion())"""


def lexer_bool(
    stream: Stream,
) -> Optional[Bool]:  # buscador de variables booleanas
    lexerTrue = reader_lexer("True", Bool(True))
    evaluation = lexerTrue(stream)
    if evaluation is None:
        lexerFalse = reader_lexer("False", Bool(False))
        evaluation = lexerFalse(stream)
        return evaluation
    return evaluation

    # boolean_symbols=["True","False"]
    # for b in boolean_symbols:
    #    #print("****************************************************************")
    #    lexer = reader_lexer(b, Bool(bool(b)))
    #    #print("Se ejecutó identificador de lexer.")
    #    evaluation = lexer(stream)

    #    #comparation = (lexer(stream)  == Bool(bool(b)))
    #    #print("Se ejecutó lexer. Comparado con", Bool(bool(b)), "es:",comparation)
    #    #if comparation:
    #    #    return Bool(bool(b))


# l = Stream("False<= 5")
# print("Posición de origen:", l.get_posicion())
# print("Se encontró", lexer_bool(l),"en", l.value)
# print("posición final:", l.get_posicion())
# print(lexer_bool(l)==Bool(False))


def lexer_unit(  # buscador de expresiones unit
    stream: Stream,
) -> Optional[UnitExp]:
    lexer = reader_lexer("unit", UnitExp())
    return lexer(stream)


"""l = Stream("unit<= 5")
print("Posición de origen:", l.get_posicion())
print("Se encontró", lexer_unit(l),"en", l.value)
print("posición final:", l.get_posicion())"""


def lexer_leftP(  # buscador de apertura de paréntesis
    stream: Stream,
) -> Optional[LeftP]:
    lexer = reader_lexer("(", LeftP())
    return lexer(stream)


def lexer_rightP(  # buscador de cierre de paréntesis
    stream: Stream,
) -> Optional[RightP]:
    lexer = reader_lexer(")", RightP())
    return lexer(stream)


def lexer_arrowR(  # buscador de flechas
    stream: Stream,
) -> Optional[ArrowR]:
    lexer = reader_lexer("->", ArrowR())
    return lexer(stream)


def lexer_lineLambda(  # buscador de expresiones lambda
    stream: Stream,
) -> Optional[LineLambda]:
    lexer = reader_lexer("/", LineLambda())
    return lexer(stream)


# def lexer_twop(# buscador de ????
#     stream: Stream,
# ) -> Optional[Twop]:
#     lexer = reader_lexer("->", Twop())
#     return lexer(stream)


def lexer_if(  # buscador de if
    stream: Stream,
) -> Optional[If]:
    lexer = reader_lexer("if", If())
    return lexer(stream)


def lexer_then(  # buscador de Then
    stream: Stream,
) -> Optional[Then]:
    lexer = reader_lexer("then", Then())
    return lexer(stream)

def lexer_else(  # buscador de Then
    stream: Stream,
) -> Optional[Then]:
    lexer = reader_lexer("else", Then())
    return lexer(stream)

def lexer_equals(  # buscador de =
    stream: Stream,
) -> Optional[Equals]:
    lexer = reader_lexer("=", Equals())
    return lexer(stream)


"""Lexer de tipos"""
def lexer_int_type(stream: Stream) -> Optional[IntType]:
    lexer = reader_lexer("Int", IntType())
    return lexer(stream)


def lexer_bool_type(stream: Stream) -> Optional[BoolType]:
    lexer = reader_lexer("Bool", BoolType())
    return lexer(stream)


def lexer_unit_type(stream: Stream) -> Optional[UnitType]:
    lexer = reader_lexer("Unit", UnitType())
    return lexer(stream)

def lexer_twoP(stream: Stream) -> Optional[TwoP]:
    lexer = reader_lexer(":", TwoP())
    return lexer(stream)

def lexer_space(stream: Stream) -> Optional[bool]:
    lexer = reader_lexer(" ", True)
    return lexer(stream)

def lexer_spaces(stream: Stream) -> None:
    while True:
        space = lexer_space(stream)
        if space is None:
            break

# stream = Stream('   -15')
# lexer_spaces(stream)
# print(var.get_char())


def lexer_literal(stream: Stream)->Optional[Int | Bool | UnitExp]:  #Saca los tipos considerados literal
    original_position = stream.get_posicion()
    token_lexer_list = [lexer_int, lexer_bool, lexer_unit]
    for lexer in token_lexer_list:
        value = lexer(stream)
        if value is not None:
            return value
    return None


def lexer_token(stream: Stream) -> Optional[Token]:
    lexer_list: Sequence[Callable[[Stream], Optional[Token]]] = [
        lexer_leftP,
        lexer_int_type,
        lexer_bool_type,
        lexer_unit_type,
        lexer_lineLambda,
        lexer_literal,
        lexer_if,
        lexer_variable,
        lexer_operator,
        lexer_twoP,
        lexer_arrowR,
        lexer_then,
        lexer_else,
        lexer_equals,
        lexer_literal,
        lexer_rightP,
    ]
    lexer_spaces(stream)
    original_position = stream.get_posicion()
    if stream.get_char() is None:
        return None
    for lexer_function in lexer_list:
        value = lexer_function(stream)
        if value is not None:
            return value
    return TokenError(original_position)

# stream = Stream('   -15')
# print(lexer_token(stream))

def lexer(stream:Stream) -> list[Token]:
    tokens_list:list[Token]=[]
    last_token=None
    while True:
        token = lexer_token(stream)
        if token is None: 
            return tokens_list
        elif isinstance(token,TokenError):
            tokens_list.append(token)
            return tokens_list
        tokens_list.append(token)
        
# stream = Stream('( True -> False)')
# print(lexer(stream))