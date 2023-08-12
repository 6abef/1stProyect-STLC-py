"""
Este archivo presenta las pruebas en pytest para los parser del proyecto    
"""
from typing import Optional, TypeVar, Callable
from STLC_proj.Parser import (
    parser_expression_variable,
    parser_expression_literal,
    ExpressionVariable,
    ExpressionLiteral,
    ExpressionApplication,
    ExpressionLambda,
    ExpressionOperator,
    ExpressionIf,
    ExpressionDeclaration,
    ExpressionError,
    Expression,
    TokensList,
)

from STLC_proj.Lexer import Variable, TokenError, Int, Bool, UnitExp

import pytest

T = TypeVar("T")


def make_positive_test(
    parser: Callable[[TokensList], Optional[T]],
    tokensList: TokensList,
    expected: Expression,
):
    expression = parser(tokensList)
    assert expression == expected


def make_negative_test(
    parser: Callable[[TokensList], Optional[T]], tokensList: TokensList
):
    expression = parser(tokensList)
    assert expression == None


def make_positive_position_test(
    parser: Callable[[TokensList], Optional[T]],
    tokensList: TokensList,
    expectedposition: Int,
):
    expression = parser(tokensList)
    position = tokensList.get_posicion()
    assert position == expectedposition


def make_negative_position_test(
    parser: Callable[[TokensList], Optional[T]], tokensList: TokensList
):
    original_position = tokensList.get_posicion()
    print('\nOriginalmente en:', original_position)
    expression = parser(tokensList)
    position = tokensList.get_posicion()
    print('\nFinalmente en:', position)
    assert position == original_position


"""
********************************   Tests parser Variable ********************************************
"""


@pytest.mark.parametrize(
    "tokensList,expected",
    [
        (
            TokensList([Variable("hola")]),
            ExpressionVariable("hola"),
        ),  # Prueba variables y tokenError
        (TokensList([TokenError("5")]), ExpressionError("5")),
    ],
)
def test_positive_parser_variable(tokensList: TokensList, expected: Variable):
    make_positive_test(parser_expression_variable, tokensList, expected)


@pytest.mark.parametrize(
    "tokensList",
    [
        (TokensList([Int(4)])),  # Prueba literales
        (TokensList([Bool(False)])),
        (TokensList([UnitExp()])),
    ],
)
def test_negative_parser_variable(tokensList: TokensList):
    make_negative_test(parser_expression_variable, tokensList)


@pytest.mark.parametrize(
    "tokensList",
    [
        TokensList([Variable("hola")]),
    ],
)
def test_positive_parser_variable(tokensList: TokensList):
    make_positive_position_test(parser_expression_variable, tokensList, 1)


@pytest.mark.parametrize(
    "tokensList",
    [
        TokensList([Int(4)]),  # Prueba literales
        TokensList([Bool(False)]),
        TokensList([UnitExp()]),
        TokensList([TokenError("5")]),
    ],
)
def test_negative_parser_variable(tokensList: TokensList):
    make_negative_position_test(parser_expression_variable, tokensList)


"""
***********************************   Tests parser Literal ****************************************
"""


@pytest.mark.parametrize(
    "tokensList, expected",
    [
        (TokensList([Int(4)]), ExpressionLiteral(Int(4))),
        (TokensList([Bool(False)]), ExpressionLiteral(Bool(False))),
        (TokensList([UnitExp()]), ExpressionLiteral(UnitExp())),
        (TokensList([TokenError("6")]), ExpressionError("6")),
    ],
)
def test_positive_parser_literal(tokensList: TokensList, expected: Variable):
    make_positive_test(parser_expression_literal, tokensList, expected)


@pytest.mark.parametrize(
    "tokensList",
    [(TokensList([Variable("hola")]))],
)
def test_negative_parser_literal(tokensList: TokensList):
    make_negative_test(parser_expression_literal, tokensList)


@pytest.mark.parametrize(
    "tokensList",
    [TokensList([Int(4)]), TokensList([Bool(False)]), TokensList([UnitExp()])],
)
def test_positive_position_parser_literal(tokensList: TokensList):
    make_positive_position_test(parser_expression_literal, tokensList, 1)


@pytest.mark.parametrize(
    "tokensList",
    [
        TokensList([Variable("vaR")]),  # Prueba literales
        TokensList([TokenError("5")]),
    ],
)
def test_negative_position_parser_literal(tokensList: TokensList):
    make_negative_position_test(parser_expression_variable, tokensList)
