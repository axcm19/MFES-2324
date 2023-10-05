# METODOS FORMAIS DE ENGENHARIA DE SOFTWARE
# FICHA 3

from z3 import *

# ------------------------------------------------------- EXERCICIO 1 -------------------------------------------------------

"""
O Cryptarithms é um jogo que consiste numa equação matemática entre números desconhecidos, cujos dígitos são representados
por letras. Cada letra deve representar um dígito diferente e o dígito inicial de um número com vários dígitos não deve ser
zero.

Use o Z3 para o ajudar a descobrir os dígitos a que correspondem as letras envolvidas na seguinte equação: 

SEND + MORE = MONEY

Sugestão: Escreva diretamente a equação, representado cada parcela por uma expressão aritmétrica onde cada letra é 
multiplicada pelo seu "peso especíco" em base 10.

Confirme que só existe uma solução para este puzzle.
"""

def solve1():

    S, E, N, D, M, O, R, Y = Ints("S E N D M O R Y")

    s = Solver()

    # Regras
    s.add(And(0<=S, S<=9))
    s.add(And(0<=E, E<=9))
    s.add(And(0<=N, N<=9))
    s.add(And(0<=D, D<=9))
    s.add(And(0<=M, M<=9))
    s.add(And(0<=O, O<=9))
    s.add(And(0<=R, R<=9))
    s.add(And(0<=Y, Y<=9))
    
    s.push()

    if s.check() == sat :
        m = s.model()
        print("O conjunto de regras é consistente.")
        print(m)
        for d in m.decls():
            print("%s = %d" % (d.name(), m[d].as_long()))


    else:
        print("O conjunto de regras é inconsistente.")

    s.push()

    i = 0
    vars = [S, E, N, D, M, O, R, Y]

    while s.check() == sat:
        i += 1
        m = s.model()
        print(m)
        s.add(Or([x != m[x] for x in vars]))
        print("\n")

    print("Numero de soluções: ",i)

    s.pop()



# ------------------------------------------------------- EXERCICIO 2 -------------------------------------------------------

"""

"""

def solve2():

    

    s = Solver()

    # Regras
    s.add()
    
    s.push()

    if s.check() == sat :
        m = s.model()
        print("O conjunto de regras é consistente.")
        print(m)
        for d in m.decls():
            print("%s = %d" % (d.name(), m[d].as_long()))


    else:
        print("O conjunto de regras é inconsistente.")

    


# ------------------------------------------- MAIN -------------------------------------------


if __name__ == '__main__':

    print("--------------")
    print("MFES - FICHA 3")
    print("--------------")
    print("Qual exercicio (1,2,3,4) quer correr?")
    print("0 - encerrar")

    escolha = input(">> ")

    while escolha != "0":

        if(escolha == "1"):
            solve1()

        if(escolha == "2"):
            print("INDISPONIVEL")

        if(escolha == "3"):
            print("INDISPONIVEL")

        if(escolha == "4"):
            print("INDISPONIVEL")

        escolha = input(">> ")

    print("ENCERRANDO...")

