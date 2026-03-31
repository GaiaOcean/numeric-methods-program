import tkinter as tk
from tkinter import messagebox
import sympy as sp
import io
import sys
import methods 

class AppCalculadoraPUC:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo Numérico - Regra dos Trapézios (PUC-SP)")
        self.root.geometry("1150x950")
        self.root.configure(bg="#1e1e24")
        self.foco = None
        self.build_ui()

    def build_ui(self):
        # 1. Topo: Entrada da Função
        tk.Label(self.root, text="Função f(x):", bg="#1e1e24", fg="white", font=("Arial", 12, "bold")).pack(pady=(15,0))
        self.ent_f = tk.Entry(self.root, font=("Courier", 22), bg="#cfd0d1", justify="right")
        self.ent_f.pack(fill="x", padx=25, ipady=12)
        self.ent_f.bind("<FocusIn>", lambda e: self.set_foco(self.ent_f))

        # 2. Container Central (Teclado e Configurações)
        corpo = tk.Frame(self.root, bg="#1e1e24")
        corpo.pack(fill="both", expand=True, padx=25, pady=15)

        # Esquerda: Teclado Científico Simétrico (SEM abs)
        kb_frame = tk.Frame(corpo, bg="#1e1e24")
        kb_frame.pack(side="left", fill="both", expand=True)
        
        btns = [
            ('sin(', 'cos(', 'tan(', 'sqrt(', 'C', 'DEL'),
            ('7', '8', '9', '(', ')', '/'),
            ('4', '5', '6', 'log(', 'ln(', '*'),
            ('1', '2', '3', 'e', 'pi', '-'),
            ('.', '0', 'x', '**', ' ', '+')
        ]

        for r, row in enumerate(btns):
            for c, txt in enumerate(row):
                if txt == ' ': continue
                
                # Cores e Largura Fixa (width=7) para evitar espremer
                cor = "#ff8c00" if txt in '/*-+' or txt == '**' else "#d9534f" if txt in ('C', 'DEL') else "#2b2b36"
                btn = tk.Button(kb_frame, text=txt, bg=cor, fg="white", font=("Arial", 10, "bold"), 
                                width=7, height=2, command=lambda t=txt: self.digitar(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
            kb_frame.rowconfigure(r, weight=1)
        for col in range(6): kb_frame.columnconfigure(col, weight=1)

        # Direita: Painel de Parâmetros
        cfg_frame = tk.Frame(corpo, bg="#2b2b36", padx=20, pady=20)
        cfg_frame.pack(side="right", fill="y", padx=(20,0))
        self.campos = {}
        for lb, k in [("Lim. Inferior (a):", "a"), ("Lim. Superior (b):", "b"), ("Trapézios (n):", "n"), ("Casas (FIX):", "casas")]:
            tk.Label(cfg_frame, text=lb, bg="#2b2b36", fg="white", font=("Arial", 10, "bold")).pack(anchor="w")
            e = tk.Entry(cfg_frame, font=("Arial", 11), width=15)
            e.pack(pady=(0,12))
            e.bind("<FocusIn>", lambda ev, w=e: self.set_foco(w))
            self.campos[k] = e

        tk.Button(cfg_frame, text="CALCULAR", bg="#5cb85c", fg="white", font=("Arial", 12, "bold"), 
                  command=self.executar, height=2).pack(fill="x", pady=20)

        # 3. Base: Visor do Relatório com SCROLLBAR LATERAL
        frame_visor = tk.Frame(self.root, bg="#1e1e24")
        frame_visor.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        self.scroll = tk.Scrollbar(frame_visor)
        self.scroll.pack(side="right", fill="y")

        self.visor = tk.Text(frame_visor, font=("Courier", 10), bg="#cfd0d1", fg="black", 
                             padx=15, pady=15, yscrollcommand=self.scroll.set)
        self.visor.pack(side="left", fill="both", expand=True)
        self.scroll.config(command=self.visor.yview)

    def set_foco(self, widget): self.foco = widget
    
    def digitar(self, v):
        if not self.foco: return
        if v == 'C': self.foco.delete(0, tk.END)
        elif v == 'DEL': self.foco.delete(len(self.foco.get())-1, tk.END)
        else: self.foco.insert(tk.END, v)

    def executar(self):
        try:
            buffer = io.StringIO()
            sys.stdout = buffer
            f_txt = self.ent_f.get()

            a = float(sp.sympify(self.campos['a'].get(), locals={'pi': sp.pi, 'e': sp.E}))
            b = float(sp.sympify(self.campos['b'].get(), locals={'pi': sp.pi, 'e': sp.E}))
            n = int(self.campos['n'].get())
            casas = int(self.campos['casas'].get())

            f_sym = sp.sympify(f_txt, locals={
                'e': sp.E,
                'pi': sp.pi,
                'ln': sp.log,
                'log': lambda x: sp.log(x, 10)
            })

            print(f"Função: f(x) = {f_txt}\n")

            passo = methods.calcularPasso(a, b, n)
            print(f"Passo (h) = {passo}\n")

            resultados = methods.criarTabela(f_txt, f_sym, a, b, n, casas)
            print()

            soma = methods.calcularSomatorio(resultados, casas)
            print()

            area = methods.calcularAreaTrapezio(a, b, soma, casas, n)
            print()

            erro_arredondamento = methods.calcularErroDeArredondamento(a, b, n, casas)
            print()

            max_segunda_derivada = methods.maxSegundaDerivada(f_txt, f_sym, a, b, passo, n)
            print()

            erro_truncamento = methods.calcularErroDeTruncamento(f_txt, passo, casas, max_segunda_derivada, n, a, b)
            print()

            erro_total = methods.calcularErroTotal(erro_truncamento, erro_arredondamento, casas)
            print()

            methods.respostaFinal(f_txt, f_sym, a, b, area, casas, erro_total)

            sys.stdout = sys.__stdout__

            rel = buffer.getvalue()

            self.visor.delete(1.0, tk.END)
            self.visor.insert(tk.END, rel)

        except Exception as e:
            sys.stdout = sys.__stdout__
            messagebox.showerror("Erro", f"Houve um problema:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    AppCalculadoraPUC(root)
    root.mainloop()