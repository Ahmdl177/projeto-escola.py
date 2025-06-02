import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
import sqlite3

NOME_BANCO_DADOS = "UNIFBV.db"
TITULO_PROJETO = "Sistema de Gestão UNIFBV"
DESCRICAO_APP = "Aplicação para cadastro de alunos e turmas utilizando Tkinter e SQLite."
MEMBROS_GRUPO = "Arthur Henrique, Bruno Henrique, Guilherme Sales"

def conectar_banco():
    """Conecta ao banco de dados SQLite e retorna a conexão e o cursor."""
    conn = sqlite3.connect(NOME_BANCO_DADOS)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas_se_nao_existirem():
    """Cria as tabelas 'turma' e 'aluno' se elas ainda não existirem."""
    conn, cursor = conectar_banco()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turma (
                id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_turma TEXT UNIQUE NOT NULL,
                periodo TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aluno (
                id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_aluno TEXT NOT NULL,
                email_aluno TEXT,
                id_turma_fk INTEGER,
                FOREIGN KEY (id_turma_fk) REFERENCES turma(id_turma)
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()

def adicionar_turma_db(nome_turma, periodo):
    conn, cursor = conectar_banco()
    try:
        cursor.execute("INSERT INTO turma (nome_turma, periodo) VALUES (?, ?)", (nome_turma, periodo))
        conn.commit()
        messagebox.showinfo("Sucesso", "Turma adicionada com sucesso!")
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", f"A turma '{nome_turma}' já existe.")
        return False
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao adicionar turma: {e}")
        return False
    finally:
        conn.close()

def buscar_turmas_db():
    conn, cursor = conectar_banco()
    try:
        cursor.execute("SELECT id_turma, nome_turma, periodo FROM turma ORDER BY nome_turma")
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao buscar turmas: {e}")
        return []
    finally:
        conn.close()
def adicionar_aluno_db(nome_aluno, email_aluno, id_turma_fk):
    conn, cursor = conectar_banco()
    try:
        cursor.execute("INSERT INTO aluno (nome_aluno, email_aluno, id_turma_fk) VALUES (?, ?, ?)",
                       (nome_aluno, email_aluno, id_turma_fk))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao adicionar aluno: {e}")
        return False
    finally:
        conn.close()

def buscar_alunos_com_turmas_db():
    conn, cursor = conectar_banco()
    try:
        cursor.execute("""
            SELECT a.id_aluno, a.nome_aluno, a.email_aluno, COALESCE(t.nome_turma, 'Sem Turma')
            FROM aluno a
            LEFT JOIN turma t ON a.id_turma_fk = t.id_turma
            ORDER BY a.nome_aluno
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao buscar alunos: {e}")
        return []
    finally:
        conn.close()
class AppEscola:
    def __init__(self, root):
        self.root = root
        self.root.title(TITULO_PROJETO)
        self.root.geometry("800x600")

        criar_tabelas_se_nao_existirem()

        self.criar_menus() 

        self.frame_conteudo = ttk.Frame(self.root, padding="10")
        self.frame_conteudo.pack(expand=True, fill=tk.BOTH)

        self.mostrar_tela_inicial()

    def limpar_frame_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_frame_conteudo()
        label = ttk.Label(self.frame_conteudo, text="Bem-vindo ao Sistema de Gestão Academica!", font=("Arial", 16))
        label.pack(pady=20)
        btn_alunos = ttk.Button(self.frame_conteudo, text="Ver Alunos", command=self.abrir_tela_exibir_alunos)
        btn_alunos.pack(pady=10)
        btn_turmas = ttk.Button(self.frame_conteudo, text="Ver Turmas", command=self.abrir_tela_exibir_turmas)
        btn_turmas.pack(pady=10)

    def criar_menus(self):
        menubar = tk.Menu(self.root) 

        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(label="Alunos", command=self.abrir_tela_cadastro_aluno) 
        menu_cadastros.add_command(label="Turmas", command=self.abrir_tela_cadastro_turma)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        menu_exibir = tk.Menu(menubar, tearoff=0)
        menu_exibir.add_command(label="Listar Alunos", command=self.abrir_tela_exibir_alunos)
        menu_exibir.add_command(label="Listar Turmas", command=self.abrir_tela_exibir_turmas)
        menubar.add_cascade(label="Exibir", menu=menu_exibir)

        menu_ajuda = tk.Menu(menubar, tearoff=0) 
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.root.config(menu=menubar)

    def mostrar_sobre(self):
        texto_sobre = f"""
        {TITULO_PROJETO}

        Descrição:
        {DESCRICAO_APP}

        Desenvolvido por:
        {MEMBROS_GRUPO}
        """
        messagebox.showinfo("Sobre o Sistema", texto_sobre)

    def abrir_tela_cadastro_turma(self):
        self.limpar_frame_conteudo()
        label_titulo = ttk.Label(self.frame_conteudo, text="Cadastro de Turma", font=("Arial", 14))
        label_titulo.pack(pady=10)

        frame_form = ttk.Frame(self.frame_conteudo)
        frame_form.pack(pady=10)

        ttk.Label(frame_form, text="Nome da Turma:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_turma = ttk.Entry(frame_form, width=40)
        self.entry_nome_turma.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Período:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_periodo_turma = ttk.Combobox(frame_form, values=["Manhã", "Tarde", "Noite", "Integral"], width=37)
        self.combo_periodo_turma.grid(row=1, column=1, padx=5, pady=5)
        self.combo_periodo_turma.current(0) 

        btn_salvar = ttk.Button(frame_form, text="Salvar Turma", command=self.salvar_turma)
        btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

    def salvar_turma(self):
        nome = self.entry_nome_turma.get().strip()
        periodo = self.combo_periodo_turma.get()

        if not nome:
            messagebox.showerror("Erro de Validação", "O nome da turma é obrigatório.")
            return

        if adicionar_turma_db(nome, periodo):
            self.entry_nome_turma.delete(0, tk.END) 
            self.combo_periodo_turma.current(0)
            self.abrir_tela_exibir_turmas() 

    def abrir_tela_cadastro_aluno(self):
        self.limpar_frame_conteudo()
        label_titulo = ttk.Label(self.frame_conteudo, text="Cadastro de Aluno", font=("Arial", 14))
        label_titulo.pack(pady=10)

        frame_form = ttk.Frame(self.frame_conteudo)
        frame_form.pack(pady=10)

        ttk.Label(frame_form, text="Nome do Aluno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_aluno = ttk.Entry(frame_form, width=40)
        self.entry_nome_aluno.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_email_aluno = ttk.Entry(frame_form, width=40)
        self.entry_email_aluno.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Turma:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        turmas_raw = buscar_turmas_db() 
        self.turmas_map = {nome: id_turma for id_turma, nome, _ in turmas_raw}
        nomes_turmas = [nome for _, nome, _ in turmas_raw]

        self.combo_turma_aluno = ttk.Combobox(frame_form, values=nomes_turmas, width=37, state="readonly")
        self.combo_turma_aluno.grid(row=2, column=1, padx=5, pady=5)
        if nomes_turmas:
            self.combo_turma_aluno.current(0)

        btn_salvar = ttk.Button(frame_form, text="Salvar Aluno", command=self.salvar_aluno)
        btn_salvar.grid(row=3, column=0, columnspan=2, pady=10)

    def salvar_aluno(self):
        nome = self.entry_nome_aluno.get().strip()
        email = self.entry_email_aluno.get().strip()
        nome_turma_selecionada = self.combo_turma_aluno.get()

        if not nome:
            messagebox.showerror("Erro de Validação", "O nome do aluno é obrigatório.")
            return
        if not nome_turma_selecionada:
            messagebox.showerror("Erro de Validação", "Selecione uma turma para o aluno.")
            return

        id_turma = self.turmas_map.get(nome_turma_selecionada)

        if adicionar_aluno_db(nome, email, id_turma):
            self.entry_nome_aluno.delete(0, tk.END)
            self.entry_email_aluno.delete(0, tk.END)
            if self.combo_turma_aluno['values']:
                 self.combo_turma_aluno.current(0)
            self.abrir_tela_exibir_alunos()

    def abrir_tela_exibir_turmas(self):
        self.limpar_frame_conteudo()
        label_titulo = ttk.Label(self.frame_conteudo, text="Lista de Turmas", font=("Arial", 14))
        label_titulo.pack(pady=10)

        colunas = ("id_turma", "nome_turma", "periodo")
        self.tree_turmas = ttk.Treeview(self.frame_conteudo, columns=colunas, show="headings")

        self.tree_turmas.heading("id_turma", text="ID")
        self.tree_turmas.heading("nome_turma", text="Nome da Turma")
        self.tree_turmas.heading("periodo", text="Período")

        self.tree_turmas.column("id_turma", width=50, anchor=tk.CENTER)
        self.tree_turmas.column("nome_turma", width=300)
        self.tree_turmas.column("periodo", width=150, anchor=tk.CENTER)

        turmas = buscar_turmas_db()
        for turma in turmas:
            self.tree_turmas.insert("", tk.END, values=turma)

        self.tree_turmas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_atualizar = ttk.Button(self.frame_conteudo, text="Atualizar Lista", command=self.abrir_tela_exibir_turmas)
        btn_atualizar.pack(pady=5)

    def abrir_tela_exibir_alunos(self):
        self.limpar_frame_conteudo()
        label_titulo = ttk.Label(self.frame_conteudo, text="Lista de Alunos", font=("Arial", 14))
        label_titulo.pack(pady=10)

        colunas_alunos = ("id_aluno", "nome_aluno", "email_aluno", "nome_turma")
        self.tree_alunos = ttk.Treeview(self.frame_conteudo, columns=colunas_alunos, show="headings")

        self.tree_alunos.heading("id_aluno", text="ID")
        self.tree_alunos.heading("nome_aluno", text="Nome do Aluno")
        self.tree_alunos.heading("email_aluno", text="Email")
        self.tree_alunos.heading("nome_turma", text="Turma")

        self.tree_alunos.column("id_aluno", width=50, anchor=tk.CENTER)
        self.tree_alunos.column("nome_aluno", width=250)
        self.tree_alunos.column("email_aluno", width=250)
        self.tree_alunos.column("nome_turma", width=150)

        alunos = buscar_alunos_com_turmas_db()
        for aluno in alunos:
            self.tree_alunos.insert("", tk.END, values=aluno)

        self.tree_alunos.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_atualizar = ttk.Button(self.frame_conteudo, text="Atualizar Lista", command=self.abrir_tela_exibir_alunos)
        btn_atualizar.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppEscola(root)
    root.mainloop()