import tkinter as tk
from tkinter import scrolledtext
from semantic_analyzer.main import semantic_analyzer
from lexical_analyzer import lexer
from syntatic_analyzer.main import syntactic_analyzer

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador de Código")
        self.geometry("800x800")

        # Editor de Código
        self.code_editor_label = tk.Label(self, text="Editor de Código")
        self.code_editor_label.pack()
        self.code_editor = scrolledtext.ScrolledText(self, width=100, height=20)
        self.code_editor.pack(pady=10)

        # Sección de Salida de Analizador Léxico
        self.lexical_output_label = tk.Label(self, text="Salida del Analizador Léxico")
        self.lexical_output_label.pack()
        self.lexical_output = scrolledtext.ScrolledText(self, width=100, height=5, wrap=tk.WORD)
        self.lexical_output.pack(pady=10)

        # Sección de Salida de Analizador Sintáctico
        self.syntax_output_label = tk.Label(self, text="Salida del Analizador Sintáctico")
        self.syntax_output_label.pack()
        self.syntax_output = scrolledtext.ScrolledText(self, width=100, height=5, wrap=tk.WORD)
        self.syntax_output.pack(pady=10)

        # Sección de Salida de Analizador Semántico
        self.semantic_output_label = tk.Label(self, text="Salida del Analizador Semántico")
        self.semantic_output_label.pack()
        self.semantic_output = scrolledtext.ScrolledText(self, width=100, height=5, wrap=tk.WORD)
        self.semantic_output.pack(pady=10)

        # Botón para iniciar análisis
        self.analyze_button = tk.Button(self, text="Analizar Código", command=self.analyze_code)
        self.analyze_button.pack(pady=10)

    def analyze_code(self):
        code = self.code_editor.get("1.0", tk.END)



        tokens_list = lexer(code)
        output_lexical = '\n'.join([str(elem) for elem in tokens_list])

        response = syntactic_analyzer(code)

        output_semantic = ""
        output_syntax = ""

        if response['status'] == 'success':
            try:
                output_list = semantic_analyzer(code)
                output_semantic = '\n'.join([str(elem) for elem in output_list])
                output_syntax = "Válido"
            except Exception as e:
                output_syntax = "Válido"
                output_semantic = f"{str(e)}"
        else:
            output_semantic = ""
            output_syntax = response['message']



        # Aquí iría tu lógica para el análisis léxico, sintáctico y semántico
        # En este ejemplo, simplemente copiamos el contenido del editor a las salidas
        self.lexical_output.delete("1.0", tk.END)
        self.lexical_output.insert(tk.END, output_lexical)

        self.syntax_output.delete("1.0", tk.END)
        self.syntax_output.insert(tk.END, output_syntax)

        self.semantic_output.delete("1.0", tk.END)
        self.semantic_output.insert(tk.END, output_semantic)