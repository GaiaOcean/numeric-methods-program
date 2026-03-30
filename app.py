import tkinter as tk
from tkinter import messagebox
import sympy as sp
import methods # Usando o seu arquivo original sem alterações

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
            f_txt = self.ent_f.get()
            a = float(sp.sympify(self.campos['a'].get(), locals={'pi':sp.pi, 'e':sp.E}))
            b = float(sp.sympify(self.campos['b'].get(), locals={'pi':sp.pi, 'e':sp.E}))
            n = int(self.campos['n'].get())
            casas = int(self.campos['casas'].get())
            f_sym = sp.sympify(f_txt, locals={'e':sp.E, 'pi':sp.pi, 'ln':sp.log, 'log':lambda x: sp.log(x,10)})

            # Chamadas sincronizadas com o SEU methods.py
            h = methods.calcularPasso(a, b, n)
            tabela = methods.criarTabela(f_txt, f_sym, a, b, n, casas)
            soma = methods.calcularSomatorio(f_txt, f_sym, a, b, n, casas)
            area = methods.calcularAreaTrapezio(a, b, soma, casas, n)
            e_arr = methods.calcularErroDeArredondamento(a, b, n, casas)
            max_f2 = methods.maxSegundaDerivada(f_txt, f_sym, a, b, h, n)
            e_tru = methods.calcularErroDeTruncamento(h, casas, max_f2, n)
            e_tot = methods.calcularErroTotal(e_tru, e_arr, casas)

            # Cálculo dos limites para a representação em colchetes
            lim_inf = area - e_tot
            lim_sup = area + e_tot

            self.visor.delete(1.0, tk.END)
            rel = f"=== RELATÓRIO TÉCNICO: f(x) = {f_txt} ===\n\n"
            rel += f"1. PASSO: h = (b - a) / n = {h}\n\n"
            
            rel += "2. TABELA DE PONTOS:\n"
            rel += f"{'i':<4} | {'xi':<12} | {'f(xi)':<12}\n"
            rel += "-" * 35 + "\n"
            for i, val in enumerate(tabela):
                rel += f"{i:<4} | {a + i*h:<12.4f} | {val:<12.{casas}f}\n"

            rel += f"\n3. ÁREA ESTIMADA (Regra dos Trapézios):\n"
            rel += f"Fórmula: Área ≈ h * [f(x0)/2 + f(x1) + ... + f(xn)/2]\n"
            rel += f"Área ≈ {area:.{casas}f}\n\n"

            rel += f"4. ERROS:\n"
            rel += f"|Ea|   (Arredondamento) <= {e_arr:.{casas}f}\n"
            rel += f"|Etru| (Truncamento)     <= {e_tru:.{casas}f}\n"
            rel += f"|Etot| (Erro Total)      <= {e_tot:.{casas}f}\n\n"

            rel += f"5. RESULTADO FINAL (Representação Dupla):\n"
            rel += f"A. Por parênteses: ∈ ({area:.{casas}f} ± {e_tot:.{casas}f})\n"
            rel += f"B. Por colchetes:  ∈ [{lim_inf:.{casas}f}; {lim_sup:.{casas}f}]\n"
            
            self.visor.insert(tk.END, rel)

        except Exception as e:
            messagebox.showerror("Erro", f"Houve um problema:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    AppCalculadoraPUC(root)
    root.mainloop()