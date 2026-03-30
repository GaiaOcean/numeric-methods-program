import sympy as sp

def temVariavel(funcao:str) -> bool:
    """
    Verifica se a função contém variáveis (x, y ou z).
    Retorna True se for uma função variável e False se for constante.
    """
    for item in funcao:
        if item in ("x", "y", "z"):
            return True
    return False

def calcularPasso(a:float, b:float, num_trapezios:int) -> float:
    """
    Calcula o passo (h), que é a largura da base de cada trapézio.
    Variaveis: a (limite inferior), b (limite superior), num_trapezios (n).
    """
    return (b - a) / num_trapezios

def criarTabela(f_str:str, funcao, a:float, b:float, num_trapezios:int, casas_decimais:int) -> list:
    """
    Gera os pontos (x, f(x)) e imprime a tabela no terminal.
    """
    passo = calcularPasso(a, b, num_trapezios)
    possuiVariavel = temVariavel(f_str)
    lista_dos_resultados = list()

    # Prepara a função para ser executada pelo Python
    if possuiVariavel:
        var = list(funcao.free_symbols)[0]
        math_function = sp.lambdify(var, funcao)
    else:
        math_function = sp.lambdify([], funcao)
    
    print(f"\n{'x':>3} {'|':>5} {'f(x)':>7}")
    print('-' * 20)

    # Uso do 'for' para garantir que o ponto_avaliado chegue exatamente ao limite b
    for i in range(num_trapezios + 1):
        # ponto_avaliado: O valor de x na posição atual da partição
        ponto_avaliado = a + (i * passo)
        
        resultado = math_function(ponto_avaliado) if possuiVariavel else math_function()
        
        print(f"{ponto_avaliado:.1f}\t  {resultado:.{casas_decimais}f}")
        lista_dos_resultados.append(resultado)
    
    print('-' * 20)
    return lista_dos_resultados

def calcularSomatorio(f_str, funcao, a:float, b:float, num_trapezios:int, casas_decimais:int) -> float:
    """
    Soma as áreas dos trapézios seguindo a Regra dos Trapézios.
    """
    resultados = criarTabela(f_str, funcao, a, b, num_trapezios, casas_decimais)
    n = len(resultados)
    soma = 0
    equacao_soma_areas = [] 

    for i in range(n):
        # f(x0) e f(xn) são divididos por 2 conforme a fórmula
        if i == 0 or i == n-1:
            soma += resultados[i] / 2
            equacao_soma_areas.append(f"({resultados[i]:.{casas_decimais}f}/2)")
        else:
            soma += resultados[i]
            equacao_soma_areas.append(f"{resultados[i]:.{casas_decimais}f}")
            
    print(f"∑ = {' + '.join(equacao_soma_areas)} = {soma:.{casas_decimais}f}")
    return soma

def calcularAreaTrapezio(a, b, soma:float, casas_decimais:int, num_trapezios:int) -> float:
    """Calcula a área final multiplicando o somatório pelo passo h."""
    altura = calcularPasso(a, b, num_trapezios)
    area = soma * altura
    print(f"Area ≈ (soma das areas) * h")
    print(f"Area ≈ {area:.{casas_decimais}f}")
    return area

def calcularErroDeArredondamento(a:float, b:float, num_trapezios:int, casas_decimais:int) -> float:
    """Calcula o limite superior do erro gerado pelo corte de casas decimais."""
    passo = calcularPasso(a, b, num_trapezios)
    erro = abs((num_trapezios) * 0.5 * 10**(-casas_decimais) * passo)
    print(f"|Ea| <= n * 0.5 * 10^(-casas_decimais) * h")
    print(f"|Ea| <= {erro} ≈ {erro:.{casas_decimais}f}")
    return erro

def maxSegundaDerivada(f_str:str, funcao, a:float, b:float, passo:float, num_trapezios:int) -> float:
    """Varre o intervalo para encontrar o módulo máximo da segunda derivada |f''(x)|."""
    valor_max = 0
    if temVariavel(f_str):
        var = list(funcao.free_symbols)[0]
        # Derivamos o objeto simbólico 'funcao' para precisão
        segunda_derivada_sym = sp.diff(funcao, var, 2)
        segunda_derivada = sp.lambdify(var, segunda_derivada_sym)

        for i in range(num_trapezios + 1):
            ponto_avaliado = a + (i * passo)
            val = abs(segunda_derivada(ponto_avaliado))
            if val > valor_max:
                valor_max = val
    return valor_max 

def calcularErroDeTruncamento(passo:float, casas_decimais:int, max_segunda_derivada:float, num_trapezios:int) -> float:
    """Calcula o erro inerente ao método (a curvatura que o trapézio não cobre)."""
    erro = abs(num_trapezios * (passo**3 / 12) * max_segunda_derivada)
    print(f"|Etru| <= n * (h³/12) * max|f''(x)|")
    print(f" max|f''(x)| => {max_segunda_derivada} ≈ {max_segunda_derivada:.{casas_decimais}f}")
    print(f"|Etru| <= {erro} ≈ {erro:.{casas_decimais}f}")
    return erro

def calcularErroTotal(Etru:float, Earr:float, casas_decimais:int) -> float:
    """Soma o erro de arredondamento e o de truncamento."""
    erro = abs(Etru + Earr)
    print(f"|Etot| <= |Ea| + |Etru| <= {Earr} + {Etru} ≈ {erro:.{casas_decimais}f}")
    return erro

def respostaFinal(f_str:str, funcao, a:float, b:float, area:float, casas_decimais:int, Etot):
    """Exibe o resultado final com a notação de intervalo de confiança."""
    if temVariavel(f_str):
        var = list(funcao.free_symbols)[0]
        funcao_integral = sp.Integral(funcao, (var, a, b))
    else:
        funcao_integral = funcao 
    
    inferior = area - Etot
    superior = area + Etot  
    sp.pprint(funcao_integral)
    print(f"∈ ({area:.{casas_decimais}f} ± {Etot:.{casas_decimais}f})")
    print(f"Ou seja, ∈ [{inferior:.{casas_decimais}f}; {superior:.{casas_decimais}f}]")