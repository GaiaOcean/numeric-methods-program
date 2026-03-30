import sympy as sp
import methods

if __name__ == "__main__":
    # Entrada do intervalo: alterado para sympify para aceitar 'pi' e 'e' como limites
    entrada_intervalo = input("Digite o Intervalo(e.g 1 2 ou 0 pi): ").split()
    a = float(sp.sympify(entrada_intervalo[0], locals={'pi': sp.pi, 'e': sp.E}))
    b = float(sp.sympify(entrada_intervalo[1], locals={'pi': sp.pi, 'e': sp.E}))
    
    num_trapezios = int(input("Digite o número de trapezios (n): "))
    num_casas_decimais = int(input("Digite o número de casas decimais (casas): "))
    funcao = input("Digite a função: ") # No estilo do python
    print()
    
    passo = methods.calcularPasso(a, b, num_trapezios)
    print(f"Passo (h) = {passo}\n")

    # RESOLUÇÃO TODO: Reconhecer constantes e diferenciar ln de log (base 10)
    f = sp.sympify(funcao, locals={
        'e': sp.E, 
        'pi': sp.pi, 
        'ln': sp.log,               # ln(x) interpreta como logaritmo natural
        'log': lambda x: sp.log(x, 10) # log(x) interpreta como base 10
    })

    # Chamadas das funções do methods.py com os parâmetros sincronizados
    soma = methods.calcularSomatorio(funcao, f, a, b, num_trapezios, num_casas_decimais)
    print()
    area = methods.calcularAreaTrapezio(a, b, soma, num_casas_decimais, num_trapezios)
    print()
    erro_arredondamento = methods.calcularErroDeArredondamento(a, b, num_trapezios, num_casas_decimais)
    print()
    # Ajustado para os 6 parâmetros definidos no methods.py
    max_segunda_derivada = methods.maxSegundaDerivada(funcao, f, a, b, passo, num_trapezios)
    print()
    erro_truncamento = methods.calcularErroDeTruncamento(passo, num_casas_decimais, max_segunda_derivada, num_trapezios)
    print()
    erro_total = methods.calcularErroTotal(erro_truncamento, erro_arredondamento, num_casas_decimais)
    print()
    methods.respostaFinal(funcao, f, a, b, area, num_casas_decimais, erro_total)