
import sympy as sp
import methods
 
if __name__ == "__main__":
    a,b = map(int, input("Digite o Intervalo(e.g 1 2): ").split()) #sempre digite usando um espaco entre os digitos
    num_trapezios = int(input("Digite o número de trapezios (n): "))
    num_casas_decimais = int(input("Digite o número de casas decimais (casas): "))
    funcao = input("Digite a função: ") #no style do python
    print()
    passo = methods.calcularPasso(a,b,num_trapezios)
    print(f"Passo (h) = {passo}\n")

    x = sp.symbols('x') # X da matematica
    f = sp.sympify(funcao)

    soma = methods.calcularSomatorio(f,a,b,num_trapezios,num_casas_decimais)
    print()
    area = methods.calcularAreaTrapezio(a,b,soma,num_casas_decimais,num_trapezios)
    print()
    erro_arredondamento = methods.calcularErroDeArredondamento(a,b,num_trapezios,num_casas_decimais)
    print()
    max_segunda_derivada = methods.maxSegundaDerivada(f,a,b,passo,num_casas_decimais,num_trapezios)
    print()
    erro_truncamento = methods.calcularErroDeTruncamento(passo,num_casas_decimais,max_segunda_derivada,num_trapezios)
    print()
    erro_total = methods.calcularErroTotal(erro_truncamento, erro_arredondamento,num_casas_decimais)
    print()
    intervalo_final = methods.respostaFinal(f,a,b,area,num_casas_decimais,erro_total)
