from typing import Optional, Union, TypeVar, Callable
from dataclasses import dataclass
from STLC_proj.Lexer import lexer, Stream, Token, Variable, Int, Bool, UnitExp, LeftP, RightP, Operator, TokenError


#*************************************************************
#                 Declaración de expresiones
#*************************************************************
Expression = Union[
    "ExpressionVariable",
    "ExpressionLiteral",
    "ExpressionApplication",
    "ExpressionLambda",
    "ExpressionOperator",
    "ExpressionIf",
    "ExpressionDeclaration",
]


@dataclass
class ExpressionVariable:
    name: str


@dataclass
class ExpressionLiteral:
    token: Token


@dataclass
class ExpressionApplication:
    leftElement: Expression
    rightElement: Expression


@dataclass
class ExpressionLambda:
    variable: ExpressionVariable
    function: Expression


@dataclass
class ExpressionOperator:
    operatorToken: Token


@dataclass
class ExpressionOperation:
    leftElement: Expression
    operator: ExpressionOperator
    rightElement: Expression


@dataclass
class ExpressionIf:
    ifExpression: Expression
    thenExpression: Expression
    elseExpression: Expression


@dataclass
class ExpressionType:
    expression: Expression


@dataclass
class ExpressionDeclaration:
    expression: Expression
    type: ExpressionType
    
@dataclass
class ExpressionError:
    name: str


#*************************************************************
#                 Clase: lector de lista de tokens
#*************************************************************
@dataclass
class TokensList:
    value: list
    pos: int

    def __init__( self, value:list ):
        self.pos = 0
        self.value = value

    def get_token(self) -> Optional[Token]:
        if len(self.value) > self.pos:
            return self.value[self.pos]
        else:
            return None

    def consume(self):
        self.pos += 1

    def get_posicion(self):
        return self.pos

    def colocar_posicion(self, new_pos):
        self.pos = new_pos



#*****************************************************************************************
#   Declaración de operadores bind(combinador de parsers) y pure (inyector de resultantes)
#*****************************************************************************************
T = TypeVar("T")
T2 = TypeVar("T2")

ParserResult = Union[ExpressionError, tuple[Int, T]] # en caso de aplicarse el parser, retorna e sufijo de la posición y el resultado previo
Parser = Callable[[TokensList], ParserResult[T]]



def bind(parser : Parser[T], transformation: Callable[[T], Parser[T2]]) -> Parser[T2]:
    """Esta función toma un parser tipo T y un parser aplicable a algo tipo T para obtener el segundo parser para otro tipo"""
    
    def new_parser(tokensList: TokensList) -> ParserResult[T2]:
        """Función del segundo parser sobre un elemento de tipo T"""
        originalPosition = tokensList.get_posicion()
        parserResult = parser(tokensList)
        
        if isinstance(parserResult, ExpressionError):
            tokensList.colocar_posicion(originalPosition)
            return parserResult
        else: 
            (newPosition, value1) = parserResult
            tokensList.colocar_posicion(newPosition)
            otherParser = transformation(value1)
            return otherParser(tokensList)     
    return new_parser        


def pure(result:T) ->Parser[T]:
    return lambda tokensList: (tokensList, result)


def parser_expression_variable(tokensList: TokensList) -> ParserResult[ExpressionVariable]:
    originalPosition = tokensList.get_posicion()
    token = tokensList.get_token()
    
    match token:
        case Variable(name = name): # Revisar patternmatch + python!!!
            tokensList.consume()
            return (tokensList.get_posicion(), ExpressionVariable(token.name))
        case _:
            tokensList.colocar_posicion(originalPosition)
            return ExpressionError(f"No es posible identificar una variable en {token}")

def parser_expression_literal(tokensList: TokensList) -> ParserResult[ExpressionLiteral]:
    """Parser para identificar expresiones de una literal(Int, Bool o UnitExp) en una tokenList o regresa None"""
    originalPosition = tokensList.get_posicion()
    token = tokensList.get_token()
    
    match token:
        case Int() | Bool() | UnitExp():
            tokensList.consume()
            return (tokensList.get_posicion(), ExpressionLiteral(token))
        case _:
            tokensList.colocar_posicion(originalPosition)
            return ExpressionError(f"No es posible identificar una literal en {token}")
 
def parser_expression_operator(tokensList: TokensList) -> ParserResult[ExpressionOperator]:
    """Parser para identificar operadores en una tokenList o regresa None"""
    originalPosition = tokensList.get_posicion()
    token = tokensList.get_token()
    
    match token:
        case Operator():
            tokensList.consume()
            return (tokensList.get_posicion(), ExpressionOperator(token))
        case _:
            tokensList.colocar_posicion(originalPosition)
            return ExpressionError(f"No es posible identificar un operador en {token}")
        
def parser_expression_operation(tokensList: TokensList) -> ParserResult[ExpressionOperation]:
    """Parser para identificar expresiones tipo operación en una tokenList o regresa None"""
    originalPosition = tokensList.get_posicion()
    token = tokensList.get_token()
    
    match token:
        case Operator():
            tokensList.consume()
            return (tokensList.get_posicion(), ExpressionOperator(token))
        case _:
            tokensList.colocar_posicion(originalPosition)
            return ExpressionError(f"No es posible identificar una aplicación en {token}")  
        
              

# def parser_expression_Operation(tokensList:TokensList) -> Optional[ExpressionOperation]:
#     """Parser para identificar expresiones tipo operación en una tokenList o regresa None"""
#     original_position = tokensList.get_posicion()
#     if (tokensList is not None) and (tokensList != []):
#         token = tokensList.get_token()
#         if isinstance(token, LeftP):
#             tokensList.consume()
#             token = tokensList.get_token()
#             if isinstance(parser_expression_Operator(token, Expression)):
#                 operator = token
#                 token =
#             else:
#                 return None
#         else:
#             return None
#     else:
#         return None 

# # print(parser_expression_Operation([LeftP(), Int(5), Operator('+'), Int(12), RightP()]))

# def parser_expression_application(tokensList:[Token])->Optional[ExpressionApplication]:
#     if (tokensList is not None) and (tokensList != []):
#         if isinstance(tokensList[0], LeftP):
#             if isinstance(tokensList[-1], RightP):
#                  reader = tokensList[1:-1]
#                  print(reader)  
#                  parser_list =[parser_expression_variable, parser_expression_literal,parser_expression_application]# ,parser_expression_lambda, parser_expression_operation, parser_expression_if, parser_expression_type, parser_expression_declaration]  
#                  for parser in parser_list:
#                       expression = parser(reader)
                     
#                       if isinstance(expression, )
#                  return ExpressionVariable(tokensList[0])
#             else:
#              return None
#     else:
#          return None 

# # # samplelist = [LeftP(),LeftP(),Int(5),Variable('x'),RightP(), LeftP(),Int(8),RightP(), RightP()]
# # # parser_expression_application(samplelist)

# def parser_expression(tokenslist:list[Token]) -> Optional[Expression]:
#     parser_list =[parser_expression_variable, parser_expression_literal, parser_expression_application]# ,parser_expression_lambda, parser_expression_operation, parser_expression_if, parser_expression_type, parser_expression_declaration]  
#     for parser in parser_list:
#             expression = parser(tokenslist)
#             if isinstance(expression, ExpressionVariable):
#                 return expression
#             else:  
#                 return None