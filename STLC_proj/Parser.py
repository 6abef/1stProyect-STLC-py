from typing import Optional, Union, TypeVar, Callable
from STLC_proj.Lexer import lexer, Stream, Token, Variable, Int, Bool, UnitExp, LeftP, RightP, Operator, TokenError
from dataclasses import dataclass

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


@dataclass
class TokensList:
    value: list
    pos: int

    def __init__( self, value:str ):
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

    def colcar_posicion(self, new_pos):
        self.pos = new_pos



def parser_expression_variable(tokensList: TokensList) -> Optional[ExpressionVariable]:
    position = tokensList.get_posicion()
    token = tokensList.get_token()
    
    if isinstance(token , Variable):
        tokensList.consume()
        return ExpressionVariable(token.name)
    elif isinstance(token,TokenError):
        tokensList.colcar_posicion(position)
        return ExpressionError(token.error)
    else:
        return None
          
# print(parser_expression_variable(  TokensList( [ Variable('hola') ,  Variable("Wai") ] )   )  )
# print(parser_expression_variable(TokensList([TokenError(4)])))
# print(parser_expression_variable(TokensList([Int(4)])))

def parser_expression_literal(tokensList:TokensList) -> Optional[ExpressionLiteral]:
    position = tokensList.get_posicion()
    token = tokensList.get_token()
    
    if isinstance(token , Int) or isinstance(token , Bool) or isinstance(token , UnitExp):
        tokensList.consume()
        return ExpressionLiteral(token)
    
    elif isinstance(token,TokenError):
        tokensList.colcar_posicion(position)
        return ExpressionError(token.error)
    
    else:
        tokensList.colcar_posicion(position)
        return None

# # print(parser_expression_literal([UnitExp()]))

# def parser_expression_Operator(tokensList:TokensList)->Optional[ExpressionApplication]:
#     if isinstance(tokensList.value[0], Operator):
#         tokensList.consume()
#         return ExpressionOperator(tokensList.value[0])
#     return None

# # print(parser_expression_Operator([LeftP(), Int(5), Operator('+'), Int(12), RightP()]))
    
# def parser_expression_Operation(tokensList:TokensList) -> Optional[ExpressionOperation]:
#     original_position = tokensList.get_posicion()
    
#     if (tokensList is not None) and (tokensList != []):
#         if isinstance(tokensList[0], LeftP):
#             if isinstance(parser_expression(tokensList[1:], Expression)):
#                 pass
#             else:
#                 return None
#         else:
#             return None
#     else:
#         return None 

# print(parser_expression_Operation([LeftP(), Int(5), Operator('+'), Int(12), RightP()]))

# # def parser_expression_application(tokensList:[Token])->Optional[ExpressionApplication]:
# #     if (tokensList is not None) and (tokensList != []):
# #         if isinstance(tokensList[0], LeftP):
# #             if isinstance(tokensList[-1], RightP):
# #                 reader = tokensList[1:-1]
# #                 print(reader)  
# #                 parser_list =[parser_expression_variable, parser_expression_literal,parser_expression_application ,parser_expression_lambda, parser_expression_operation, parser_expression_if, parser_expression_type, parser_expression_declaration]  
# #                 for parser in parser_list:
# #                      expression = parser(reader)
                     
# #                      if isinstance(expression, )
# #                 return ExpressionVariable(tokensList[0])
# #         else:
# #             return None
# #     else:
# #         return None 

# # samplelist = [LeftP(),LeftP(),Int(5),Variable('x'),RightP(), LeftP(),Int(8),RightP(), RightP()]
# # parser_expression_application(samplelist)

# def parser_expression(tokenslist:list[Token]) -> Optional[Expression]:
#     parser_list =[parser_expression_variable, parser_expression_literal, parser_expression_application ,parser_expression_lambda, parser_expression_operation, parser_expression_if, parser_expression_type, parser_expression_declaration]  
#     for parser in parser_list:
#             expression = parser(tokenslist)
#             if isinstance(expression, ExpressionVariable):
#                 return ExpressionVariable(tokensList[0])
#             else:  
#                 return None