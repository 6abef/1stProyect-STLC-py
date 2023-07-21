# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:10:34 2023

@author: Moisés
Definición de clases
"""
from dataclasses import dataclass
from typing import Union, Optional


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
    "Twop",
    "UnitType",
    "UnitExp",
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
class TokenError:
    error: str


@dataclass
class LeftP:
    pass


@dataclass
class RightP:
    pass


@dataclass
class ArrowR:
    pass


@dataclass
class LineLambda:
    pass


@dataclass
class Twop:
    pass


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

    def colcar_posicion(self, new_pos):
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


def is_operator(string: str) -> bool:
    # Verifica que sea operador
    if len(string) > 0:
        operator = string[0]
        if (
            operator == "+"
            or operator == "-"
            or operator == "*"
            or operator == "/"
            or operator == "<"
            or operator == ">"
            or operator == "="  # Para verificar una igualdad en bool
            or operator == "&"
            or operator == "|"
            or operator == "~"
        ):
            return True
    return False


def lexer_variable(stream: Stream) -> Optional[Variable]:
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
                stream.colcar_posicion(orig_post)
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
                stream.colcar_posicion(orig_post)
                return None
            elif final_str == "False":
                stream.colcar_posicion(orig_post)
                return None
            return Variable("".join(acc))
        else:
            return None


#print(lexer_variable(Stream("_augiugk$b")))
print("Prueba lexer_variable: ")
#s = Stream("_")
#print(lexer_variable(s),s.get_posicion())

#s = Stream("_variable")
#lex_var =lexer_variable(s)
#if lex_var is not None:
#    print(len(lex_var.name),s.get_posicion())


def lexer_int(stream: Stream) -> Optional[Int]:
    acc: list[str] = []
    orig_post = stream.get_posicion()
    num = stream.get_char()
    if num is None:
        stream.colcar_posicion(orig_post)
        return None
    else:
        if num == "-":
            acc.append(num)
            stream.consume()
            num = stream.get_char()
            if num is None:
                stream.colcar_posicion(orig_post)
                return None
            if is_digit(num):
                while is_digit(num):
                    acc.append(num)
                    stream.consume()
                    num = stream.get_char()
                    if num is None:
                        break
            else:
                stream.colcar_posicion(orig_post)
                return None
        elif is_digit(num):
            while is_digit(num):
                acc.append(num)
                stream.consume()
                num = stream.get_char()
                if num is None:
                    break
            stream.colcar_posicion(orig_post)
        else:
            stream.colcar_posicion(orig_post)
            return None
    return Int(int("".join(acc)))


"""            
print(lexer_int(Stream("-121+3-4"))) 
        
b = Stream("_fgsfds-56365")
print(b,"b")
t = lexer_int(b)
print(b,"b")
print(t,"t")
p =lexer_variable(b)
print(p,"p")
print(b,"b")
"""


def lexer_operator(stream: Stream) -> Optional[Operator]:
    orig_post = stream.get_posicion()
    char = stream.get_char()
    if char is None:
        return None
    if is_operator(char):
        match char:
            case "-":
                stream.consume()
                next_char = stream.get_char()
                if next_char is None:
                    return Operator(char)
                if is_digit(next_char):
                    stream.colcar_posicion(orig_post)
                    return None
                return Operator(char)
            case "<":
                stream.consume()
                next_char = stream.get_char()
                if next_char is None:
                    return Operator(char)
                if next_char == "=":
                    stream.colcar_posicion(orig_post)
                    return Operator(char + next_char)
                if next_char == " " or is_digit(next_char):
                    stream.colcar_posicion(orig_post)
                    return Operator(char)
                return Operator(char)
            case ">":
                stream.consume()
                next_char = stream.get_char()
                if next_char is None:
                    return Operator(char)
                if next_char == "=":
                    return Operator(char + next_char)
                if next_char == " " or is_digit(next_char):
                    return Operator(char)
                return Operator(char)
            case "=":
                stream.consume()
                next_char = stream.get_char()
                if next_char is None:
                    return Operator(char)
                if next_char == "=":
                    return Operator(char + next_char)
                if next_char == " " or is_digit(next_char):
                    stream.colcar_posicion(orig_post)
                    return None
                return Operator(char)
            case _:
                return Operator(char)
        return Operator(char)
    else:
        return None


"""operadores=["+", "-", "*", "/", "<", ">", "<=", ">=", "==", "&", "|","~"]
for op in operadores:
    print(op," es operador: ",lexer_operator(Stream(op)))"""


def lexer_bool(stream: Stream) -> Optional[Bool]:
    acc: list[str] = []
    orig_post = stream.get_posicion()
    char = stream.get_char()
    if char is None:
        return None
    else:
        if (char == "T") or (char == "F"):
            acc.append(char)
            stream.consume()
            char = stream.get_char()
            if char is None:
                stream.colcar_posicion(orig_post)
                return None
            while char >= "a" and char <= "z":
                acc.append(char)
                stream.consume()
                char = stream.get_char()
                if char is None:
                    break
            final_str = "".join(acc)

            if (
                final_str == "True"
            ):  # identifica que la cadena corresponda a la variable Booleana True o False
                return Bool(True)
            elif final_str == "False":
                return Bool(False)

            return None
        else:
            return None


def lexer_unit(stream: Stream) -> Optional[UnitExp]:
    pass
