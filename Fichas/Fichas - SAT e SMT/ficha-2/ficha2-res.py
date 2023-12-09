# METODOS FORMAIS DE ENGENHARIA DE SOFTWARE
# FICHA 2

from z3 import *

# ------------------------------------------------------- EXERCICIO 1 -------------------------------------------------------

"""
Configuração de computadores

Uma loja de electrónica permite aos seus clientes personalizar o seu computador, escolhendo entre dois modelos de CPU, dois modelos de placa gráfica, dois modelos de memória RAM, 
dois modelos de motherboards e dois modelos de monitor. Cada computador tem que ter obrigatorimente uma única motherboard, um único CPU, uma única placa gráfica e uma única 
memória RAM. O computador poderá ter ou não ter monitor.
A personalização do computador deverá obedecer às seguintas regras:

    1. A motherboard MB1 quando combinada com a placa gráfica PG1, obriga à utilização da RAM1.
    2. A placa grágica PG1 precisa do CPU1, excepto quando combinada com uma memória RAM2.
    3. O CPU2 só pode ser instalado na motherboard MB2.
    4. O monitor MON1 para poder funcionar precisa da placa gráfica PG1 e da memória RAM2.

Codifique o problema num SAT solver e comprove que o conjunto de regras é consistente.
"""

def solve1():

    CPU1, CPU2 = Bools("CPU1 CPU2")
    PG1, PG2 = Bools("PG1 PG2")
    RAM1, RAM2 = Bools("RAM1 RAM2")
    MB1, MB2 = Bools("MB1 MB2")
    MON1, MON2 = Bools("MON1 MON2")

    s = Solver()

    # Um e um só CPU, PG, RAM e MB
    s.add(Or(CPU1,CPU2))
    s.add(Implies(CPU1,Not(CPU2)))

    # Um e um só PG
    s.add(Or(PG1,PG2))
    s.add(Implies(PG1,Not(PG2)))

    # Um e um só RAM
    s.add(Or(RAM1,RAM2))
    s.add(Implies(RAM1,Not(RAM2)))

    # Um e um só MB
    s.add(Or(MB1,MB2))
    s.add(Implies(MB1,Not(MB2)))

    # A motherboard MB1 quando combinada com a placa gráfica PG1, obriga à utilização da RAM1
    re1 = And(MB1, PG1)
    s.add(Implies(re1, RAM1))

    # A placa grágica PG1 precisa do CPU1, excepto quando combinada com uma memória RAM2
    re2 = And(PG1, Not(RAM2))
    s.add(Implies(re2, CPU1))

    # O CPU2 só pode ser instalado na motherboard MB2
    s.add(Implies(CPU2, MB2))

    # O monitor MON1 para poder funcionar precisa da placa gráfica PG1 e da memória RAM2
    re3 = And(PG1, RAM2)
    s.add(Implies(MON1, re3))
    
    s.push()

    if s.check() == sat:
        print("O conjunto de regras é consistente.")
        print("\n")

        print("O monitor MON1 só poderá ser usado com uma motherboard MB1 ?")

        re4 = Implies(MON1, MB1)
        s.add(re4)

        if s.check() == sat:
            print("É verdade!")
            print("\n")
        else:
            print("É falso!")
            print("\n")
            

        print("Um cliente pode personalizar o seu computador da seguinte forma: ")
        print("  - uma motherboard MB2, o CPU1, a placa gráfica PG2 e a memória RAM1 ?")
        
        re5 = And(MB2, CPU1, PG2, RAM1)
        s.add(re5)

        if s.check() == sat:
            print("É verdade!")
            print("\n")
        else:
            print("É falso!")
            print("\n")

    else:
        print("O conjunto de regras é inconsistente.")



# ------------------------------------------------------- EXERCICIO 3 -------------------------------------------------------

"""
Alocação de aulas

Num curso de formação temos 5 aulas consecutivas e temos 3 formadores (a Ana, a Beatriz e o Carlos) capazes de dar qualquer aula. Queremos alocar os formadores à diversas aulas, obedecendo às seguintes restrições:

    1. O Carlos não pode dar a primeira aula.
    2. Se a Beatriz der a primeira aula, não poderá dar a última.
    3. Cada aula tem pelo menos um formador.
    4. As quatro primeiras aulas têm no máximo um formador.
    5. A última aula pode ter no máximo dois formadores.
    6. Nenhum formador pode dar 4 aulas consecutivas.

Pretende-se que escreva um programa Python que, usando o Z3 como SAT solver, faça a distribuição das formadores pelas aulas.
"""

def solve3():

    formadores = ["Ana","Beatriz","Carlos"]
    aulas = [1,2,3,4,5]

    x = {}
    for f in formadores:
        x[f] = {}
        for a in aulas:
            x[f][a] = Bool("%s,%d" % (f,a))

    s = Solver()

    # O Carlos não pode dar a primeira aula.
    s.add(Not(x["Carlos"][1]))

    # Se a Beatriz der a primeira aula, não poderá dar a última.
    s.add(Implies(x["Beatriz"][1], Not(x["Beatriz"][5])))

    # Cada aula tem pelo menos um formador.
    for a in aulas:
        s.add(Or(x["Ana"][a], x["Beatriz"][a], x["Carlos"][a]))

    # As quatro primeiras aulas têm no máximo um formador.
    for i in range(1, 5):
        re1 = Implies(x["Ana"][a], And(Not(x["Beatriz"][a]), Not(x["Carlos"][a])))
        re2 = Implies(x["Beatriz"][a],Not(x["Carlos"][a]))
        s.add(And(re1, re2))

    # A última aula pode ter no máximo dois formadores.
    re3 = And(x["Ana"][5], x["Beatriz"][5], x["Carlos"][5])
    s.add(Not(re3))

    # Nenhum formador pode dar 4 aulas consecutivas.
    for f in formadores:
        re4 = Implies(And(x[f][1], x[f][2], x[f][3]), Not(x[f][4]))
        re5 = Implies(And(x[f][3], x[f][4], x[f][5]), Not(x[f][2]))
        s.add(And(re4, re5))

    s.push()

    if s.check() == sat:
        m = s.model()
        for f in formadores:
            for a in aulas:
                if is_true(m[x[f][a]]):
                    print("%s leciona a aula %d" % (f,a))
    else:
        print("Não tem solução.")


# ------------------------------------------- MAIN -------------------------------------------


if __name__ == '__main__':

    print("--------------")
    print("MFES - FICHA 2")
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
            solve3()

        if(escolha == "4"):
            print("INDISPONIVEL")

        escolha = input(">> ")

    print("ENCERRANDO...")


