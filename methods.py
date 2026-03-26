
import sympy as sp

def temVariavel(funcao:str) -> bool:
    for item in funcao:
        if item in ("x", "y", "z"):
            return True
    return False


def calcularPasso(a:int, b:int, num_trapezios:int) -> float: #tambem é a altura do trapezio
    return (b - a) / num_trapezios

def criarTabela(f:str,funcao,a:int, b:int,num_trapezios:int, casas_decimais:int) -> list:
    passo = calcularPasso(a,b,num_trapezios)
    possuiVariavel = temVariavel(f)
    logs = funcao.atoms(sp.log)
    lista_dos_resultados = list()

    for log_expr in logs:
        if len(log_expr.args) == 1:  # nenhuma base especifica
            x_arg = log_expr.args[0]
            funcao = funcao.subs(log_expr, sp.log(x_arg, 10))

    if possuiVariavel:
        var = list(funcao.free_symbols)[0]
        math_function = sp.lambdify(var,funcao)
    else:
        math_function = sp.lambdify([],funcao)
    
    #separar entre x e f(x) visualmente
    print(f"{'x':>3} {'|':>5} {'f(x)':>7}")
    print('-' * 15)

    if possuiVariavel:
        while a <= b:
            resultado = math_function(a)
            print(f"{a:.1f}\t  {resultado:.{casas_decimais}f}")
            lista_dos_resultados.append(resultado)
            a += passo
    else:
        while a <= b:
            resultado = math_function()
            print(f"{a:.1f}\t  {resultado:.{casas_decimais}f}")
            lista_dos_resultados.append(resultado)
            a += passo
    
   
       
    print('-' * 15)

    return lista_dos_resultados


def calcularSomatorio(f,funcao,a:int, b:int,num_trapezios:int, casas_decimais:int)->float:
    resultados = criarTabela(f,funcao,a,b,num_trapezios,casas_decimais)
    n = len(resultados)
    soma = 0
    equacao_soma_areas = [] #pra printar a soma das areas, primeiro e utlimo dividio por 2 

    for i in range(0,n):
        
        if i == 0 or i == n-1:
            soma += resultados[i]/2
            equacao_soma_areas.append(f"({resultados[i]:.{casas_decimais}f}/2)")
        else:
            soma += resultados[i]
            equacao_soma_areas.append(f"{resultados[i]:.{casas_decimais}f}")
    print(f"∑ = {' + '.join(equacao_soma_areas)} = {soma:.{casas_decimais}f}")

    return soma

def calcularAreaTrapezio(a,b,soma:float,casas_decimais:int,num_trapezios:int) -> float:
    altura = calcularPasso(a,b,num_trapezios)
    area = soma*altura
    print(f"Area ≈ (soma das areas) * h")
    print(f"Area ≈ {area:.{casas_decimais}f}")
    return soma*altura


def calcularErroDeArredondamento(a:int,b:int,num_trapezios:int,casas_decimais:int) -> float:
    passo = calcularPasso(a,b,num_trapezios)
    erro = abs((num_trapezios)*0.5 * 10**(-casas_decimais) * passo)
    print(f"|Ea| <= n * 0.5 * 10^(-casas_decimais) * h")
    print(f"|Ea| <= {erro} ≈ {erro:.{casas_decimais}f}")
    return erro

# TODO considerar ln base 2 e log base 10 (se tivermos o azar maldito de pegar ln, e sair base 10, ela vai pegar...) - pendente
# TODO corrigir o calculo do max da segunda derivada - acho que ok
# TODO imprimir: passo, equacao do erro de arredondamento, formula da area - ok

def maxSegundaDerivada(f:str,funcao,a:int,b:int,passo:float,casas_decimais:int, num_trapezios:int) -> float:
    valor_max = 0
    possuiVariavel = temVariavel(f)
    logs = funcao.atoms(sp.log)
    for log_expr in logs: #caso a expressao tenha log, transforma o log para base 10
        if len(log_expr.args) == 1:
            x_arg = log_expr.args[0]
            funcao = funcao.subs(log_expr, sp.log(x_arg, 10))

    if possuiVariavel:
        var = list(funcao.free_symbols)[0]  # pick a variable
        segunda_derivada_sym = sp.diff(f, var, 2)  # differentiate SymPy expression
        segunda_derivada = sp.lambdify(var, segunda_derivada_sym)

        for i in range(num_trapezios+1): #exemplo intervalo 2 a 5, 6 trapezios = 0 a 6 pontos, 7 pontos
            x = a + i*passo #vai testar cada ponto (usei o ex 2 a 5, passo = 0.5, pontos: 2, 2.5, 3, 3.5, 4, 4.5, 5)
            val = abs(segunda_derivada(x))
            if val > valor_max:
                valor_max  = val
    
    return valor_max 

def calcularErroDeTruncamento(passo:float,casas_decimais:int, max_segunda_derivada:float, num_trapezios:int) -> float:
    erro = abs(num_trapezios*(passo**3/12)*max_segunda_derivada)
    print(f"|Etru| <= n * (h³/12) * max|f''(x)|")
    print(f" max|f''(x)| => {max_segunda_derivada} ≈ {max_segunda_derivada:.{casas_decimais}f}")
    print(f"|Etru| <= {erro} ≈ {erro:.{casas_decimais}f}")
    return erro

def calcularErroTotal(Etru:float, Earr:float,casas_decimais:int) -> float:
    erro = abs(Etru + Earr)
    # print(f"|Etot| <  |Ea| + |Etru| < {Earr:.{casas_decimais}f} + {Etru:.{casas_decimais}f}, logo {erro:.{casas_decimais}f}")
    print(f"|Etot| <= |Ea| + |Etru| <= {Earr} + {Etru} < {Earr + Etru} ≈ {erro:.{casas_decimais}f} (com {casas_decimais} casas)")
    return erro

def respostaFinal(f:str,funcao,a:int,b:int,area:float,casas_decimais:int,Etot):
    if temVariavel(f):
        x = list(funcao.free_symbols)[0]
        funcao= sp.Integral(funcao, (x, a, b))
    else:
       funcao = funcao 
    inferior = area - Etot
    superior = area + Etot  
    sp.pprint(funcao)
    print(f"∈ ({area:.{casas_decimais}f} ± {Etot:.{casas_decimais}f})")
    print(f"Ou seja, ∈ [{inferior:.{casas_decimais}f}; {superior:.{casas_decimais}f}]")