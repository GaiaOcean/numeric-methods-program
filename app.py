import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import methods 

class CalculadoraFrontEnd:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Métodos Numéricos - PUC-SP")
        self.root.geometry("1150x850") 
        self.root.configure(bg="#1e1e24") 
        
        self.configurar_estilos()
        self.criar_interface()
        self.entrada_focada = self.entry_funcao 

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e24", foreground="#ffffff", font=("Arial", 11, "bold"))
        style.configure("Num.TButton", font=("Arial", 12, "bold"), background="#2b2b36", foreground="white")
        style.configure("Op.TButton", font=("Arial", 12, "bold"), background="#ff8c00", foreground="white")
        style.configure("Acao.TButton", font=("Arial", 12, "bold"), background="#d9534f", foreground="white")
        style.configure("Calc.TButton", font=("Arial", 14, "bold"), background="#5cb85c", foreground="white")

    def criar_interface(self):
        # --- TOPO: Entrada da Função ---
        frame_topo = tk.Frame(self.root, bg="#1e1e24")
        frame_topo.pack(pady=15, fill="x", padx=20)
        
        ttk.Label(frame_topo, text="Função f(x):", font=("Arial", 14, "bold")).pack(anchor="w")
        self.entry_funcao = tk.Entry(frame_topo, font=("Courier", 20), bg="#cfd0d1", fg="black", justify="right")
        self.entry_funcao.pack(fill="x", ipady=10)
        self.entry_funcao.bind("<FocusIn>", lambda e: self.atualizar_foco(self.entry_funcao))

        frame_meio = tk.Frame(self.root, bg="#1e1e24")
        frame_meio.pack(fill="x", padx=20)

        # --- ESQUERDA: Teclado Científico ---
        frame_teclado = tk.Frame(frame_meio, bg="#1e1e24")
        frame_teclado.pack(side="left", fill="both", expand=True)
        botoes = [
            ('sin(', 'cos(', 'tan(', 'sqrt(', 'C', 'DEL'), 
            ('7', '8', '9', '(', ')', '/'), 
            ('4', '5', '6', 'log(', 'ln(', '*'), 
            ('1', '2', '3', 'e', 'pi', '-'), 
            ('.', '0', 'x', '**', 'abs(', '+')
        ]
        for r, linha in enumerate(botoes):
            for c, texto in enumerate(linha):
                estilo = "Num.TButton"
                if texto in ['/', '*', '-', '+', '**']: estilo = "Op.TButton"
                elif texto in ['C', 'DEL']: estilo = "Acao.TButton"
                btn = ttk.Button(frame_teclado, text=texto, style=estilo, command=lambda t=texto: self.clique_teclado(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2, ipadx=5, ipady=10)
            frame_teclado.rowconfigure(r, weight=1)
            frame_teclado.columnconfigure(c, weight=1)

        # --- DIREITA: Configurações ---
        frame_configs = tk.Frame(frame_meio, bg="#2b2b36", padx=15, pady=15)
        frame_configs.pack(side="right", fill="y", padx=(15, 0))
        
        campos = [("Lim. Inferior (a):", "entry_a"), ("Lim. Superior (b):", "entry_b"), 
                  ("Trapézios (n):", "entry_n"), ("Casas (FIX):", "entry_casas")]
        
        for label, var_name in campos:
            ttk.Label(frame_configs, text=label, background="#2b2b36").pack(anchor="w")
            entry = tk.Entry(frame_configs, font=("Arial", 12), width=15)
            entry.pack(pady=(0, 10))
            entry.bind("<FocusIn>", lambda e, w=entry: self.atualizar_foco(w))
            setattr(self, var_name, entry)

        ttk.Button(frame_configs, text="CALCULAR\nINTEGRAL", style="Calc.TButton", command=self.integrar_backend).pack(fill="x", ipady=15)

        # --- BASE: Relatório ---
        frame_base = tk.Frame(self.root, bg="#1e1e24")
        frame_base.pack(fill="both", expand=True, padx=20, pady=20)
        ttk.Label(frame_base, text="Relatório Numérico:").pack(anchor="w")
        
        self.visor_relatorio = tk.Text(frame_base, font=("Courier", 11), bg="#cfd0d1", fg="black")
        self.visor_relatorio.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(frame_base, command=self.visor_relatorio.yview)
        scroll.pack(side="right", fill="y")
        self.visor_relatorio.config(yscrollcommand=scroll.set)

    def atualizar_foco(self, entry_widget): self.entrada_focada = entry_widget

    def clique_teclado(self, valor):
        if not self.entrada_focada: return
        if valor == 'C': self.entrada_focada.delete(0, tk.END)
        elif valor == 'DEL': self.entrada_focada.delete(len(self.entrada_focada.get())-1, tk.END)
        else: self.entrada_focada.insert(tk.END, valor)

    def integrar_backend(self):
        f_raw = self.entry_funcao.get()
        a_raw, b_raw = self.entry_a.get(), self.entry_b.get()
        n_str, casas_str = self.entry_n.get(), self.entry_casas.get()
 
        if not all([f_raw, a_raw, b_raw, n_str, casas_str]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!"); return
 
        try:
            a = float(sp.sympify(a_raw, locals={'pi': sp.pi, 'e': sp.E}))
            b = float(sp.sympify(b_raw, locals={'pi': sp.pi, 'e': sp.E}))
            n, casas = int(n_str), int(casas_str)
 
            f_sym = sp.sympify(f_raw, locals={
                'e': sp.E, 'pi': sp.pi, 'ln': sp.log,
                'log': lambda x: sp.log(x, 10)
            })
 
            passo = methods.calcularPasso(a, b, n)
            resultados = methods.criarTabela(f_raw, f_sym, a, b, n, casas)
            soma = methods.calcularSomatorio(f_raw, f_sym, a, b, n, casas)
 
            # --- CONSTRUÇÃO DA TABELA VISUAL NO RELATÓRIO ---
            tabela_relatorio = f"{'x':<10} | {'f(x)':<10}\n"
            tabela_relatorio += "-" * 25 + "\n"
            for i, res in enumerate(resultados):
                ponto_x = a + (i * passo)
                tabela_relatorio += f"{ponto_x:<10.4f} | {res:<10.{casas}f}\n"
 
            # Montagem da fórmula da soma
            equacao_lista = []
            for i, res in enumerate(resultados):
                if i == 0 or i == len(resultados) - 1:
                    equacao_lista.append(f"({res:.{casas}f}/2)")
                else:
                    equacao_lista.append(f"{res:.{casas}f}")
            soma_str = " + ".join(equacao_lista)
 
            area = methods.calcularAreaTrapezio(a, b, soma, casas, n)
            e_arr = methods.calcularErroDeArredondamento(a, b, n, casas)
            max_f2 = methods.maxSegundaDerivada(f_raw, f_sym, a, b, passo, n)
            e_tru = methods.calcularErroDeTruncamento(passo, casas, max_f2, n)
            e_tot = e_arr + e_tru
 
            # --- EXIBIÇÃO NO VISOR ---
            self.visor_relatorio.delete(1.0, tk.END)
            rel = f"=== RELATÓRIO: f(x) = {f_raw} ===\n\n"
           
            rel += "1. TABELA DE PONTOS:\n"
            rel += tabela_relatorio + "\n"
           
            rel += f"2. CÁLCULO DA ÁREA (h = {passo})\n"
            rel += f"∑ = {soma_str}\n"
            rel += f"∑ = {soma:.{casas}f}\n"
            rel += f"Área ≈ {area:.{casas}f}\n\n"
           
            rel += "3. ANÁLISE DE ERROS:\n"
            rel += f"|f''(x)|_max = {max_f2:.{casas}f}\n"
            rel += f"|Ea|   <= {e_arr:.{casas}f}\n"
            rel += f"|Etru| <= {e_tru:.{casas}f}\n"
            rel += f"|Etot| <= {e_tot:.{casas}f}\n\n"
           
            rel += "4. RESULTADO FINAL:\n"
            rel += f"∈ ({area:.{casas}f} ± {e_tot:.{casas}f})\n"
            rel += f"Intervalo: [{area - e_tot:.{casas}f}; {area + e_tot:.{casas}f}]"
           
            self.visor_relatorio.insert(tk.END, rel)
 
        except Exception as err:
            messagebox.showerror("Erro Matemático", f"Detalhe: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    CalculadoraFrontEnd(root)
    root.mainloop()