from STLC_proj.Lexer import lexer, Stream
from colorama import Fore, Back, Style

def read_from_terminal()-> None:
    while True: 
        stream = input(Fore.BLUE+"~")           
        tokens_id=lexer(Stream(stream))
        if tokens_id is not None:
            if tokens_id != []:
                print(Fore.LIGHTBLUE_EX+str(tokens_id)+"\n")
read_from_terminal()