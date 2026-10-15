import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from riviera_core import BuildError, Project, Table


# ==============================================================
# Traduções da interface
# ==============================================================

ENGLISH = {
    "title": "Riviera - Text Editor",
    "file": "File",
    "tools": "Tools",
    "language": "Language",
    "dictionary": "Open dictionary",
    "open_bin": "Open BIN",
    "open_json": "Open JSON project",
    "save": "Save",
    "save_as": "Save project as...",
    "export_bin": "Export BIN",
    "export_dump": "Export old dump",
    "import_dump": "Import old dump",
    "exit": "Exit",
    "show_all": "Show all",
    "translated_only": "Show translated only",
    "pending_only": "Show pending only",
    "text_only": "Show text only",
    "validate": "Validate translations",
    "search": "Search:",
    "clear": "Clear",
    "entries": "Entries",
    "status": "Status",
    "text": "Text",
    "original": "Original text",
    "translation": "Translation",
    "show_hidden": "Show hidden bytes/commands",
    "preserved": "Preserved bytes",
    "translated": "Translated",
    "pending": "Pending",
    "command": "Command",
    "none_hidden": "✓ No hidden commands",
    "hidden": "⚙ {count} preserved block(s) · {size} bytes",
    "unavailable": "Hidden bytes unavailable",
    "no_hidden": "No hidden bytes found.",
    "no_project": "No project open",
    "dictionary_required": "Dictionary required",
    "open_dictionary_first": "Open the dictionary first.",
    "project_required": "Project required",
    "open_project_first": "Open a BIN or JSON project first.",
    "loaded_dictionary": "Dictionary loaded: {name}",
    "opened_bin": "BIN opened: {name} — {count} entries",
    "opened_project": "Project opened: {name} — {count} entries",
    "saved_project": "Project saved: {name}",
    "exported_bin": "BIN exported: {name}",
    "warnings": "Dictionary warnings",
    "validation": "Validation",
    "valid": "No invalid characters found.",
    "invalid": "Invalid characters",
    "imported": "Import completed",
    "import_result": "Imported: {a}\nSkipped: {b}",
    "old_project": (
        "[Old project without raw bytes]\n\n"
        "Open the original BIN and save a new project."
    ),
    "raw_missing": (
        "This entry has no original raw bytes.\n\n"
        "Open the original BIN and save a new project."
    ),
    "separator": "──────── ⚙ preserved commands here ────────",
    "save_before_exit": "Save the project before exiting?",
    "rel": "rel",
    "abs": "abs",
    "bytes": "bytes",
    "tags": "tags",
}

SPANISH = {
    **ENGLISH,
    "title": "Riviera - Editor de textos",
    "file": "Archivo",
    "tools": "Herramientas",
    "language": "Idioma",
    "dictionary": "Abrir diccionario",
    "open_bin": "Abrir BIN",
    "open_json": "Abrir proyecto JSON",
    "save": "Guardar",
    "save_as": "Guardar proyecto como...",
    "export_bin": "Exportar BIN",
    "export_dump": "Exportar dump antiguo",
    "import_dump": "Importar dump antiguo",
    "exit": "Salir",
    "show_all": "Mostrar todos",
    "translated_only": "Mostrar solo traducidos",
    "pending_only": "Mostrar solo pendientes",
    "text_only": "Mostrar solo textos",
    "validate": "Validar traducciones",
    "search": "Buscar:",
    "clear": "Limpiar",
    "entries": "Entradas",
    "status": "Estado",
    "text": "Texto",
    "original": "Texto original",
    "translation": "Traducción",
    "show_hidden": "Mostrar bytes/comandos ocultos",
    "preserved": "Bytes preservados",
    "translated": "Traducida",
    "pending": "Pendiente",
    "command": "Comando",
    "none_hidden": "✓ No hay comandos ocultos",
    "hidden": "⚙ {count} bloque(s) preservado(s) · {size} bytes",
    "unavailable": "Bytes ocultos no disponibles",
    "no_hidden": "No se encontraron bytes ocultos.",
    "no_project": "Ningún proyecto abierto",
    "dictionary_required": "Diccionario necesario",
    "open_dictionary_first": "Abra primero el diccionario.",
    "project_required": "Proyecto necesario",
    "open_project_first": "Abra primero un BIN o proyecto JSON.",
    "loaded_dictionary": "Diccionario cargado: {name}",
    "opened_bin": "BIN abierto: {name} — {count} entradas",
    "opened_project": "Proyecto abierto: {name} — {count} entradas",
    "saved_project": "Proyecto guardado: {name}",
    "exported_bin": "BIN exportado: {name}",
    "warnings": "Avisos del diccionario",
    "validation": "Validación",
    "valid": "No se encontraron caracteres inválidos.",
    "invalid": "Caracteres inválidos",
    "imported": "Importación completada",
    "import_result": "Importadas: {a}\nIgnoradas: {b}",
    "old_project": (
        "[Proyecto antiguo sin bytes raw]\n\n"
        "Abra el BIN original y guarde un proyecto nuevo."
    ),
    "raw_missing": (
        "Esta entrada no tiene bytes raw originales.\n\n"
        "Abra el BIN original y guarde un proyecto nuevo."
    ),
    "separator": "──────── ⚙ comandos preservados aquí ────────",
    "save_before_exit": "¿Guardar el proyecto antes de salir?",
}

FRENCH = {
    **ENGLISH,
    "title": "Riviera - Éditeur de textes",
    "file": "Fichier",
    "tools": "Outils",
    "language": "Langue",
    "dictionary": "Ouvrir le dictionnaire",
    "open_bin": "Ouvrir le BIN",
    "open_json": "Ouvrir le projet JSON",
    "save": "Enregistrer",
    "save_as": "Enregistrer le projet sous...",
    "export_bin": "Exporter le BIN",
    "export_dump": "Exporter l'ancien dump",
    "import_dump": "Importer l'ancien dump",
    "exit": "Quitter",
    "show_all": "Afficher tout",
    "translated_only": "Afficher uniquement les traductions",
    "pending_only": "Afficher uniquement les textes en attente",
    "text_only": "Afficher uniquement les textes",
    "validate": "Valider les traductions",
    "search": "Rechercher :",
    "clear": "Effacer",
    "entries": "Entrées",
    "status": "État",
    "text": "Texte",
    "original": "Texte original",
    "translation": "Traduction",
    "show_hidden": "Afficher les octets/commandes masqués",
    "preserved": "Octets préservés",
    "translated": "Traduit",
    "pending": "En attente",
    "command": "Commande",
    "none_hidden": "✓ Aucune commande masquée",
    "hidden": "⚙ {count} bloc(s) préservé(s) · {size} octets",
    "unavailable": "Octets masqués indisponibles",
    "no_hidden": "Aucun octet masqué trouvé.",
    "no_project": "Aucun projet ouvert",
    "dictionary_required": "Dictionnaire nécessaire",
    "open_dictionary_first": "Ouvrez d'abord le dictionnaire.",
    "project_required": "Projet nécessaire",
    "open_project_first": "Ouvrez d'abord un BIN ou un projet JSON.",
    "loaded_dictionary": "Dictionnaire chargé : {name}",
    "opened_bin": "BIN ouvert : {name} — {count} entrées",
    "opened_project": "Projet ouvert : {name} — {count} entrées",
    "saved_project": "Projet enregistré : {name}",
    "exported_bin": "BIN exporté : {name}",
    "warnings": "Avertissements du dictionnaire",
    "validation": "Validation",
    "valid": "Aucun caractère invalide trouvé.",
    "invalid": "Caractères invalides",
    "imported": "Importation terminée",
    "import_result": "Importées : {a}\nIgnorées : {b}",
    "old_project": (
        "[Ancien projet sans octets raw]\n\n"
        "Ouvrez le BIN original et créez un nouveau projet."
    ),
    "raw_missing": (
        "Cette entrée ne contient pas les octets raw originaux.\n\n"
        "Ouvrez le BIN original et créez un nouveau projet."
    ),
    "separator": "──────── ⚙ commandes préservées ici ────────",
    "save_before_exit": "Enregistrer le projet avant de quitter ?",
    "bytes": "octets",
}

PORTUGUESE = {
    **ENGLISH,
    "title": "Riviera - Editor de Textos",
    "file": "Arquivo",
    "tools": "Ferramentas",
    "language": "Idioma",
    "dictionary": "Abrir dicionário",
    "open_bin": "Abrir BIN",
    "open_json": "Abrir projeto JSON",
    "save": "Salvar",
    "save_as": "Salvar projeto como...",
    "export_bin": "Exportar BIN",
    "export_dump": "Exportar dump antigo",
    "import_dump": "Importar dump antigo",
    "exit": "Sair",
    "show_all": "Mostrar todas",
    "translated_only": "Mostrar somente traduzidas",
    "pending_only": "Mostrar somente pendentes",
    "text_only": "Mostrar somente textos",
    "validate": "Validar traduções",
    "search": "Buscar:",
    "clear": "Limpar",
    "entries": "Entradas",
    "status": "Estado",
    "text": "Texto",
    "original": "Texto original",
    "translation": "Tradução",
    "show_hidden": "Mostrar bytes ocultos/comandos",
    "preserved": "Bytes preservados",
    "translated": "Traduzida",
    "pending": "Pendente",
    "command": "Comando",
    "none_hidden": "✓ Nenhum comando oculto",
    "hidden": "⚙ {count} bloco(s) preservado(s) · {size} bytes",
    "unavailable": "Bytes ocultos indisponíveis",
    "no_hidden": "Nenhum byte oculto encontrado.",
    "no_project": "Nenhum projeto aberto",
    "dictionary_required": "Dicionário necessário",
    "open_dictionary_first": "Abra o dicionário primeiro.",
    "project_required": "Projeto necessário",
    "open_project_first": "Abra um BIN ou projeto JSON primeiro.",
    "loaded_dictionary": "Dicionário carregado: {name}",
    "opened_bin": "BIN aberto: {name} — {count} entradas",
    "opened_project": "Projeto aberto: {name} — {count} entradas",
    "saved_project": "Projeto salvo: {name}",
    "exported_bin": "BIN exportado: {name}",
    "warnings": "Avisos do dicionário",
    "validation": "Validação",
    "valid": "Nenhum caractere inválido encontrado.",
    "invalid": "Caracteres inválidos",
    "imported": "Importação concluída",
    "import_result": "Importadas: {a}\nIgnoradas: {b}",
    "old_project": (
        "[Projeto antigo sem bytes raw]\n\n"
        "Abra o BIN original e salve um projeto novo."
    ),
    "raw_missing": (
        "Esta entrada não possui os bytes raw originais.\n\n"
        "Abra o BIN original e salve um projeto novo."
    ),
    "separator": "──────── ⚙ comandos preservados aqui ────────",
    "save_before_exit": "Deseja salvar o projeto antes de sair?",
}

LANGUAGES = {
    "English": ENGLISH,
    "Español": SPANISH,
    "Français": FRENCH,
    "Português": PORTUGUESE,
}


class RivieraEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.language_name = "English"
        self.lang = LANGUAGES[self.language_name]
        self.language_var = tk.StringVar(
            value=self.language_name
        )

        self.table = None
        self.project = None
        self.dictionary_path = None
        self.project_path = None
        self.current_index = None
        self.filter_mode = "all"

        self.show_hidden_bytes = tk.BooleanVar(value=False)
        self.search_var = tk.StringVar()
        self.hidden_summary_var = tk.StringVar()

        self._create_menu()
        self._create_widgets()
        self._bind_shortcuts()

        self.protocol(
            "WM_DELETE_WINDOW",
            self._on_close,
        )

        self.title(self.tr("title"))
        self._update_hidden_summary()

    # ==============================================================
    # Idiomas
    # ==============================================================

    def tr(self, key, **values):
        text = self.lang.get(key, key)
        return text.format(**values) if values else text

    def change_language(self, name):
        if name not in LANGUAGES:
            return

        self.language_name = name
        self.lang = LANGUAGES[name]
        self.language_var.set(name)

        if self.project:
            self.project.language = name

        self._rebuild_menus()
        self._update_widget_texts()
        self._refresh_tree()
        self._update_hidden_summary()
        self._update_hidden_bytes()

        self.title(self.tr("title"))

    # ==============================================================
    # Menus
    # ==============================================================

    def _create_menu(self):
        self.menu_bar = tk.Menu(self)

        self.file_menu = tk.Menu(
            self.menu_bar,
            tearoff=False,
        )
        self.tools_menu = tk.Menu(
            self.menu_bar,
            tearoff=False,
        )
        self.language_menu = tk.Menu(
            self.menu_bar,
            tearoff=False,
        )

        # Guardamos os índices. Não usamos self.menu_bar.index(menu),
        # pois o Tkinter não aceita o objeto Menu como índice.
        self.file_menu_index = 0
        self.tools_menu_index = 1
        self.language_menu_index = 2

        self.menu_bar.add_cascade(
            label=self.tr("file"),
            menu=self.file_menu,
        )
        self.menu_bar.add_cascade(
            label=self.tr("tools"),
            menu=self.tools_menu,
        )
        self.menu_bar.add_cascade(
            label=self.tr("language"),
            menu=self.language_menu,
        )

        self.config(menu=self.menu_bar)
        self._rebuild_menus()

    def _rebuild_menus(self):
        self.file_menu.delete(0, tk.END)
        self.tools_menu.delete(0, tk.END)
        self.language_menu.delete(0, tk.END)

        # Atualiza os nomes File/Tools/Language.
        self.menu_bar.entryconfigure(
            self.file_menu_index,
            label=self.tr("file"),
        )
        self.menu_bar.entryconfigure(
            self.tools_menu_index,
            label=self.tr("tools"),
        )
        self.menu_bar.entryconfigure(
            self.language_menu_index,
            label=self.tr("language"),
        )

        # Arquivo
        self.file_menu.add_command(
            label=self.tr("dictionary"),
            command=self.open_dictionary,
        )
        self.file_menu.add_command(
            label=self.tr("open_bin"),
            command=self.open_bin,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=self.tr("open_json"),
            command=self.open_project,
        )
        self.file_menu.add_command(
            label=self.tr("save"),
            command=self.save_project,
        )
        self.file_menu.add_command(
            label=self.tr("save_as"),
            command=self.save_project_as,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=self.tr("export_bin"),
            command=self.export_bin,
        )
        self.file_menu.add_command(
            label=self.tr("export_dump"),
            command=self.export_dump,
        )
        self.file_menu.add_command(
            label=self.tr("import_dump"),
            command=self.import_dump,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=self.tr("exit"),
            command=self._on_close,
        )

        # Ferramentas
        self.tools_menu.add_command(
            label=self.tr("show_all"),
            command=lambda: self.set_filter("all"),
        )
        self.tools_menu.add_command(
            label=self.tr("translated_only"),
            command=lambda: self.set_filter("translated"),
        )
        self.tools_menu.add_command(
            label=self.tr("pending_only"),
            command=lambda: self.set_filter("untranslated"),
        )
        self.tools_menu.add_command(
            label=self.tr("text_only"),
            command=lambda: self.set_filter("text"),
        )
        self.tools_menu.add_separator()
        self.tools_menu.add_command(
            label=self.tr("validate"),
            command=self.validate_project,
        )

        # Idioma
        for language in LANGUAGES:
            self.language_menu.add_radiobutton(
                label=language,
                value=language,
                variable=self.language_var,
                command=lambda value=language: (
                    self.change_language(value)
                ),
            )

    # ==============================================================
    # Interface
    # ==============================================================

    def _create_widgets(self):
        top = ttk.Frame(self, padding=6)
        top.pack(fill=tk.X)

        self.dictionary_button = ttk.Button(
            top,
            text=self.tr("dictionary"),
            command=self.open_dictionary,
        )
        self.dictionary_button.pack(side=tk.LEFT, padx=3)

        self.open_bin_button = ttk.Button(
            top,
            text=self.tr("open_bin"),
            command=self.open_bin,
        )
        self.open_bin_button.pack(side=tk.LEFT, padx=3)

        self.open_json_button = ttk.Button(
            top,
            text=self.tr("open_json"),
            command=self.open_project,
        )
        self.open_json_button.pack(side=tk.LEFT, padx=3)

        self.save_button = ttk.Button(
            top,
            text=self.tr("save"),
            command=self.save_project,
        )
        self.save_button.pack(side=tk.LEFT, padx=3)

        self.export_button = ttk.Button(
            top,
            text=self.tr("export_bin"),
            command=self.export_bin,
        )
        self.export_button.pack(side=tk.LEFT, padx=3)

        self.validate_button = ttk.Button(
            top,
            text=self.tr("validate"),
            command=self.validate_project,
        )
        self.validate_button.pack(side=tk.LEFT, padx=3)

        self.search_label = ttk.Label(
            top,
            text=self.tr("search"),
        )
        self.search_label.pack(
            side=tk.LEFT,
            padx=(20, 4),
        )

        self.search_entry = ttk.Entry(
            top,
            textvariable=self.search_var,
            width=30,
        )
        self.search_entry.pack(side=tk.LEFT)

        self.search_var.trace_add(
            "write",
            self._search_changed,
        )

        self.clear_button = ttk.Button(
            top,
            text=self.tr("clear"),
            command=lambda: self.search_var.set(""),
        )
        self.clear_button.pack(side=tk.LEFT, padx=4)

        main = ttk.PanedWindow(
            self,
            orient=tk.HORIZONTAL,
        )
        main.pack(
            fill=tk.BOTH,
            expand=True,
            padx=6,
            pady=(0, 6),
        )

        self._create_entry_list(main)
        self._create_editor(main)

        self.status_var = tk.StringVar(
            value=self.tr("no_project")
        )

        ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=4,
        ).pack(
            fill=tk.X,
            side=tk.BOTTOM,
        )

    def _create_entry_list(self, parent):
        left = ttk.Frame(parent, padding=4)
        parent.add(left, weight=1)

        self.entries_label = ttk.Label(
            left,
            text=self.tr("entries"),
            font=("TkDefaultFont", 10, "bold"),
        )
        self.entries_label.pack(anchor=tk.W)

        self.entry_count_var = tk.StringVar(value="0")
        ttk.Label(
            left,
            textvariable=self.entry_count_var,
        ).pack(anchor=tk.W, pady=(2, 5))

        frame = ttk.Frame(left)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("index", "status", "text"),
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("index", text="#")
        self.tree.heading(
            "status",
            text=self.tr("status"),
        )
        self.tree.heading(
            "text",
            text=self.tr("text"),
        )

        self.tree.column(
            "index",
            width=55,
            anchor=tk.E,
        )
        self.tree.column(
            "status",
            width=120,
            anchor=tk.CENTER,
        )
        self.tree.column(
            "text",
            width=360,
            anchor=tk.W,
        )

        scroll_y = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.tree.yview,
        )
        scroll_x = ttk.Scrollbar(
            left,
            orient=tk.HORIZONTAL,
            command=self.tree.xview,
        )

        self.tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )
        scroll_y.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )
        scroll_x.pack(fill=tk.X)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self._entry_selected,
        )

    def _create_editor(self, parent):
        right = ttk.Frame(parent, padding=4)
        parent.add(right, weight=3)

        self.original_label = ttk.Label(
            right,
            text=self.tr("original"),
            font=("TkDefaultFont", 10, "bold"),
        )
        self.original_label.pack(anchor=tk.W)

        original_frame = ttk.Frame(right)
        original_frame.pack(
            fill=tk.X,
            pady=(5, 8),
        )

        self.original_text = tk.Text(
            original_frame,
            height=9,
            wrap=tk.WORD,
            background="#eeeeee",
            foreground="#222222",
            font=("TkDefaultFont", 11),
        )
        self.original_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        original_scroll = ttk.Scrollbar(
            original_frame,
            orient=tk.VERTICAL,
            command=self.original_text.yview,
        )
        original_scroll.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self.original_text.configure(
            yscrollcommand=original_scroll.set,
            state=tk.DISABLED,
        )

        header = ttk.Frame(right)
        header.pack(fill=tk.X, pady=(0, 5))

        self.hidden_check = ttk.Checkbutton(
            header,
            text=self.tr("show_hidden"),
            variable=self.show_hidden_bytes,
            command=self._toggle_hidden_bytes,
        )
        self.hidden_check.pack(side=tk.LEFT)

        self.hidden_summary_label = tk.Label(
            header,
            textvariable=self.hidden_summary_var,
            font=("TkDefaultFont", 9, "bold"),
            padx=8,
            pady=2,
        )
        self.hidden_summary_label.pack(
            side=tk.LEFT,
            padx=(12, 0),
        )

        self.hidden_frame = ttk.LabelFrame(
            right,
            text=self.tr("preserved"),
            padding=5,
        )

        hidden_inner = ttk.Frame(self.hidden_frame)
        hidden_inner.pack(fill=tk.BOTH, expand=True)

        self.hidden_text = tk.Text(
            hidden_inner,
            height=8,
            wrap=tk.NONE,
            font=("TkFixedFont", 10),
            background="#202020",
            foreground="#d0d0d0",
        )
        self.hidden_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        hidden_scroll = ttk.Scrollbar(
            hidden_inner,
            orient=tk.VERTICAL,
            command=self.hidden_text.yview,
        )
        hidden_scroll.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self.hidden_text.configure(
            yscrollcommand=hidden_scroll.set,
            state=tk.DISABLED,
        )

        self.hidden_frame.pack_forget()

        self.translation_label = ttk.Label(
            right,
            text=self.tr("translation"),
            font=("TkDefaultFont", 10, "bold"),
        )
        self.translation_label.pack(anchor=tk.W)

        translation_frame = ttk.Frame(right)
        translation_frame.pack(
            fill=tk.BOTH,
            expand=True,
            pady=(5, 0),
        )

        self.translation_text = tk.Text(
            translation_frame,
            wrap=tk.WORD,
            font=("TkDefaultFont", 11),
            undo=True,
        )
        self.translation_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        translation_scroll = ttk.Scrollbar(
            translation_frame,
            orient=tk.VERTICAL,
            command=self.translation_text.yview,
        )
        translation_scroll.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self.translation_text.configure(
            yscrollcommand=translation_scroll.set,
        )

        self.translation_text.bind(
            "<FocusOut>",
            self._translation_changed,
        )

    def _update_widget_texts(self):
        self.dictionary_button.configure(
            text=self.tr("dictionary")
        )
        self.open_bin_button.configure(
            text=self.tr("open_bin")
        )
        self.open_json_button.configure(
            text=self.tr("open_json")
        )
        self.save_button.configure(
            text=self.tr("save")
        )
        self.export_button.configure(
            text=self.tr("export_bin")
        )
        self.validate_button.configure(
            text=self.tr("validate")
        )
        self.search_label.configure(
            text=self.tr("search")
        )
        self.clear_button.configure(
            text=self.tr("clear")
        )
        self.entries_label.configure(
            text=self.tr("entries")
        )
        self.original_label.configure(
            text=self.tr("original")
        )
        self.translation_label.configure(
            text=self.tr("translation")
        )
        self.hidden_check.configure(
            text=self.tr("show_hidden")
        )
        self.hidden_frame.configure(
            text=self.tr("preserved")
        )

        self.tree.heading(
            "status",
            text=self.tr("status"),
        )
        self.tree.heading(
            "text",
            text=self.tr("text"),
        )

    def _bind_shortcuts(self):
        self.bind_all(
            "<Control-s>",
            lambda event: self.save_project(),
        )
        self.bind_all(
            "<Control-f>",
            self._focus_search,
        )
        self.bind_all(
            "<Control-Return>",
            lambda event: self.export_bin(),
        )

    # ==============================================================
    # Arquivos
    # ==============================================================

    def open_dictionary(self):
        path = filedialog.askopenfilename(
            title=self.tr("dictionary"),
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            self.table = Table.load(path)
            self.dictionary_path = path

            self.status_var.set(
                self.tr(
                    "loaded_dictionary",
                    name=os.path.basename(path),
                )
            )

            if self.table.warnings:
                messagebox.showwarning(
                    self.tr("warnings"),
                    "\n".join(self.table.warnings[:50]),
                )

            if self.project:
                self.project.dictionary_path = path
                self.project.dictionary_data = (
                    self.table.to_data()
                )
                self._refresh_tree()
                self._update_hidden_summary()
                self._update_hidden_bytes()

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def open_bin(self):
        if not self._require_table():
            return

        path = filedialog.askopenfilename(
            title=self.tr("open_bin"),
            filetypes=[
                ("BIN files", "*.bin"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            with open(path, "rb") as file:
                data = file.read()

            self.project = Project.from_bin(
                data,
                self.table,
                os.path.basename(path),
            )

            self.project.source_path = path
            self.project.dictionary_path = (
                self.dictionary_path or ""
            )
            self.project.dictionary_data = (
                self.table.to_data()
            )
            self.project.language = self.language_name

            self.project_path = None
            self.current_index = None

            self._refresh_tree()
            self._clear_editor()

            self.status_var.set(
                self.tr(
                    "opened_bin",
                    name=os.path.basename(path),
                    count=len(self.project.entries),
                )
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def open_project(self):
        path = filedialog.askopenfilename(
            title=self.tr("open_json"),
            filetypes=[
                ("JSON project", "*.json"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            project = Project.load(path)
            table = None

            # Primeiro usa o dicionário embutido no JSON.
            if project.dictionary_data:
                table = Table.from_data(
                    project.dictionary_data,
                    project.dictionary_path or None,
                )

            # Compatibilidade: tenta o caminho salvo.
            elif (
                project.dictionary_path
                and os.path.exists(project.dictionary_path)
            ):
                table = Table.load(
                    project.dictionary_path
                )

            # Compatibilidade com JSONs antigos.
            if table is None:
                dictionary_path = filedialog.askopenfilename(
                    title=self.tr("dictionary"),
                    filetypes=[
                        ("Text files", "*.txt"),
                        ("All files", "*.*"),
                    ],
                )

                if not dictionary_path:
                    return

                table = Table.load(dictionary_path)
                project.dictionary_path = dictionary_path
                project.dictionary_data = table.to_data()

            self.project = project
            self.table = table
            self.project_path = path
            self.dictionary_path = (
                project.dictionary_path or table.path
            )
            self.current_index = None

            if project.language in LANGUAGES:
                self.change_language(project.language)

            self._refresh_tree()
            self._clear_editor()

            self.status_var.set(
                self.tr(
                    "opened_project",
                    name=os.path.basename(path),
                    count=len(project.entries),
                )
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def _save_metadata(self):
        if not self.project:
            return

        self.project.language = self.language_name

        if self.dictionary_path:
            self.project.dictionary_path = (
                self.dictionary_path
            )

        if self.table:
            self.project.dictionary_data = (
                self.table.to_data()
            )

    def save_project(self):
        if not self._require_project():
            return

        self._save_current_entry()
        self._save_metadata()

        if not self.project_path:
            return self.save_project_as()

        try:
            self.project.save(self.project_path)
            self._refresh_tree()

            self.status_var.set(
                self.tr(
                    "saved_project",
                    name=os.path.basename(
                        self.project_path
                    ),
                )
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def save_project_as(self):
        if not self._require_project():
            return

        self._save_current_entry()
        self._save_metadata()

        path = filedialog.asksaveasfilename(
            title=self.tr("save_as"),
            defaultextension=".json",
            filetypes=[
                ("JSON project", "*.json"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            self.project.save(path)
            self.project_path = path
            self._refresh_tree()

            self.status_var.set(
                self.tr(
                    "saved_project",
                    name=os.path.basename(path),
                )
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def export_bin(self):
        if not self._require_project():
            return

        if not self._require_table():
            return

        self._save_current_entry()

        path = filedialog.asksaveasfilename(
            title=self.tr("export_bin"),
            defaultextension=".bin",
            filetypes=[
                ("BIN files", "*.bin"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            data = self.project.build(self.table)

            with open(path, "wb") as file:
                file.write(data)

            self.status_var.set(
                self.tr(
                    "exported_bin",
                    name=os.path.basename(path),
                )
            )

            messagebox.showinfo(
                self.tr("export_bin"),
                f"{path}\n\n{len(data)} bytes",
            )

        except BuildError as exc:
            details = "\n".join(
                f"Entry {index}: {error}"
                for index, error in exc.errors
            )
            messagebox.showerror(
                self.tr("invalid"),
                details,
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def export_dump(self):
        if not self._require_project():
            return

        self._save_current_entry()

        path = filedialog.asksaveasfilename(
            title=self.tr("export_dump"),
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            self.project.export_dump(path)

            messagebox.showinfo(
                self.tr("export_dump"),
                path,
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    def import_dump(self):
        if not self._require_project():
            return

        path = filedialog.askopenfilename(
            title=self.tr("import_dump"),
            filetypes=[
                ("Text files", "*.txt *.tsv"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            self._save_current_entry()

            imported, skipped = (
                self.project.import_dump(path)
            )

            self._refresh_tree()

            messagebox.showinfo(
                self.tr("imported"),
                self.tr(
                    "import_result",
                    a=imported,
                    b=skipped,
                ),
            )

        except Exception as exc:
            messagebox.showerror(
                self.tr("error"),
                str(exc),
            )

    # ==============================================================
    # Edição
    # ==============================================================

    def _entry_selected(self, event=None):
        selection = self.tree.selection()

        if not selection:
            return

        values = self.tree.item(
            selection[0]
        ).get("values", [])

        if not values:
            return

        index = int(values[0])

        if index == self.current_index:
            return

        self._save_current_entry()
        self._load_entry(index)

    def _load_entry(self, index):
        if not self.project:
            return

        entry = self.project.entries[index]
        self.current_index = index

        clean_text = self._editor_text(entry)
        display_text = self._display_original(entry)

        self.original_text.configure(state=tk.NORMAL)
        self.original_text.delete("1.0", tk.END)
        self.original_text.insert("1.0", display_text)
        self.original_text.configure(state=tk.DISABLED)

        self.translation_text.delete("1.0", tk.END)
        self.translation_text.insert(
            "1.0",
            entry.tr or clean_text,
        )

        self._update_hidden_summary()
        self._update_hidden_bytes()

        self.status_var.set(
            f"#{index} | pointers: {entry.ptrs} | "
            f"offset: 0x{entry.offset:X} | "
            f"{entry.osize} bytes"
        )

    def _editor_text(self, entry):
        if not self.table:
            return entry.orig

        raw = getattr(entry, "raw", b"")

        if not raw:
            return self.tr("old_project")

        try:
            return entry.editor_text(self.table)
        except Exception:
            return entry.orig

    def _display_original(self, entry):
        text = self._editor_text(entry)

        if not self._has_controls(entry):
            return text

        parts = text.split("\n\n")

        if len(parts) <= 1:
            return text

        separator = (
            f"\n\n{self.tr('separator')}\n\n"
        )

        return separator.join(parts)

    def _save_current_entry(self):
        if not self.project:
            return

        if self.current_index is None:
            return

        entry = self.project.entries[
            self.current_index
        ]

        value = self.translation_text.get(
            "1.0",
            "end-1c",
        )

        if value == self._editor_text(entry):
            entry.tr = ""
        else:
            entry.tr = value

    def _translation_changed(self, event=None):
        self._save_current_entry()
        self._refresh_tree()

    # ==============================================================
    # Bytes ocultos
    # ==============================================================

    def _has_controls(self, entry):
        if not self.table:
            return False

        raw = getattr(entry, "raw", b"")

        if not raw:
            return False

        try:
            return any(
                kind == "control"
                for kind, value, block
                in self.table.split_text_runs(raw)
            )
        except Exception:
            return False

    def _update_hidden_summary(self):
        if not hasattr(self, "hidden_summary_label"):
            return

        if not self.project or self.current_index is None:
            self.hidden_summary_var.set(
                self.tr("none_hidden")
            )
            self.hidden_summary_label.configure(
                foreground="#146c2e",
                background="#d1e7dd",
            )
            return

        if not self.table:
            self.hidden_summary_var.set(
                self.tr("unavailable")
            )
            return

        entry = self.project.entries[
            self.current_index
        ]
        raw = getattr(entry, "raw", b"")

        if not raw:
            self.hidden_summary_var.set(
                self.tr("unavailable")
            )
            self.hidden_summary_label.configure(
                foreground="#9b1c1c",
                background="#f8d7da",
            )
            return

        try:
            controls = [
                run
                for run in self.table.split_text_runs(raw)
                if run[0] == "control"
            ]
        except Exception:
            self.hidden_summary_var.set(
                self.tr("unavailable")
            )
            return

        count = len(controls)
        size = sum(len(run[2]) for run in controls)

        if size == 0:
            self.hidden_summary_var.set(
                self.tr("none_hidden")
            )
            self.hidden_summary_label.configure(
                foreground="#146c2e",
                background="#d1e7dd",
            )
        else:
            self.hidden_summary_var.set(
                self.tr(
                    "hidden",
                    count=count,
                    size=size,
                )
            )
            self.hidden_summary_label.configure(
                foreground="#9a6700",
                background="#fff3cd",
            )

    def _toggle_hidden_bytes(self):
        if self.show_hidden_bytes.get():
            self.hidden_frame.pack(
                fill=tk.BOTH,
                expand=False,
                before=self.translation_label,
            )
            self._update_hidden_bytes()
        else:
            self.hidden_frame.pack_forget()

    def _set_hidden_text(self, text):
        self.hidden_text.configure(state=tk.NORMAL)
        self.hidden_text.delete("1.0", tk.END)
        self.hidden_text.insert("1.0", text)
        self.hidden_text.configure(state=tk.DISABLED)

    def _update_hidden_bytes(self):
        if not self.show_hidden_bytes.get():
            return

        if not self.project or self.current_index is None:
            self._set_hidden_text("")
            return

        entry = self.project.entries[
            self.current_index
        ]
        raw = getattr(entry, "raw", b"")

        if not raw:
            self._set_hidden_text(
                self.tr("raw_missing")
            )
            return

        output = []
        relative = 0

        for kind, display, block in (
            self.table.split_text_runs(raw)
        ):
            if kind == "control":
                hex_bytes = " ".join(
                    f"{byte:02x}"
                    for byte in block
                )
                absolute = entry.offset + relative

                output.append(
                    f"{self.tr('rel')} +{relative:04x} | "
                    f"{self.tr('abs')} +{absolute:08x}\n"
                    f"{self.tr('bytes')}: {hex_bytes}\n"
                    f"{self.tr('tags')}: {display}\n"
                )

            relative += len(block)

        self._set_hidden_text(
            "\n".join(output).rstrip()
            if output
            else self.tr("no_hidden")
        )

    # ==============================================================
    # Lista, busca e filtros
    # ==============================================================

    def _refresh_tree(self):
        self.tree.delete(
            *self.tree.get_children()
        )

        if not self.project:
            self.entry_count_var.set("0")
            return

        query = self.search_var.get().lower().strip()
        visible = 0

        for index, entry in enumerate(
            self.project.entries
        ):
            translated = bool(entry.tr)

            if (
                self.filter_mode == "translated"
                and not translated
            ):
                continue

            if (
                self.filter_mode == "untranslated"
                and translated
            ):
                continue

            if (
                self.filter_mode == "text"
                and not entry.has_text
            ):
                continue

            clean_text = self._editor_text(entry)

            searchable = (
                f"{index}\n{clean_text}\n{entry.tr}"
            ).lower()

            if query and query not in searchable:
                continue

            if translated:
                status = self.tr("translated")
            elif entry.has_text:
                status = self.tr("pending")
            else:
                status = self.tr("command")

            if self._has_controls(entry):
                status = "⚙ " + status

            preview = clean_text.replace(
                "\n",
                "\\n",
            )

            if len(preview) > 90:
                preview = preview[:87] + "..."

            self.tree.insert(
                "",
                tk.END,
                values=(index, status, preview),
            )

            visible += 1

        self.entry_count_var.set(
            f"{visible} / {len(self.project.entries)}"
        )

        if self.current_index is not None:
            for item in self.tree.get_children():
                values = self.tree.item(item).get(
                    "values",
                    [],
                )

                if values and int(values[0]) == self.current_index:
                    self.tree.selection_set(item)
                    self.tree.focus(item)
                    self.tree.see(item)
                    break

    def set_filter(self, mode):
        self._save_current_entry()
        self.filter_mode = mode
        self._refresh_tree()

    def _search_changed(self, *args):
        self._save_current_entry()
        self._refresh_tree()

    # ==============================================================
    # Validação e utilidades
    # ==============================================================

    def validate_project(self):
        if not self._require_project():
            return

        if not self._require_table():
            return

        self._save_current_entry()
        errors = []

        for index, entry in enumerate(
            self.project.entries
        ):
            if not entry.tr:
                continue

            invalid = self.table.invalid_spans(entry.tr)

            if invalid:
                snippets = [
                    repr(entry.tr[start:end])
                    for start, end in invalid[:10]
                ]
                errors.append(
                    f"Entry {index}: "
                    f"{', '.join(snippets)}"
                )

        if errors:
            messagebox.showerror(
                self.tr("invalid"),
                "\n".join(errors[:100]),
            )
        else:
            messagebox.showinfo(
                self.tr("validation"),
                self.tr("valid"),
            )

    def _require_table(self):
        if self.table is None:
            messagebox.showwarning(
                self.tr("dictionary_required"),
                self.tr("open_dictionary_first"),
            )
            return False

        return True

    def _require_project(self):
        if self.project is None:
            messagebox.showwarning(
                self.tr("project_required"),
                self.tr("open_project_first"),
            )
            return False

        return True

    def _clear_editor(self):
        self.current_index = None

        self.original_text.configure(state=tk.NORMAL)
        self.original_text.delete("1.0", tk.END)
        self.original_text.configure(state=tk.DISABLED)

        self.translation_text.delete("1.0", tk.END)
        self._set_hidden_text("")
        self._update_hidden_summary()

    def _focus_search(self, event=None):
        self.search_entry.focus_set()
        self.search_entry.selection_range(0, tk.END)
        return "break"

    def _on_close(self):
        if self.project:
            answer = messagebox.askyesnocancel(
                self.tr("exit"),
                self.tr("save_before_exit"),
            )

            if answer is None:
                return

            if answer:
                self.save_project()

        self.destroy()


def main():
    app = RivieraEditor()
    app.mainloop()


if __name__ == "__main__":
    main()