
import sympy as sp

def calcularPasso(a:int, b:int, num_trapezios:int) -> float: #tambem é a altura do trapezio
    return (b - a) / num_trapezios

def criarTabela(funcao,a:int, b:int,num_trapezios:int, casas_decimais:int) -> list:
    passo = calcularPasso(a,b,num_trapezios)
    logs = funcao.atoms(sp.log)
    lista_dos_resultados = list()

    for log_expr in logs:
        if len(log_expr.args) == 1:  # nenhuma base especifica
            x_arg = log_expr.args[0]
            funcao = funcao.subs(log_expr, sp.log(x_arg, 10))

    var = list(funcao.free_symbols)[0]
    math_function = sp.lambdify(var,funcao)
    

    while a <= b:
       resultado = math_function(a)
       print(f"{a:.1f}\t  {resultado:.{casas_decimais}f}")
       lista_dos_resultados.append(resultado)
       a += passo

    return lista_dos_resultados


def calcularSomatorio(funcao,a:int, b:int,num_trapezios:int, casas_decimais:int)->float:
    resultados = criarTabela(funcao,a,b,num_trapezios,casas_decimais)
    n = len(resultados)
    soma = 0

    for i in range(0,n):
        if i == 0 or i == n-1:
            soma += resultados[i]/2
        else:
            soma += resultados[i]
    print(f"∑ = {soma:.{casas_decimais}f}")

    return soma

def calcularAreaTrapezio(a,b,soma:float,casas_decimais:int,num_trapezios:int) -> float:
    altura = calcularPasso(a,b,num_trapezios)
    area = soma*altura
    print(f"∑area =  {area:.{casas_decimais}f}")
    return soma*altura


def calcularErroDeArredondamento(a:int,b:int,num_trapezios:int,casas_decimais:int) -> float:
    passo = calcularPasso(a,b,num_trapezios)
    erro = abs((num_trapezios)*0.5 * 10**(-casas_decimais) * passo)
    print(f"|Ea| <= {erro:.{casas_decimais}f}")
    return erro

# TODO considerar ln base 2 e log base 10 (se tivermos o azar maldito de pegar ln, e sair base 10, ela vai pegar...)
# TODO corrigir o calculo do max da segunda derivada
# TODO imprimir: passo, equacao do erro de arredondamento, formula da area  

def maxSegundaDerivada(funcao,a:int,b:int,passo:float,casas_decimais:int) -> float:
    valor_max = 0

    logs = funcao.atoms(sp.log)
    for log_expr in logs: #caso a expressao tenha log, transforma o log para base 10
        if len(log_expr.args) == 1:
            x_arg = log_expr.args[0]
            funcao = funcao.subs(log_expr, sp.log(x_arg, 10))
    var = list(funcao.free_symbols)[0]

    segunda_derivada = sp.diff(funcao, var, 2)
    segunda_derivada = sp.lambdify(var, segunda_derivada)

    while a <= b:
        val = abs(segunda_derivada(a))
        if val > valor_max:
            valor_max  = val
        a += passo
    print(f"maximo da segunda derivada =  {valor_max:.{casas_decimais}f}")
    
    return valor_max 

def calcularErroDeTruncamento(passo:float,casas_decimais:int, max_segunda_derivada:float, num_trapezios:int) -> float:
    erro = abs(num_trapezios*(passo**3/12)*max_segunda_derivada)
    print(f"|Etru| <= {erro:.{casas_decimais}f}")
    return erro

def calcularErroTotal(Etru:float, Earr:float,casas_decimais:int) -> float:
    erro = abs(Etru + Earr)
    print(f"|Etot| <=  |Ea| + |Etru| <= {Earr:.{casas_decimais}f} + {Etru:.{casas_decimais}f}, logo {erro:.{casas_decimais}f}")
    return erro

def respostaFinal(funcao,a:int,b:int,area:float,casas_decimais:int,Etot):
    x = list(funcao.free_symbols)[0]
    funcao= sp.Integral(funcao, (x, a, b))
    inferior = area - Etot
    superior = area + Etot  
    sp.pprint(funcao)
    print(f"∈ ({area:.{casas_decimais}f} ± {Etot:.{casas_decimais}f})")
    print(f"Ou seja, ∈ [{inferior:.{casas_decimais}f}; {superior:.{casas_decimais}f}]")