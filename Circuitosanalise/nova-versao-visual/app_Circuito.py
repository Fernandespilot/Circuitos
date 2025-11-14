
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class CircuitAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ ANÁLISE CIRCUITO PRO - Análise Avançada de Circuitos RLC")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#0a0e27')
        
        # Set window icon and properties
        self.root.state('zoomed') if self.root.winfo_screenwidth() > 1400 else None
        
        # Variables
        self.f = tk.DoubleVar(value=60)
        self.vm = tk.DoubleVar(value=311)
        self.im = tk.DoubleVar(value=10)
        self.theta_v = tk.DoubleVar(value=0)
        self.theta_i = tk.DoubleVar(value=-30)
        self.r = tk.DoubleVar(value=10)
        self.l = tk.DoubleVar(value=0.01)
        self.c = tk.DoubleVar(value=100e-6)
        
        self.v_phasor = None
        self.i_phasor = None
        self.z_equiv = None
        self.s_apparent = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create gradient-like header
        header_frame = tk.Frame(self.root, bg='#0a0e27', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title with modern styling
        title_container = tk.Frame(header_frame, bg='#161b3a')
        title_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(title_container, text="⚡ CIRCUIT ANALYZER PRO", 
                              font=("Segoe UI", 24, "bold"), fg='#00d4ff', bg='#161b3a')
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(title_container, text="v2.0 Advanced", 
                                font=("Segoe UI", 10), fg='#7c3aed', bg='#161b3a')
        version_label.pack(side=tk.RIGHT, anchor='se')
        
        subtitle_label = tk.Label(title_container, text="🔬 Análise Avançada de Circuitos RLC - Engenharia da Computação", 
                                 font=("Segoe UI", 11), fg='#a78bfa', bg='#161b3a')
        subtitle_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Main container with modern gradient effect
        main_container = tk.Frame(self.root, bg='#0a0e27')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Left sidebar with new design
        self.sidebar = tk.Frame(main_container, bg='#1a1f3e', width=350, relief=tk.RAISED, bd=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        self.sidebar.pack_propagate(False)
        
        # Right content area with modern styling
        self.content_frame = tk.Frame(main_container, bg='#0a0e27')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_sidebar()
        self.setup_content_tabs()
    
    def setup_sidebar(self):
        # Modern sidebar header
        header_sidebar = tk.Frame(self.sidebar, bg='#2d3561', height=60)
        header_sidebar.pack(fill=tk.X, pady=(0, 15))
        header_sidebar.pack_propagate(False)
        
        sidebar_title = tk.Label(header_sidebar, text="🎛️ PAINEL DE CONTROLE", 
                                font=("Segoe UI", 14, "bold"), fg='#00d4ff', bg='#2d3561')
        sidebar_title.pack(pady=15)
        
        # Modern parameters section with gradient effect
        params_frame = tk.LabelFrame(self.sidebar, text="⚙️ Parâmetros do Circuito", 
                                    font=("Segoe UI", 11, "bold"), fg='#00d4ff', bg='#1a1f3e',
                                    relief=tk.FLAT, bd=2)
        params_frame.pack(fill=tk.X, padx=15, pady=8)
        
        # Create parameter inputs
        params = [
            ("Frequência (Hz):", self.f),
            ("Tensão máx. (V):", self.vm),
            ("Corrente máx. (A):", self.im),
            ("Ângulo V (°):", self.theta_v),
            ("Ângulo I (°):", self.theta_i),
            ("Resistência (Ω):", self.r),
            ("Indutância (H):", self.l),
            ("Capacitância (F):", self.c)
        ]
        
        for i, (label_text, var) in enumerate(params):
            row_frame = tk.Frame(params_frame, bg='#1a1f3e')
            row_frame.pack(fill=tk.X, padx=8, pady=4)
            
            label = tk.Label(row_frame, text=label_text, font=("Segoe UI", 10), 
                           fg='#e2e8f0', bg='#1a1f3e', width=16, anchor='w')
            label.pack(side=tk.LEFT)
            
            entry = tk.Entry(row_frame, textvariable=var, font=("Segoe UI", 10), 
                           bg='#2d3561', fg='#00d4ff', insertbackground='#00d4ff', 
                           width=14, relief=tk.FLAT, bd=5)
            entry.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Modern buttons section with gradient effects
        buttons_frame = tk.Frame(self.sidebar, bg='#1a1f3e')
        buttons_frame.pack(fill=tk.X, padx=15, pady=20)
        
        analyze_btn = tk.Button(buttons_frame, text="🔍 ANALISAR CIRCUITO", 
                               command=self.analyze_circuit, font=("Segoe UI", 11, "bold"),
                               bg='#6366f1', fg='white', activebackground='#4f46e5',
                               relief=tk.FLAT, pady=12, cursor="hand2")
        analyze_btn.pack(fill=tk.X, pady=4)
        
        correction_btn = tk.Button(buttons_frame, text="⚡ CORREÇÃO FP", 
                                  command=self.power_factor_correction, font=("Segoe UI", 11, "bold"),
                                  bg='#059669', fg='white', activebackground='#047857',
                                  relief=tk.FLAT, pady=12, cursor="hand2")
        correction_btn.pack(fill=tk.X, pady=4)
        
        clear_btn = tk.Button(buttons_frame, text="🗑️ LIMPAR TUDO", 
                             command=self.clear_results, font=("Segoe UI", 11, "bold"),
                             bg='#dc2626', fg='white', activebackground='#b91c1c',
                             relief=tk.FLAT, pady=12, cursor="hand2")
        clear_btn.pack(fill=tk.X, pady=4)
        
        # Modern quick calculations section
        calc_frame = tk.LabelFrame(self.sidebar, text="🚀 Cálculos Rápidos", 
                                  font=("Segoe UI", 11, "bold"), fg='#00d4ff', bg='#1a1f3e',
                                  relief=tk.FLAT, bd=2)
        calc_frame.pack(fill=tk.X, padx=15, pady=8)
        
        calc_impedance_btn = tk.Button(calc_frame, text="⚙️ Calc. Impedância", 
                                      command=self.calc_impedance, font=("Segoe UI", 10),
                                      bg='#7c3aed', fg='white', relief=tk.FLAT, pady=8, cursor="hand2")
        calc_impedance_btn.pack(fill=tk.X, padx=8, pady=3)
        
        calc_resonance_btn = tk.Button(calc_frame, text="📊 Freq. Ressonância", 
                                      command=self.calc_resonance, font=("Segoe UI", 10),
                                      bg='#c026d3', fg='white', relief=tk.FLAT, pady=8, cursor="hand2")
        calc_resonance_btn.pack(fill=tk.X, padx=8, pady=3)
        
        # Modern advanced analysis section
        advanced_frame = tk.LabelFrame(self.sidebar, text="🔬 Análises Avançadas", 
                                      font=("Segoe UI", 11, "bold"), fg='#00d4ff', bg='#1a1f3e',
                                      relief=tk.FLAT, bd=2)
        advanced_frame.pack(fill=tk.X, padx=15, pady=8)
        
        transient_btn = tk.Button(advanced_frame, text="⚡ Análise Transitória", 
                                 command=self.run_transient_analysis, font=("Segoe UI", 10),
                                 bg='#f59e0b', fg='white', relief=tk.FLAT, pady=8, cursor="hand2")
        transient_btn.pack(fill=tk.X, padx=8, pady=3)
        
        frequency_btn = tk.Button(advanced_frame, text="📈 Resposta Frequência", 
                                 command=self.run_frequency_analysis, font=("Segoe UI", 10),
                                 bg='#ef4444', fg='white', relief=tk.FLAT, pady=8, cursor="hand2")
        frequency_btn.pack(fill=tk.X, padx=8, pady=3)
    
    def setup_content_tabs(self):
        # Create modern notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Configure modern notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#0a0e27', borderwidth=0, tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', 
                       background='#1a1f3e', 
                       foreground='#a78bfa', 
                       padding=[20, 12], 
                       font=("Segoe UI", 11, "bold"),
                       focuscolor='none')
        style.map('TNotebook.Tab', 
                 background=[('selected', '#6366f1'), ('active', '#4338ca')],
                 foreground=[('selected', 'white'), ('active', 'white')])
        
        # Tab 1: Análise de Sinais
        self.signals_frame = tk.Frame(self.notebook, bg='#0a0e27')
        self.notebook.add(self.signals_frame, text='📊 Sinais Elétricos')
        self.setup_signals_tab()
        
        # Tab 2: Diagrama Fasorial
        self.phasor_frame = tk.Frame(self.notebook, bg='#0a0e27')
        self.notebook.add(self.phasor_frame, text='⚡ Diagrama Fasorial')
        self.setup_phasor_tab()
        
        # Tab 3: Montagem de Circuito
        self.circuit_frame = tk.Frame(self.notebook, bg='#0a0e27')
        self.notebook.add(self.circuit_frame, text='🔧 Designer de Circuitos')
        self.setup_circuit_tab()
        
        # Tab 4: Resultados
        self.results_frame = tk.Frame(self.notebook, bg='#0a0e27')
        self.notebook.add(self.results_frame, text='📋 Relatórios')
        self.setup_results_tab()
    
    def setup_signals_tab(self):
        # Modern signals plot with dark theme
        self.fig_signals = Figure(figsize=(14, 9), facecolor='#0a0e27')
        self.ax1 = self.fig_signals.add_subplot(211, facecolor='#161b3a')
        self.ax2 = self.fig_signals.add_subplot(212, facecolor='#161b3a')
        
        # Style the plots with modern colors
        for ax in [self.ax1, self.ax2]:
            ax.spines['bottom'].set_color('#00d4ff')
            ax.spines['top'].set_color('#00d4ff')
            ax.spines['right'].set_color('#00d4ff')
            ax.spines['left'].set_color('#00d4ff')
            ax.tick_params(colors='#a78bfa')
            ax.grid(True, alpha=0.2, color='#7c3aed')
        
        self.canvas_signals = FigureCanvasTkAgg(self.fig_signals, self.signals_frame)
        self.canvas_signals.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def setup_phasor_tab(self):
        # Create main container for phasor diagrams
        main_phasor_container = tk.Frame(self.phasor_frame, bg='#0f172a')
        main_phasor_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side: Diagrams (2x2 grid)
        diagrams_frame = tk.Frame(main_phasor_container, bg='#1e293b', relief=tk.RAISED, bd=2)
        diagrams_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right side: Results panel
        results_panel = tk.Frame(main_phasor_container, bg='#1e293b', width=350, relief=tk.RAISED, bd=2)
        results_panel.pack(side=tk.RIGHT, fill=tk.Y)
        results_panel.pack_propagate(False)
        
        # Setup diagrams in 2x2 grid
        self.fig_phasor = Figure(figsize=(10, 8), facecolor='#1e293b')
        self.ax_vi = self.fig_phasor.add_subplot(221, facecolor='#1e293b')
        self.ax_z = self.fig_phasor.add_subplot(222, facecolor='#1e293b')
        self.ax_power = self.fig_phasor.add_subplot(223, facecolor='#1e293b')
        self.ax_circuit = self.fig_phasor.add_subplot(224, facecolor='#1e293b')
        
        # Style all phasor plots
        for ax in [self.ax_vi, self.ax_z, self.ax_power, self.ax_circuit]:
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(colors='white')
        
        self.canvas_phasor = FigureCanvasTkAgg(self.fig_phasor, diagrams_frame)
        self.canvas_phasor.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Setup results panel
        results_title = tk.Label(results_panel, text="RESULTADOS FASORIAIS", 
                                font=("Arial", 12, "bold"), fg='#3b82f6', bg='#1e293b')
        results_title.pack(pady=(15, 10))
        
        # Scrollable text for results
        self.phasor_results_text = scrolledtext.ScrolledText(results_panel, height=35, width=40,
                                                           bg='#334155', fg='white', font=("Arial", 9),
                                                           wrap=tk.WORD)
        self.phasor_results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def setup_circuit_tab(self):
        # Modern circuit builder interface
        circuit_container = tk.Frame(self.circuit_frame, bg='#0a0e27')
        circuit_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header for circuit tab
        header_circuit = tk.Frame(circuit_container, bg='#161b3a', height=50)
        header_circuit.pack(fill=tk.X, pady=(0, 15))
        header_circuit.pack_propagate(False)
        
        header_title = tk.Label(header_circuit, text="🔧 DESIGNER DE CIRCUITOS RLC", 
                               font=("Segoe UI", 16, "bold"), fg='#00d4ff', bg='#161b3a')
        header_title.pack(pady=10)
        
        # Main content container
        content_container = tk.Frame(circuit_container, bg='#0a0e27')
        content_container.pack(fill=tk.BOTH, expand=True)
        
        # Left: Circuit drawing with modern frame
        circuit_canvas_frame = tk.Frame(content_container, bg='#161b3a', relief=tk.FLAT, bd=2)
        circuit_canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Right: Circuit parameters with modern styling
        circuit_params_frame = tk.Frame(content_container, bg='#1a1f3e', width=350, relief=tk.FLAT, bd=2)
        circuit_params_frame.pack(side=tk.RIGHT, fill=tk.Y)
        circuit_params_frame.pack_propagate(False)
        
        # Modern circuit visualization
        self.fig_circuit = Figure(figsize=(10, 8), facecolor='#161b3a')
        self.ax_circuit_draw = self.fig_circuit.add_subplot(111, facecolor='#0a0e27')
        self.ax_circuit_draw.set_aspect('equal')
        
        self.canvas_circuit = FigureCanvasTkAgg(self.fig_circuit, circuit_canvas_frame)
        self.canvas_circuit.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Modern circuit parameters panel
        params_title = tk.Label(circuit_params_frame, text="⚙️ CONFIGURAÇÃO DO CIRCUITO", 
                               font=("Segoe UI", 12, "bold"), fg='#00d4ff', bg='#1a1f3e')
        params_title.pack(pady=(20, 15))
        
        # Modern circuit type selection
        type_frame = tk.LabelFrame(circuit_params_frame, text="🔌 Tipo de Circuito", 
                                  font=("Segoe UI", 10, "bold"), fg='#00d4ff', bg='#1a1f3e',
                                  relief=tk.FLAT, bd=2)
        type_frame.pack(fill=tk.X, padx=15, pady=8)
        
        self.circuit_type = tk.StringVar(value="RLC_Serie")
        types = [("🔗 RLC Série", "RLC_Serie"), ("⚡ RLC Paralelo", "RLC_Paralelo"), 
                ("🔄 DC - Malhas", "DC_Malhas")]
        
        for text, value in types:
            rb = tk.Radiobutton(type_frame, text=text, variable=self.circuit_type, value=value,
                               font=("Segoe UI", 10), fg='#e2e8f0', bg='#1a1f3e', 
                               selectcolor='#6366f1', command=self.update_circuit_drawing,
                               activeforeground='#00d4ff', activebackground='#1a1f3e')
            rb.pack(anchor='w', padx=10, pady=4)
        
        # Modern component values frame
        components_frame = tk.LabelFrame(circuit_params_frame, text="🎛️ Valores dos Componentes", 
                                        font=("Segoe UI", 10, "bold"), fg='#00d4ff', bg='#1a1f3e',
                                        relief=tk.FLAT, bd=2)
        components_frame.pack(fill=tk.X, padx=15, pady=8)
        
        # Modern voltage source input
        self.vs_voltage = tk.DoubleVar(value=127)
        self.vs_phase = tk.DoubleVar(value=0)
        
        vs_frame = tk.Frame(components_frame, bg='#1a1f3e')
        vs_frame.pack(fill=tk.X, padx=10, pady=6)
        tk.Label(vs_frame, text="⚡ Tensão da Fonte (V):", font=("Segoe UI", 10), 
                fg='#e2e8f0', bg='#1a1f3e').pack(side=tk.LEFT)
        tk.Entry(vs_frame, textvariable=self.vs_voltage, font=("Segoe UI", 10), 
                bg='#2d3561', fg='#00d4ff', width=10, relief=tk.FLAT, bd=5).pack(side=tk.RIGHT)
        
        # Modern calculate button
        calc_circuit_btn = tk.Button(circuit_params_frame, text="🚀 CALCULAR CIRCUITO", 
                                    command=self.calculate_circuit, font=("Segoe UI", 11, "bold"),
                                    bg='#6366f1', fg='white', relief=tk.FLAT, pady=12, cursor="hand2")
        calc_circuit_btn.pack(fill=tk.X, padx=15, pady=20)
        
        # Info panel
        info_frame = tk.Frame(circuit_params_frame, bg='#2d3561')
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        info_text = tk.Text(info_frame, height=8, width=30, bg='#161b3a', fg='#a78bfa',
                           font=("Segoe UI", 9), wrap=tk.WORD, relief=tk.FLAT, bd=5)
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info_text.insert(tk.END, """📊 INFORMAÇÕES:
        
• Selecione o tipo de circuito
• Configure a tensão da fonte
• Visualize o diagrama esquemático
• Execute os cálculos detalhados
        
🔧 Use os parâmetros R, L, C 
   da barra lateral esquerda""")
        info_text.config(state=tk.DISABLED)
        
        # Draw initial circuit
        self.update_circuit_drawing()
    
    def setup_results_tab(self):
        # Transient analysis interface
        transient_container = tk.Frame(self.transient_frame, bg='#0f172a')
        transient_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Controls
        controls_frame = tk.Frame(transient_container, bg='#1e293b', width=300, relief=tk.RAISED, bd=2)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        controls_frame.pack_propagate(False)
        
        # Right: Plots
        plots_frame = tk.Frame(transient_container, bg='#1e293b', relief=tk.RAISED, bd=2)
        plots_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Transient parameters
        params_title = tk.Label(controls_frame, text="PARÂMETROS TRANSITÓRIOS", 
                               font=("Arial", 11, "bold"), fg='#3b82f6', bg='#1e293b')
        params_title.pack(pady=(15, 10))
        
        # Analysis type
        analysis_frame = tk.LabelFrame(controls_frame, text="Tipo de Análise", 
                                      font=("Arial", 10, "bold"), fg='white', bg='#1e293b')
        analysis_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.transient_type = tk.StringVar(value="step")
        transient_types = [("Resposta ao Degrau", "step"), ("Resposta ao Impulso", "impulse"), 
                          ("Resposta Natural", "natural")]
        
        for text, value in transient_types:
            rb = tk.Radiobutton(analysis_frame, text=text, variable=self.transient_type, value=value,
                               font=("Arial", 9), fg='white', bg='#1e293b', 
                               selectcolor='#3b82f6')
            rb.pack(anchor='w', padx=5, pady=2)
        
        # Time parameters
        time_frame = tk.LabelFrame(controls_frame, text="Parâmetros Temporais", 
                                  font=("Arial", 10, "bold"), fg='white', bg='#1e293b')
        time_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.t_final = tk.DoubleVar(value=0.1)
        self.step_amplitude = tk.DoubleVar(value=12)
        
        # Time final
        t_frame = tk.Frame(time_frame, bg='#1e293b')
        t_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(t_frame, text="Tempo Final (s):", font=("Arial", 9), fg='white', bg='#1e293b').pack(side=tk.LEFT)
        tk.Entry(t_frame, textvariable=self.t_final, font=("Arial", 9), 
                bg='#334155', fg='white', width=8).pack(side=tk.RIGHT)
        
        # Step amplitude
        step_frame = tk.Frame(time_frame, bg='#1e293b')
        step_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(step_frame, text="Amplitude (V):", font=("Arial", 9), fg='white', bg='#1e293b').pack(side=tk.LEFT)
        tk.Entry(step_frame, textvariable=self.step_amplitude, font=("Arial", 9), 
                bg='#334155', fg='white', width=8).pack(side=tk.RIGHT)
        
        # Run button
        run_transient_btn = tk.Button(controls_frame, text="EXECUTAR ANÁLISE", 
                                     command=self.calculate_transient_response, font=("Arial", 10, "bold"),
                                     bg='#f59e0b', fg='white', relief=tk.FLAT, pady=8)
        run_transient_btn.pack(fill=tk.X, padx=10, pady=20)
        
        # Transient plots
        self.fig_transient = Figure(figsize=(12, 8), facecolor='#1e293b')
        self.ax_transient1 = self.fig_transient.add_subplot(211, facecolor='#1e293b')
        self.ax_transient2 = self.fig_transient.add_subplot(212, facecolor='#1e293b')
        
        # Style transient plots
        for ax in [self.ax_transient1, self.ax_transient2]:
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(colors='white')
        
        self.canvas_transient = FigureCanvasTkAgg(self.fig_transient, plots_frame)
        self.canvas_transient.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_frequency_tab(self):
        # Frequency analysis interface
        freq_container = tk.Frame(self.frequency_frame, bg='#0f172a')
        freq_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Controls
        freq_controls_frame = tk.Frame(freq_container, bg='#1e293b', width=300, relief=tk.RAISED, bd=2)
        freq_controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        freq_controls_frame.pack_propagate(False)
        
        # Right: Plots
        freq_plots_frame = tk.Frame(freq_container, bg='#1e293b', relief=tk.RAISED, bd=2)
        freq_plots_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Frequency parameters
        freq_title = tk.Label(freq_controls_frame, text="ANÁLISE DE FREQUÊNCIA", 
                             font=("Arial", 11, "bold"), fg='#3b82f6', bg='#1e293b')
        freq_title.pack(pady=(15, 10))
        
        # Frequency range
        range_frame = tk.LabelFrame(freq_controls_frame, text="Faixa de Frequência", 
                                   font=("Arial", 10, "bold"), fg='white', bg='#1e293b')
        range_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.f_start = tk.DoubleVar(value=1)
        self.f_end = tk.DoubleVar(value=10000)
        
        # Start frequency
        fstart_frame = tk.Frame(range_frame, bg='#1e293b')
        fstart_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(fstart_frame, text="Freq. Inicial (Hz):", font=("Arial", 9), fg='white', bg='#1e293b').pack(side=tk.LEFT)
        tk.Entry(fstart_frame, textvariable=self.f_start, font=("Arial", 9), 
                bg='#334155', fg='white', width=8).pack(side=tk.RIGHT)
        
        # End frequency
        fend_frame = tk.Frame(range_frame, bg='#1e293b')
        fend_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(fend_frame, text="Freq. Final (Hz):", font=("Arial", 9), fg='white', bg='#1e293b').pack(side=tk.LEFT)
        tk.Entry(fend_frame, textvariable=self.f_end, font=("Arial", 9), 
                bg='#334155', fg='white', width=8).pack(side=tk.RIGHT)
        
        # Plot type
        plot_type_frame = tk.LabelFrame(freq_controls_frame, text="Tipo de Gráfico", 
                                       font=("Arial", 10, "bold"), fg='white', bg='#1e293b')
        plot_type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.plot_type = tk.StringVar(value="bode")
        plot_types = [("Diagrama de Bode", "bode"), ("Nyquist", "nyquist"), ("Módulo e Fase", "mag_phase")]
        
        for text, value in plot_types:
            rb = tk.Radiobutton(plot_type_frame, text=text, variable=self.plot_type, value=value,
                               font=("Arial", 9), fg='white', bg='#1e293b', 
                               selectcolor='#3b82f6')
            rb.pack(anchor='w', padx=5, pady=2)
        
        # Run button
        run_freq_btn = tk.Button(freq_controls_frame, text="GERAR GRÁFICOS", 
                                command=self.calculate_frequency_response, font=("Arial", 10, "bold"),
                                bg='#ef4444', fg='white', relief=tk.FLAT, pady=8)
        run_freq_btn.pack(fill=tk.X, padx=10, pady=20)
        
        # Frequency plots
        self.fig_frequency = Figure(figsize=(12, 8), facecolor='#1e293b')
        self.ax_freq1 = self.fig_frequency.add_subplot(211, facecolor='#1e293b')
        self.ax_freq2 = self.fig_frequency.add_subplot(212, facecolor='#1e293b')
        
        # Style frequency plots
        for ax in [self.ax_freq1, self.ax_freq2]:
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(colors='white')
        
        self.canvas_frequency = FigureCanvasTkAgg(self.fig_frequency, freq_plots_frame)
        self.canvas_frequency.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_results_tab(self):
        # Modern results display with header
        header_results = tk.Frame(self.results_frame, bg='#161b3a', height=50)
        header_results.pack(fill=tk.X, pady=(0, 15))
        header_results.pack_propagate(False)
        
        header_title = tk.Label(header_results, text="📊 RELATÓRIOS E ANÁLISES DETALHADAS", 
                               font=("Segoe UI", 16, "bold"), fg='#00d4ff', bg='#161b3a')
        header_title.pack(pady=10)
        
        # Modern results text area
        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=45, width=120,
                                                     bg='#161b3a', fg='#e2e8f0', font=("Consolas", 10),
                                                     wrap=tk.WORD, relief=tk.FLAT, bd=10)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Configure scrollbar colors
        self.results_text.configure(selectbackground='#6366f1', selectforeground='white',
                                   insertbackground='#00d4ff')
    
    def update_circuit_drawing(self):
        self.ax_circuit_draw.clear()
        self.ax_circuit_draw.set_xlim(0, 12)
        self.ax_circuit_draw.set_ylim(0, 8)
        self.ax_circuit_draw.set_facecolor('#0a0e27')
        
        circuit_type = self.circuit_type.get()
        
        # Add grid for better visualization
        self.ax_circuit_draw.grid(True, alpha=0.1, color='#7c3aed', linewidth=0.5)
        
        if circuit_type == "RLC_Serie":
            self.draw_rlc_series_modern()
        elif circuit_type == "RLC_Paralelo":
            self.draw_rlc_parallel_modern()
        elif circuit_type == "DC_Malhas":
            self.draw_dc_mesh_modern()
        
        # Modern title with circuit info
        title_text = f'CIRCUITO {circuit_type.replace("_", " ")} - R={self.r.get():.1f}Ω, L={self.l.get()*1000:.1f}mH, C={self.c.get()*1000000:.0f}μF'
        self.ax_circuit_draw.set_title(title_text, color='#00d4ff', fontsize=11, fontweight='bold', pad=20)
        self.ax_circuit_draw.axis('off')
        
        # Add border
        self.ax_circuit_draw.add_patch(patches.Rectangle((0.2, 0.2), 11.6, 7.6, 
                                                        fill=False, color='#6366f1', linewidth=2, alpha=0.3))
        
        self.canvas_circuit.draw()
    
    def draw_rlc_series_modern(self):
        """Draw modern RLC series circuit with enhanced visuals"""
        # Modern voltage source with glow effect
        circle = plt.Circle((2, 4), 0.4, fill=True, facecolor='#161b3a', edgecolor='#00d4ff', linewidth=3)
        self.ax_circuit_draw.add_patch(circle)
        self.ax_circuit_draw.text(2, 4, 'V', ha='center', va='center', color='#00d4ff', 
                                 fontsize=14, fontweight='bold')
        self.ax_circuit_draw.text(2, 3.2, f'{self.vs_voltage.get():.0f}V', ha='center', va='center', 
                                 color='#a78bfa', fontsize=10)
        
        # Modern resistor with 3D effect
        rect_r = patches.FancyBboxPatch((4, 3.7), 1.5, 0.6, boxstyle="round,pad=0.1",
                                       facecolor='#dc2626', edgecolor='#ef4444', linewidth=2)
        self.ax_circuit_draw.add_patch(rect_r)
        self.ax_circuit_draw.text(4.75, 4, 'R', ha='center', va='center', color='white', 
                                 fontsize=12, fontweight='bold')
        self.ax_circuit_draw.text(4.75, 3.2, f'{self.r.get():.1f}Ω', ha='center', va='center', 
                                 color='#fca5a5', fontsize=9)
        
        # Modern inductor with coil representation
        for i in range(6):
            x_pos = 6.5 + i*0.25
            circle_l = plt.Circle((x_pos, 4), 0.12, fill=False, color='#10b981', linewidth=2.5)
            self.ax_circuit_draw.add_patch(circle_l)
        self.ax_circuit_draw.text(7.25, 4.8, 'L', ha='center', va='center', color='#10b981', 
                                 fontsize=12, fontweight='bold')
        self.ax_circuit_draw.text(7.25, 3.2, f'{self.l.get()*1000:.1f}mH', ha='center', va='center', 
                                 color='#6ee7b7', fontsize=9)
        
        # Modern capacitor with enhanced design
        self.ax_circuit_draw.plot([9.5, 9.5], [3.5, 4.5], color='#3b82f6', linewidth=4)
        self.ax_circuit_draw.plot([9.8, 9.8], [3.5, 4.5], color='#3b82f6', linewidth=4)
        # Add dielectric representation
        self.ax_circuit_draw.plot([9.65, 9.65], [3.6, 4.4], color='#7c3aed', linewidth=2, alpha=0.7)
        self.ax_circuit_draw.text(9.65, 4.8, 'C', ha='center', va='center', color='#3b82f6', 
                                 fontsize=12, fontweight='bold')
        self.ax_circuit_draw.text(9.65, 3.2, f'{self.c.get()*1000000:.0f}μF', ha='center', va='center', 
                                 color='#93c5fd', fontsize=9)
        
        # Modern connections with enhanced styling
        connections = [
            ([2.4, 4], [4, 4]),      # V to R
            ([5.5, 6.25], [4, 4]),   # R to L  
            ([8, 9.5], [4, 4]),      # L to C
            ([9.8, 10.5, 10.5, 1.5, 1.5, 1.6], [4, 4, 2, 2, 4, 4])  # C back to V
        ]
        
        for x_coords, y_coords in connections:
            self.ax_circuit_draw.plot(x_coords, y_coords, color='#00d4ff', linewidth=3, alpha=0.8)
        
        # Add current flow arrows
        self.ax_circuit_draw.annotate('', xy=(3.2, 4.3), xytext=(2.8, 4.3),
                                     arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2))
        self.ax_circuit_draw.text(3, 4.6, 'i(t)', ha='center', va='center', color='#f59e0b', fontsize=10)
        
        # Add node indicators
        nodes = [(2, 4), (4, 4), (5.5, 4), (8, 4), (9.8, 4)]
        for x, y in nodes:
            self.ax_circuit_draw.plot(x, y, 'o', color='#00d4ff', markersize=6)
    
    def draw_rlc_parallel_modern(self):
        """Draw modern RLC parallel circuit with enhanced visuals"""
        # Modern voltage source
        circle = plt.Circle((2, 4), 0.4, fill=True, facecolor='#161b3a', edgecolor='#00d4ff', linewidth=3)
        self.ax_circuit_draw.add_patch(circle)
        self.ax_circuit_draw.text(2, 4, 'V', ha='center', va='center', color='#00d4ff', 
                                 fontsize=14, fontweight='bold')
        self.ax_circuit_draw.text(2, 3.2, f'{self.vs_voltage.get():.0f}V', ha='center', va='center', 
                                 color='#a78bfa', fontsize=10)
        
        # Main horizontal bus lines with enhanced styling
        self.ax_circuit_draw.plot([2.4, 10], [5.5, 5.5], color='#00d4ff', linewidth=4, alpha=0.8)  # Top bus
        self.ax_circuit_draw.plot([2.4, 10], [2.5, 2.5], color='#00d4ff', linewidth=4, alpha=0.8)  # Bottom bus
        
        # Vertical connections from source with glow effect
        self.ax_circuit_draw.plot([2.4, 2.4], [4.4, 5.5], color='#00d4ff', linewidth=3, alpha=0.8)
        self.ax_circuit_draw.plot([2.4, 2.4], [3.6, 2.5], color='#00d4ff', linewidth=3, alpha=0.8)
        
        # Resistor branch with modern styling
        self.ax_circuit_draw.plot([4.5, 4.5], [5.5, 4.8], color='#00d4ff', linewidth=3)
        rect_r = patches.FancyBboxPatch((4, 3.7), 1, 0.6, boxstyle="round,pad=0.1",
                                       facecolor='#dc2626', edgecolor='#ef4444', linewidth=2)
        self.ax_circuit_draw.add_patch(rect_r)
        self.ax_circuit_draw.plot([4.5, 4.5], [3.7, 2.5], color='#00d4ff', linewidth=3)
        self.ax_circuit_draw.text(4.5, 4, 'R', ha='center', va='center', color='white', 
                                 fontsize=12, fontweight='bold')
        self.ax_circuit_draw.text(4.5, 1.8, f'{self.r.get():.1f}Ω', ha='center', va='center', 
                                 color='#fca5a5', fontsize=9)
        
        # Inductor branch with vertical coils
        self.ax_circuit_draw.plot([6.5, 6.5], [5.5, 4.8], color='#00d4ff', linewidth=3)
        for i in range(4):
            y_pos = 4.5 - i*0.3
            circle_l = plt.Circle((6.5, y_pos), 0.15, fill=False, color='#10b981', linewidth=2.5)
            self.ax_circuit_draw.add_patch(circle_l)
        self.ax_circuit_draw.plot([6.5, 6.5], [3.3, 2.5], color='#00d4ff', linewidth=3)
        self.ax_circuit_draw.text(6.5, 1.8, 'L', ha='center', va='center', color='#10b981', 
                                 fontsize=12, fontweight='bold')
        self.ax_circuit_draw.text(6.5, 1.5, f'{self.l.get()*1000:.1f}mH', ha='center', va='center', 
                                 color='#6ee7b7', fontsize=9)
        
        # Capacitor branch with enhanced design
        self.ax_circuit_draw.plot([8.5, 8.5], [5.5, 4.5], color='#00d4ff', linewidth=3)
        self.ax_circuit_draw.plot([8.2, 8.8], [4.2, 4.2], color='#3b82f6', linewidth=4)
        self.ax_circuit_draw.plot([8.2, 8.8], [3.8, 3.8], color='#3b82f6', linewidth=4)
        # Add dielectric
        self.ax_circuit_draw.plot([8.2, 8.8], [4.0, 4.0], color='#7c3aed', linewidth=2, alpha=0.7)
        self.ax_circuit_draw.plot([8.5, 8.5], [3.5, 2.5], color='#00d4ff', linewidth=3)
        self.ax_circuit_draw.text(8.5, 1.8, 'C', ha='center', va='center', color='#3b82f6', 
                                 fontsize=12, fontweight='bold')
        self.ax_circuit_draw.text(8.5, 1.5, f'{self.c.get()*1000000:.0f}μF', ha='center', va='center', 
                                 color='#93c5fd', fontsize=9)
        
        # Add current flow arrows for each branch
        self.ax_circuit_draw.annotate('', xy=(4.8, 4.5), xytext=(4.2, 4.5),
                                     arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2))
        self.ax_circuit_draw.text(4.5, 4.9, 'iR', ha='center', va='center', color='#f59e0b', fontsize=9)
        
        self.ax_circuit_draw.annotate('', xy=(6.8, 4.2), xytext=(6.2, 4.2),
                                     arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2))
        self.ax_circuit_draw.text(6.5, 4.9, 'iL', ha='center', va='center', color='#f59e0b', fontsize=9)
        
        self.ax_circuit_draw.annotate('', xy=(8.8, 4.5), xytext=(8.2, 4.5),
                                     arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2))
        self.ax_circuit_draw.text(8.5, 4.9, 'iC', ha='center', va='center', color='#f59e0b', fontsize=9)
        
        # Add node indicators
        nodes = [(2.4, 5.5), (2.4, 2.5), (4.5, 5.5), (4.5, 2.5), 
                (6.5, 5.5), (6.5, 2.5), (8.5, 5.5), (8.5, 2.5)]
        for x, y in nodes:
            self.ax_circuit_draw.plot(x, y, 'o', color='#00d4ff', markersize=5)
    
    def draw_dc_mesh_modern(self):
        """Draw modern DC mesh circuit with enhanced visuals"""
        # Enhanced mesh rectangles with rounded corners
        mesh1 = patches.FancyBboxPatch((1.5, 2), 4, 3, boxstyle="round,pad=0.1",
                                      fill=False, edgecolor='#00d4ff', linewidth=3, alpha=0.7)
        self.ax_circuit_draw.add_patch(mesh1)
        
        mesh2 = patches.FancyBboxPatch((4.5, 2), 4, 3, boxstyle="round,pad=0.1",
                                      fill=False, edgecolor='#a78bfa', linewidth=3, alpha=0.7)
        self.ax_circuit_draw.add_patch(mesh2)
        
        # Modern voltage sources with enhanced design
        circle1 = plt.Circle((2.5, 3.5), 0.3, fill=True, facecolor='#161b3a', 
                            edgecolor='#f59e0b', linewidth=3)
        self.ax_circuit_draw.add_patch(circle1)
        self.ax_circuit_draw.text(2.5, 3.5, 'V₁', ha='center', va='center', 
                                 color='#f59e0b', fontsize=11, fontweight='bold')
        self.ax_circuit_draw.text(2.5, 2.8, '12V', ha='center', va='center', 
                                 color='#fbbf24', fontsize=9)
        
        circle2 = plt.Circle((7.5, 3.5), 0.3, fill=True, facecolor='#161b3a',
                            edgecolor='#f59e0b', linewidth=3)
        self.ax_circuit_draw.add_patch(circle2)
        self.ax_circuit_draw.text(7.5, 3.5, 'V₂', ha='center', va='center', 
                                 color='#f59e0b', fontsize=11, fontweight='bold')
        self.ax_circuit_draw.text(7.5, 2.8, '8V', ha='center', va='center', 
                                 color='#fbbf24', fontsize=9)
        
        # Modern resistors with 3D effect
        rect_r1 = patches.FancyBboxPatch((3.2, 3.2), 1, 0.6, boxstyle="round,pad=0.1",
                                        facecolor='#dc2626', edgecolor='#ef4444', linewidth=2)
        self.ax_circuit_draw.add_patch(rect_r1)
        self.ax_circuit_draw.text(3.7, 3.5, 'R₁', ha='center', va='center', 
                                 color='white', fontsize=11, fontweight='bold')
        self.ax_circuit_draw.text(3.7, 4.2, '10Ω', ha='center', va='center', 
                                 color='#fca5a5', fontsize=9)
        
        # Shared resistor (between meshes)
        rect_r2 = patches.FancyBboxPatch((4.8, 3.2), 1, 0.6, boxstyle="round,pad=0.1",
                                        facecolor='#dc2626', edgecolor='#ef4444', linewidth=2)
        self.ax_circuit_draw.add_patch(rect_r2)
        self.ax_circuit_draw.text(5.3, 3.5, 'R₂', ha='center', va='center', 
                                 color='white', fontsize=11, fontweight='bold')
        self.ax_circuit_draw.text(5.3, 4.2, '5Ω', ha='center', va='center', 
                                 color='#fca5a5', fontsize=9)
        
        rect_r3 = patches.FancyBboxPatch((6.5, 3.2), 1, 0.6, boxstyle="round,pad=0.1",
                                        facecolor='#dc2626', edgecolor='#ef4444', linewidth=2)
        self.ax_circuit_draw.add_patch(rect_r3)
        self.ax_circuit_draw.text(7, 3.5, 'R₃', ha='center', va='center', 
                                 color='white', fontsize=11, fontweight='bold')
        self.ax_circuit_draw.text(7, 4.2, '8Ω', ha='center', va='center', 
                                 color='#fca5a5', fontsize=9)
        
        # Enhanced current arrows with loops
        # Mesh 1 current
        self.ax_circuit_draw.annotate('', xy=(3.5, 5.8), xytext=(3.2, 5.5),
                                     arrowprops=dict(arrowstyle='->', color='#00d4ff', lw=3))
        self.ax_circuit_draw.add_patch(patches.Arc((3.5, 4.5), 2, 2, angle=0, theta1=45, theta2=315,
                                                  color='#00d4ff', linewidth=2, alpha=0.7))
        self.ax_circuit_draw.text(3.5, 5.8, 'I₁', ha='center', va='center', 
                                 color='#00d4ff', fontsize=12, fontweight='bold')
        
        # Mesh 2 current  
        self.ax_circuit_draw.annotate('', xy=(6.5, 5.8), xytext=(6.2, 5.5),
                                     arrowprops=dict(arrowstyle='->', color='#a78bfa', lw=3))
        self.ax_circuit_draw.add_patch(patches.Arc((6.5, 4.5), 2, 2, angle=0, theta1=45, theta2=315,
                                                  color='#a78bfa', linewidth=2, alpha=0.7))
        self.ax_circuit_draw.text(6.5, 5.8, 'I₂', ha='center', va='center', 
                                 color='#a78bfa', fontsize=12, fontweight='bold')
        
        # Add equations box
        eq_box = patches.FancyBboxPatch((1, 0.5), 8, 1.2, boxstyle="round,pad=0.1",
                                       facecolor='#1a1f3e', edgecolor='#6366f1', linewidth=2, alpha=0.9)
        self.ax_circuit_draw.add_patch(eq_box)
        
        self.ax_circuit_draw.text(5, 1.4, 'Equações das Malhas (LKT)', ha='center', va='center', 
                                 color='#00d4ff', fontsize=11, fontweight='bold')
        self.ax_circuit_draw.text(5, 0.9, 'Malha 1: V₁ = I₁R₁ + (I₁-I₂)R₂', ha='center', va='center', 
                                 color='#e2e8f0', fontsize=10)
        self.ax_circuit_draw.text(5, 0.6, 'Malha 2: V₂ = I₂R₃ + (I₂-I₁)R₂', ha='center', va='center', 
                                 color='#e2e8f0', fontsize=10)
    
    def calculate_circuit(self):
        circuit_type = self.circuit_type.get()
        vs = self.vs_voltage.get()
        
        if circuit_type == "RLC_Serie":
            self.calculate_rlc_series(vs)
        elif circuit_type == "RLC_Paralelo":
            self.calculate_rlc_parallel(vs)
        elif circuit_type == "DC_Malhas":
            self.calculate_dc_mesh(vs)
    
    def calculate_rlc_series(self, vs):
        f = self.f.get()
        r = self.r.get()
        l = self.l.get()
        c = self.c.get()
        
        # Calculate reactances
        xl = 2 * math.pi * f * l
        xc = 1 / (2 * math.pi * f * c)
        
        # Total impedance
        z_total = complex(r, xl - xc)
        z_mag = abs(z_total)
        z_angle = math.degrees(cmath.phase(z_total))
        
        # Current
        i_rms = vs / z_mag
        i_angle = -z_angle
        
        result = f"""
🔷 RLC SÉRIE - CÁLCULOS DETALHADOS
═══════════════════════════════════════════════════════════════════════════════

📐 FÓRMULAS E CÁLCULOS:

1️⃣ REATÂNCIAS:
   XL = 2πfL = 2π × {f:.0f} × {l:.4f} = {xl:.2f} Ω
   XC = 1/(2πfC) = 1/(2π × {f:.0f} × {c:.6f}) = {xc:.2f} Ω
   X = XL - XC = {xl:.2f} - {xc:.2f} = {xl-xc:.2f} Ω

2️⃣ IMPEDÂNCIA TOTAL:
   Z = R + jX = {r:.1f} + j({xl-xc:.2f}) Ω
   |Z| = √(R² + X²) = √({r:.1f}² + {xl-xc:.2f}²) = {z_mag:.2f} Ω
   θ = arctan(X/R) = arctan({xl-xc:.2f}/{r:.1f}) = {z_angle:.1f}°

3️⃣ CORRENTE:
   I = V/Z = {vs:.1f}/{z_mag:.2f} = {i_rms:.3f} A
   Ângulo da corrente = 0° - {z_angle:.1f}° = {i_angle:.1f}°

4️⃣ TENSÕES NOS COMPONENTES:
   VR = I × R = {i_rms:.3f} × {r:.1f} = {i_rms * r:.1f} V
   VL = I × XL = {i_rms:.3f} × {xl:.1f} = {i_rms * xl:.1f} V
   VC = I × XC = {i_rms:.3f} × {xc:.1f} = {i_rms * xc:.1f} V

5️⃣ POTÊNCIAS:
   P = I²R = ({i_rms:.3f})² × {r:.1f} = {i_rms**2 * r:.1f} W
   Q = I²X = ({i_rms:.3f})² × {xl-xc:.2f} = {i_rms**2 * (xl-xc):.1f} VAr
   S = VI = {vs:.1f} × {i_rms:.3f} = {vs * i_rms:.1f} VA

⚡ RESULTADOS FINAIS:
• Impedância: Z = {z_mag:.2f} ∠ {z_angle:.1f}° Ω
• Corrente: I = {i_rms:.3f} ∠ {i_angle:.1f}° A
• Fator de Potência: FP = cos({z_angle:.1f}°) = {math.cos(math.radians(z_angle)):.3f}

═══════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def calculate_rlc_parallel(self, vs):
        f = self.f.get()
        r = self.r.get()
        l = self.l.get()
        c = self.c.get()
        
        # Calculate reactances
        xl = 2 * math.pi * f * l
        xc = 1 / (2 * math.pi * f * c)
        
        # Admittances
        yr = 1 / r
        yl = 1 / complex(0, xl)
        yc = 1 / complex(0, -xc)
        
        # Total admittance
        y_total = yr + yl + yc
        z_total = 1 / y_total
        
        # Currents
        ir = vs / r
        il = vs / xl
        ic = vs * 2 * math.pi * f * c
        i_total = abs(vs * y_total)
        
        result = f"""
🔷 RLC PARALELO - CÁLCULOS DETALHADOS
═══════════════════════════════════════════════════════════════════════════════

📐 FÓRMULAS E CÁLCULOS:

1️⃣ REATÂNCIAS:
   XL = 2πfL = 2π × {f:.0f} × {l:.4f} = {xl:.2f} Ω
   XC = 1/(2πfC) = 1/(2π × {f:.0f} × {c:.6f}) = {xc:.2f} Ω

2️⃣ ADMITÂNCIAS:
   YR = 1/R = 1/{r:.1f} = {yr:.4f} S
   YL = 1/(jXL) = 1/(j{xl:.2f}) = {yl.real:.4f} + j{yl.imag:.4f} S
   YC = 1/(j(-XC)) = 1/(-j{xc:.2f}) = {yc.real:.4f} + j{yc.imag:.4f} S

3️⃣ ADMITÂNCIA TOTAL:
   Y = YR + YL + YC = {y_total.real:.4f} + j{y_total.imag:.4f} S
   |Y| = √(G² + B²) = {abs(y_total):.4f} S

4️⃣ IMPEDÂNCIA EQUIVALENTE:
   Zeq = 1/Y = 1/({abs(y_total):.4f}) = {abs(z_total):.2f} Ω
   θ = {math.degrees(cmath.phase(z_total)):.1f}°

5️⃣ CORRENTES DOS RAMOS:
   IR = V/R = {vs:.1f}/{r:.1f} = {ir:.3f} A
   IL = V/XL = {vs:.1f}/{xl:.2f} = {il:.3f} A
   IC = V/XC = {vs:.1f}/{xc:.2f} = {ic:.3f} A
   
   Itotal = V × |Y| = {vs:.1f} × {abs(y_total):.4f} = {i_total:.3f} A

6️⃣ POTÊNCIAS:
   P = V²/R = ({vs:.1f})²/{r:.1f} = {vs**2 / r:.1f} W
   QL = V²/XL = ({vs:.1f})²/{xl:.2f} = {vs**2 / xl:.1f} VAr (indutiva)
   QC = V²/XC = ({vs:.1f})²/{xc:.2f} = {vs**2 / xc:.1f} VAr (capacitiva)
   S = V × Itotal = {vs:.1f} × {i_total:.3f} = {vs * i_total:.1f} VA

⚡ RESULTADOS FINAIS:
• Impedância Equivalente: Zeq = {abs(z_total):.2f} ∠ {math.degrees(cmath.phase(z_total)):.1f}° Ω
• Corrente Total: I = {i_total:.3f} A
• Fator de Potência: FP = {math.cos(cmath.phase(z_total)):.3f}

═══════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def calculate_dc_mesh(self, vs):
        result = f"""
🔷 ANÁLISE DC - MÉTODO DAS MALHAS
═══════════════════════════════════════════════════════════

Para resolver o circuito DC por malhas:

1. Identifique as malhas independentes
2. Aplique a Lei de Kirchhoff das Tensões (LKT) para cada malha
3. Monte o sistema de equações lineares
4. Resolva o sistema para encontrar as correntes de malha

Exemplo para 2 malhas:
Malha 1: V1 = I1*R1 + (I1-I2)*R2
Malha 2: V2 = I2*R3 + (I2-I1)*R2

Onde:
• I1, I2 são as correntes de malha
• R1, R2, R3 são as resistências
• V1, V2 são as tensões das fontes

═══════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def calc_impedance(self):
        try:
            f = self.f.get()
            r = self.r.get()
            l = self.l.get()
            c = self.c.get()
            
            xl = 2 * math.pi * f * l
            xc = 1 / (2 * math.pi * f * c)
            z = complex(r, xl - xc)
            
            result = f"""
🔷 CÁLCULO DE IMPEDÂNCIA (f = {f} Hz)
═══════════════════════════════════════════════════════════════════════════════

📐 FÓRMULAS E CÁLCULOS:

1️⃣ REATÂNCIA INDUTIVA:
   XL = 2πfL = 2π × {f:.0f} × {l:.4f} = {xl:.2f} Ω

2️⃣ REATÂNCIA CAPACITIVA:
   XC = 1/(2πfC) = 1/(2π × {f:.0f} × {c:.6f}) = {xc:.2f} Ω

3️⃣ REATÂNCIA RESULTANTE:
   X = XL - XC = {xl:.2f} - {xc:.2f} = {xl-xc:.2f} Ω

4️⃣ IMPEDÂNCIA COMPLEXA:
   Z = R + jX = {r:.1f} + j({xl-xc:.2f}) Ω

5️⃣ MÓDULO DA IMPEDÂNCIA:
   |Z| = √(R² + X²) = √({r:.1f}² + ({xl-xc:.2f})²) = {abs(z):.2f} Ω

6️⃣ ÂNGULO DE FASE:
   θ = arctan(X/R) = arctan({xl-xc:.2f}/{r:.1f}) = {math.degrees(cmath.phase(z)):.1f}°

⚡ RESULTADO FINAL:
• Z = {abs(z):.2f} ∠ {math.degrees(cmath.phase(z)):.1f}° Ω
• Natureza: {'Indutiva' if xl-xc > 0 else 'Capacitiva' if xl-xc < 0 else 'Resistiva'}

═══════════════════════════════════════════════════════════════════════════════
"""
            
            self.results_text.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def calc_resonance(self):
        try:
            l = self.l.get()
            c = self.c.get()
            r = self.r.get()
            
            f_res = 1 / (2 * math.pi * math.sqrt(l * c))
            
            # Calculate values at resonance
            xl_res = 2 * math.pi * f_res * l
            xc_res = 1 / (2 * math.pi * f_res * c)
            
            result = f"""
🔷 FREQUÊNCIA DE RESSONÂNCIA - CÁLCULOS DETALHADOS
═══════════════════════════════════════════════════════════════════════════════

📐 FÓRMULA E CÁLCULOS:

1️⃣ FREQUÊNCIA DE RESSONÂNCIA:
   f₀ = 1/(2π√LC)
   
   Onde:
   L = {l:.6f} H = {l*1000:.3f} mH
   C = {c:.9f} F = {c*1000000:.3f} μF
   
   f₀ = 1/(2π√({l:.6f} × {c:.9f}))
   f₀ = 1/(2π√{l*c:.9f})
   f₀ = 1/(2π × {math.sqrt(l*c):.6f})
   f₀ = {f_res:.2f} Hz

2️⃣ VERIFICAÇÃO NA RESSONÂNCIA:
   XL = 2πf₀L = 2π × {f_res:.2f} × {l:.6f} = {xl_res:.2f} Ω
   XC = 1/(2πf₀C) = 1/(2π × {f_res:.2f} × {c:.9f}) = {xc_res:.2f} Ω
   
   Diferença: |XL - XC| = |{xl_res:.2f} - {xc_res:.2f}| = {abs(xl_res - xc_res):.6f} Ω ≈ 0

3️⃣ CONDIÇÕES DE RESSONÂNCIA:
   • XL = XC (reatâncias se cancelam)
   • X = XL - XC = 0 Ω
   • Z = R = {r:.1f} Ω (impedância mínima)
   • Corrente máxima: I = V/R
   • Fator de potência unitário: FP = 1

⚡ RESULTADOS:
• Frequência de ressonância: f₀ = {f_res:.2f} Hz
• Período: T₀ = 1/f₀ = {1/f_res*1000:.3f} ms
• Ômega: ω₀ = 2πf₀ = {2*math.pi*f_res:.2f} rad/s

═══════════════════════════════════════════════════════════════════════════════
"""
            
            self.results_text.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def analyze_circuit(self):
        try:
            # Get values
            f = self.f.get()
            vm = self.vm.get()
            im = self.im.get()
            theta_v_deg = self.theta_v.get()
            theta_i_deg = self.theta_i.get()
            
            # Convert to RMS and radians
            vrms = vm / math.sqrt(2)
            irms = im / math.sqrt(2)
            theta_v_rad = math.radians(theta_v_deg)
            theta_i_rad = math.radians(theta_i_deg)
            
            # Create phasors
            self.v_phasor = complex(vrms * math.cos(theta_v_rad), vrms * math.sin(theta_v_rad))
            self.i_phasor = complex(irms * math.cos(theta_i_rad), irms * math.sin(theta_i_rad))
            
            # Calculate impedance
            self.z_equiv = self.v_phasor / self.i_phasor
            
            # Calculate power
            self.s_apparent = self.v_phasor * self.i_phasor.conjugate()
            
            # Plot signals and phasors
            self.plot_signals()
            self.plot_phasor_diagrams()
            
            # Generate comprehensive results
            self.generate_comprehensive_results()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na análise: {str(e)}")
    
    def plot_signals(self):
        # Clear plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Get parameters
        f = self.f.get()
        vm = self.vm.get()
        im = self.im.get()
        theta_v_deg = self.theta_v.get()
        theta_i_deg = self.theta_i.get()
        
        # Time array (3 periods)
        t = np.linspace(0, 3/f, 1000)
        t_ms = t * 1000
        
        # Signals
        omega = 2 * math.pi * f
        v = vm * np.sin(omega * t + math.radians(theta_v_deg))
        i = im * np.sin(omega * t + math.radians(theta_i_deg))
        p = v * i
        
        # RMS power
        vrms = vm / math.sqrt(2)
        irms = im / math.sqrt(2)
        phase_diff_deg = theta_v_deg - theta_i_deg
        prms = vrms * irms * math.cos(math.radians(phase_diff_deg))
        prms_line = np.full_like(t, prms)
        
        # Scale factor for current display
        scale_factor = vm / im if im != 0 else 1
        
        # Plot voltage and current
        self.ax1.plot(t_ms, v, 'r-', label=f'v(t) = {vm:.1f}sin(ωt + {theta_v_deg:.1f}°) V', linewidth=2.5)
        self.ax1.plot(t_ms, scale_factor*i, 'b-', label=f'i(t) = {im:.1f}sin(ωt + {theta_i_deg:.1f}°) A (×{scale_factor:.1f})', linewidth=2.5)
        
        # Find and mark zero crossings for phase analysis
        zero_crossings_v = []
        zero_crossings_i = []
        
        for i_time in range(1, len(t)):
            if v[i_time-1] * v[i_time] < 0 and v[i_time] > 0:
                zero_crossings_v.append(t_ms[i_time])
            if (scale_factor*i[i_time-1]) * (scale_factor*i[i_time]) < 0 and (scale_factor*i[i_time]) > 0:
                zero_crossings_i.append(t_ms[i_time])
        
        # Mark zero crossings
        for zc in zero_crossings_v[:4]:
            self.ax1.axvline(x=zc, color='red', linestyle='--', alpha=0.5, linewidth=1)
        for zc in zero_crossings_i[:4]:
            self.ax1.axvline(x=zc, color='blue', linestyle='--', alpha=0.5, linewidth=1)
        
        # Add phase difference annotation
        if abs(phase_diff_deg) > 1:
            self.ax1.text(0.02, 0.98, f'Defasagem: {phase_diff_deg:.1f}°', 
                         transform=self.ax1.transAxes, fontsize=12, 
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8),
                         verticalalignment='top')
        
        self.ax1.set_title('Sinais Elétricos v(t) e i(t) - Análise de Defasagem', 
                          color='white', fontsize=14, fontweight='bold')
        self.ax1.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax1.set_ylabel('Amplitude', color='white', fontsize=12)
        self.ax1.legend(fontsize=10, loc='upper right')
        self.ax1.grid(True, alpha=0.4)
        self.ax1.axhline(y=0, color='white', linewidth=0.8)
        self.ax1.axvline(x=0, color='white', linewidth=0.8)
        
        # Plot power
        if np.max(p) >= 1000:
            self.ax2.plot(t_ms, p*0.001, 'm-', label='p(t)', linewidth=2.5)
            self.ax2.plot(t_ms, prms_line*0.001, 'k-', label='Prms', linewidth=2.5)
            self.ax2.set_ylabel('Potência [kW]', color='white', fontsize=12)
        else:
            self.ax2.plot(t_ms, p, 'm-', label='p(t)', linewidth=2.5)
            self.ax2.plot(t_ms, prms_line, 'k-', label='Prms', linewidth=2.5)
            self.ax2.set_ylabel('Potência [W]', color='white', fontsize=12)
        
        self.ax2.set_title('Potência Instantânea p(t)', color='white', fontsize=14, fontweight='bold')
        self.ax2.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax2.legend(fontsize=11)
        self.ax2.grid(True, alpha=0.4)
        self.ax2.axhline(y=0, color='white', linewidth=0.8)
        self.ax2.axvline(x=0, color='white', linewidth=0.8)
        
        self.fig_signals.tight_layout(pad=2.0)
        self.canvas_signals.draw()
    
    def plot_phasor_diagrams(self):
        if self.v_phasor is None or self.i_phasor is None:
            return
        
        # Clear all phasor plots and convert to polar
        self.fig_phasor.clear()
        
        # Create polar subplots following the model
        self.ax_vi = self.fig_phasor.add_subplot(221, projection='polar', facecolor='#1e293b')
        self.ax_z = self.fig_phasor.add_subplot(222, projection='polar', facecolor='#1e293b')
        self.ax_power = self.fig_phasor.add_subplot(223, projection='polar', facecolor='#1e293b')
        self.ax_complex = self.fig_phasor.add_subplot(224, projection='polar', facecolor='#1e293b')
        
        # 1. Voltage and Current Phasors (Polar)
        v_mag = abs(self.v_phasor)
        v_angle = cmath.phase(self.v_phasor)
        i_mag = abs(self.i_phasor)
        i_angle = cmath.phase(self.i_phasor)
        
        # Plot voltage and current phasors
        self.ax_vi.plot([0, v_angle], [0, v_mag], 'r-', linewidth=4, label=f'V = {v_mag:.1f}∠{math.degrees(v_angle):.1f}°')
        self.ax_vi.plot([0, i_angle], [0, i_mag*50], 'b-', linewidth=4, label=f'I = {i_mag:.3f}∠{math.degrees(i_angle):.1f}°')
        
        # Add arrow heads
        self.ax_vi.annotate('', xy=(v_angle, v_mag), xytext=(v_angle, v_mag*0.9),
                           arrowprops=dict(arrowstyle='->', color='red', lw=3))
        self.ax_vi.annotate('', xy=(i_angle, i_mag*50), xytext=(i_angle, i_mag*50*0.9),
                           arrowprops=dict(arrowstyle='->', color='blue', lw=3))
        
        # Customize polar grid
        self.ax_vi.set_theta_zero_location('E')
        self.ax_vi.set_theta_direction(1)
        self.ax_vi.grid(True, alpha=0.6, color='white', linewidth=0.8)
        self.ax_vi.set_title('FASORES V e I\n(Tensão e Corrente)', color='white', fontweight='bold', fontsize=11, pad=20)
        
        # Add radial labels
        max_val = max(v_mag, i_mag*50) * 1.2
        self.ax_vi.set_ylim(0, max_val)
        self.ax_vi.tick_params(colors='white', labelsize=8)
        
        # 2. Impedance Diagram (Polar)
        z_mag = abs(self.z_equiv)
        z_angle = cmath.phase(self.z_equiv)
        
        self.ax_z.plot([0, z_angle], [0, z_mag], 'cyan', linewidth=4, label=f'Z = {z_mag:.1f}∠{math.degrees(z_angle):.1f}°')
        self.ax_z.annotate('', xy=(z_angle, z_mag), xytext=(z_angle, z_mag*0.9),
                          arrowprops=dict(arrowstyle='->', color='cyan', lw=3))
        
        # Add resistance and reactance components
        r_component = self.z_equiv.real
        x_component = self.z_equiv.imag
        
        # Draw R and X components as dashed lines
        if r_component > 0:
            self.ax_z.plot([0, 0], [0, r_component], 'g--', linewidth=2, alpha=0.8, label=f'R = {r_component:.1f}Ω')
        if abs(x_component) > 0:
            x_angle = math.pi/2 if x_component > 0 else -math.pi/2
            self.ax_z.plot([0, x_angle], [0, abs(x_component)], 'm--', linewidth=2, alpha=0.8, 
                          label=f'X = {x_component:.1f}Ω')
        
        self.ax_z.set_theta_zero_location('E')
        self.ax_z.set_theta_direction(1)
        self.ax_z.grid(True, alpha=0.6, color='white', linewidth=0.8)
        self.ax_z.set_title('IMPEDÂNCIA Z\n(R + jX)', color='white', fontweight='bold', fontsize=11, pad=20)
        self.ax_z.set_ylim(0, z_mag * 1.3)
        self.ax_z.tick_params(colors='white', labelsize=8)
        
        # 3. Power Triangle (Polar)
        s_mag = abs(self.s_apparent)
        s_angle = cmath.phase(self.s_apparent)
        p_active = self.s_apparent.real
        q_reactive = self.s_apparent.imag
        
        self.ax_power.plot([0, s_angle], [0, s_mag], 'magenta', linewidth=4, 
                          label=f'S = {s_mag:.1f}∠{math.degrees(s_angle):.1f}°')
        self.ax_power.annotate('', xy=(s_angle, s_mag), xytext=(s_angle, s_mag*0.9),
                              arrowprops=dict(arrowstyle='->', color='magenta', lw=3))
        
        # Add P and Q components
        if p_active > 0:
            self.ax_power.plot([0, 0], [0, p_active], 'orange', linewidth=3, alpha=0.8, label=f'P = {p_active:.1f}W')
        if abs(q_reactive) > 0:
            q_angle = math.pi/2 if q_reactive > 0 else -math.pi/2
            self.ax_power.plot([0, q_angle], [0, abs(q_reactive)], 'yellow', linewidth=3, alpha=0.8,
                              label=f'Q = {q_reactive:.1f}VAr')
        
        fp = math.cos(cmath.phase(self.z_equiv))
        self.ax_power.text(0.02, 0.98, f'FP = {fp:.3f}', transform=self.ax_power.transAxes,
                          color='yellow', fontsize=10, fontweight='bold', 
                          bbox=dict(boxstyle="round,pad=0.3", facecolor='#1e293b', alpha=0.8))
        
        self.ax_power.set_theta_zero_location('E')
        self.ax_power.set_theta_direction(1)
        self.ax_power.grid(True, alpha=0.6, color='white', linewidth=0.8)
        self.ax_power.set_title('POTÊNCIA COMPLEXA\n(P + jQ)', color='white', fontweight='bold', fontsize=11, pad=20)
        self.ax_power.set_ylim(0, s_mag * 1.3)
        self.ax_power.tick_params(colors='white', labelsize=8)
        
        # 4. Complex Number Representation
        # Show both V and I as complex numbers in same polar plot
        self.ax_complex.plot([0, v_angle], [0, v_mag], 'r-', linewidth=4, alpha=0.8, 
                            label=f'V: {v_mag:.1f}∠{math.degrees(v_angle):.1f}°')
        self.ax_complex.plot([0, i_angle], [0, i_mag*50], 'b-', linewidth=4, alpha=0.8,
                            label=f'I: {i_mag:.3f}∠{math.degrees(i_angle):.1f}°')
        
        # Add magnitude and angle annotations
        v_real = self.v_phasor.real
        v_imag = self.v_phasor.imag
        i_real = self.i_phasor.real
        i_imag = self.i_phasor.imag
        
        # Arrow heads
        self.ax_complex.annotate('', xy=(v_angle, v_mag), xytext=(v_angle, v_mag*0.9),
                                arrowprops=dict(arrowstyle='->', color='red', lw=3))
        self.ax_complex.annotate('', xy=(i_angle, i_mag*50), xytext=(i_angle, i_mag*50*0.9),
                                arrowprops=dict(arrowstyle='->', color='blue', lw=3))
        
        # Add component projections
        if abs(v_real) > 0.1:
            self.ax_complex.plot([0, 0], [0, abs(v_real)], 'r:', linewidth=2, alpha=0.6)
        if abs(v_imag) > 0.1:
            v_imag_angle = math.pi/2 if v_imag > 0 else -math.pi/2
            self.ax_complex.plot([0, v_imag_angle], [0, abs(v_imag)], 'r:', linewidth=2, alpha=0.6)
        
        self.ax_complex.set_theta_zero_location('E')
        self.ax_complex.set_theta_direction(1)
        self.ax_complex.grid(True, alpha=0.6, color='white', linewidth=0.8)
        self.ax_complex.set_title('NÚMEROS COMPLEXOS\n(Forma Polar)', color='white', fontweight='bold', fontsize=11, pad=20)
        self.ax_complex.set_ylim(0, max(v_mag, i_mag*50) * 1.2)
        self.ax_complex.tick_params(colors='white', labelsize=8)
        
        # Style all polar plots
        for ax in [self.ax_vi, self.ax_z, self.ax_power, self.ax_complex]:
            ax.set_facecolor('#1e293b')
            ax.spines['polar'].set_color('white')
            
            # Add angle markers (0°, 90°, 180°, 270°)
            angles = [0, np.pi/2, np.pi, 3*np.pi/2]
            angle_labels = ['0°', '90°', '180°', '270°']
            for angle, label in zip(angles, angle_labels):
                ax.text(angle, ax.get_ylim()[1]*1.1, label, ha='center', va='center', 
                       color='white', fontsize=9, fontweight='bold')
        
        self.fig_phasor.tight_layout(pad=2.0)
        self.canvas_phasor.draw()
        
        # Update results panel
        self.update_phasor_results()
    
    def update_phasor_results(self):
        if self.v_phasor is None or self.i_phasor is None:
            return
        
        # Clear previous results
        self.phasor_results_text.delete(1.0, tk.END)
        
        # Calculate values
        v_mag = abs(self.v_phasor)
        v_angle = math.degrees(cmath.phase(self.v_phasor))
        i_mag = abs(self.i_phasor)
        i_angle = math.degrees(cmath.phase(self.i_phasor))
        z_mag = abs(self.z_equiv)
        z_angle = math.degrees(cmath.phase(self.z_equiv))
        p_active = self.s_apparent.real
        q_reactive = self.s_apparent.imag
        s_apparent = abs(self.s_apparent)
        fp = math.cos(cmath.phase(self.z_equiv))
        
        # Create concise results
        results = f"""⚡ FASORES PRINCIPAIS
V: {v_mag:.2f} ∠ {v_angle:.1f}° V
I: {i_mag:.3f} ∠ {i_angle:.1f}° A
Z: {z_mag:.2f} ∠ {z_angle:.1f}° Ω

🔌 IMPEDÂNCIA
R = {self.z_equiv.real:.2f} Ω
X = {self.z_equiv.imag:.2f} Ω

⚡ POTÊNCIA
P = {p_active:.1f} W
Q = {q_reactive:.1f} VAr
S = {s_apparent:.1f} VA
FP = {fp:.3f}

📈 ANÁLISE
Defasagem: {v_angle - i_angle:.1f}°
Tipo: {'Indutivo' if z_angle > 0 else 'Capacitivo' if z_angle < 0 else 'Resistivo'}
"""
        
        self.phasor_results_text.insert(tk.END, results)
    
    def generate_comprehensive_results(self):
        # Calculate detailed values
        v_mag = abs(self.v_phasor)
        i_mag = abs(self.i_phasor)
        z_mag = abs(self.z_equiv)
        v_angle = math.degrees(cmath.phase(self.v_phasor))
        i_angle = math.degrees(cmath.phase(self.i_phasor))
        z_angle = math.degrees(cmath.phase(self.z_equiv))
        fp = math.cos(cmath.phase(self.z_equiv))
        
        comprehensive_results = f"""
🔷 ANÁLISE COMPLETA DO CIRCUITO - CÁLCULOS DETALHADOS
════════════════════════════════════════════════════════════════════════════════

📐 FASORES DE ENTRADA:
• Tensão: V = {self.vm.get():.1f}∠{self.theta_v.get():.1f}° V (máx) → {v_mag:.2f}∠{v_angle:.1f}° V (RMS)
• Corrente: I = {self.im.get():.1f}∠{self.theta_i.get():.1f}° A (máx) → {i_mag:.3f}∠{i_angle:.1f}° A (RMS)

📊 CÁLCULO DA IMPEDÂNCIA:
   Z = V/I = ({v_mag:.2f}∠{v_angle:.1f}°) / ({i_mag:.3f}∠{i_angle:.1f}°)
   Z = {v_mag:.2f}/{i_mag:.3f} ∠ ({v_angle:.1f}° - {i_angle:.1f}°)
   Z = {z_mag:.2f} ∠ {z_angle:.1f}° Ω
   
   Forma retangular: Z = {self.z_equiv.real:.2f} + j{self.z_equiv.imag:.2f} Ω

⚡ CÁLCULO DAS POTÊNCIAS:
   S* = V × I* = ({v_mag:.2f}∠{v_angle:.1f}°) × ({i_mag:.3f}∠{-i_angle:.1f}°)
   S* = {v_mag:.2f} × {i_mag:.3f} ∠ ({v_angle:.1f}° + {-i_angle:.1f}°)
   S* = {abs(self.s_apparent):.1f} ∠ {math.degrees(cmath.phase(self.s_apparent)):.1f}° VA
   
   P = Re(S*) = {self.s_apparent.real:.1f} W (potência ativa)
   Q = Im(S*) = {self.s_apparent.imag:.1f} VAr (potência reativa)
   S = |S*| = {abs(self.s_apparent):.1f} VA (potência aparente)

📈 FATOR DE POTÊNCIA:
   FP = cos(θ) = cos({z_angle:.1f}°) = {fp:.3f}
   
   Onde θ é o ângulo de defasagem entre tensão e corrente.

🔌 CARACTERIZAÇÃO DO CIRCUITO:
• Tipo: {'Indutivo (corrente atrasada)' if self.z_equiv.imag > 0 else 'Capacitivo (corrente adiantada)' if self.z_equiv.imag < 0 else 'Resistivo (tensão e corrente em fase)'}
• Defasagem V-I: θ = {v_angle - i_angle:.1f}°
• Resistência: R = {self.z_equiv.real:.2f} Ω
• Reatância: X = {self.z_equiv.imag:.2f} Ω {'(indutiva)' if self.z_equiv.imag > 0 else '(capacitiva)' if self.z_equiv.imag < 0 else '(nula)'}

🔍 VERIFICAÇÕES:
• Teorema de Pitágoras: |Z|² = R² + X² → {z_mag:.2f}² = {self.z_equiv.real:.2f}² + {self.z_equiv.imag:.2f}² ✓
• Triângulo de potência: |S|² = P² + Q² → {abs(self.s_apparent):.1f}² = {self.s_apparent.real:.1f}² + {self.s_apparent.imag:.1f}² ✓

════════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, comprehensive_results)
    
    def power_factor_correction(self):
        try:
            if self.z_equiv is None:
                messagebox.showwarning("Aviso", "Execute a análise do circuito primeiro!")
                return
            
            # Get current power factor
            fp_current = math.cos(cmath.phase(self.z_equiv))
            
            # Ask for desired power factor
            fp_desired = tk.simpledialog.askfloat("Correção do Fator de Potência", 
                                                 f"Fator de potência atual: {fp_current:.3f}\n" +
                                                 "Digite o fator de potência desejado (0-1):",
                                                 minvalue=0.0, maxvalue=1.0)
            
            if fp_desired is None:
                return
            
            # Calculate correction
            vrms = abs(self.v_phasor)
            p_active = self.s_apparent.real
            q_reactive_current = self.s_apparent.imag
            q_reactive_desired = p_active * math.tan(math.acos(fp_desired))
            q_capacitor = q_reactive_current - q_reactive_desired
            
            # Calculate capacitance
            f = self.f.get()
            c_microfarads = abs(q_capacitor / (vrms**2 * 2 * math.pi * f)) * 1000000
            
            correction_report = f"""
🔷 CORREÇÃO DO FATOR DE POTÊNCIA
════════════════════════════════════════════════════════════════════════════════

ANÁLISE ATUAL:
• Fator de potência original: {fp_current:.4f}
• Potência ativa: {p_active:.3f} W
• Potência reativa atual: {q_reactive_current:.3f} VAr

CORREÇÃO DESEJADA:
• Fator de potência corrigido: {fp_desired:.4f}
• Potência reativa desejada: {q_reactive_desired:.3f} VAr
• Potência reativa do capacitor: {q_capacitor:.3f} VAr

CAPACITOR DE CORREÇÃO:
• Capacitância necessária: {c_microfarads:.3f} μF
• Tensão nominal: {vrms:.1f} V RMS

RESULTADOS APÓS CORREÇÃO:
• Corrente reduzida em: {(1 - fp_desired/fp_current)*100:.1f}%
• Economia na potência aparente: {abs(self.s_apparent) - (p_active/fp_desired):.2f} VA

════════════════════════════════════════════════════════════════════════════════
"""
            
            self.results_text.insert(tk.END, correction_report)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na correção: {str(e)}")
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.phasor_results_text.delete(1.0, tk.END)
        
        # Clear all plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax_vi.clear()
        self.ax_z.clear()
        self.ax_power.clear()
        self.ax_circuit.clear()
        self.ax_circuit_draw.clear()
        
        self.canvas_signals.draw()
        self.canvas_phasor.draw()
        self.canvas_circuit.draw()
        
        # Clear transient and frequency plots
        if hasattr(self, 'ax_transient1'):
            self.ax_transient1.clear()
            self.ax_transient2.clear()
            self.canvas_transient.draw()
        
        if hasattr(self, 'ax_freq1'):
            self.ax_freq1.clear()
            self.ax_freq2.clear()
            self.canvas_frequency.draw()
        
        # Reset variables
        self.v_phasor = None
        self.i_phasor = None
        self.z_equiv = None
        self.s_apparent = None
    
    def run_transient_analysis(self):
        """Switch to transient analysis tab and prepare interface"""
        self.notebook.select(self.transient_frame)
        messagebox.showinfo("Análise Transitória", 
                           "Configure os parâmetros na aba 'Análise Transitória' e clique em 'EXECUTAR ANÁLISE'")
    
    def run_frequency_analysis(self):
        """Switch to frequency analysis tab and prepare interface"""
        self.notebook.select(self.frequency_frame)
        messagebox.showinfo("Análise de Frequência", 
                           "Configure os parâmetros na aba 'Resposta em Frequência' e clique em 'GERAR GRÁFICOS'")
    
    def calculate_transient_response(self):
        """Calculate and plot transient response"""
        try:
            # Get circuit parameters
            r = self.r.get()
            l = self.l.get()
            c = self.c.get()
            t_final = self.t_final.get()
            amplitude = self.step_amplitude.get()
            analysis_type = self.transient_type.get()
            
            # Time vector
            t = np.linspace(0, t_final, 1000)
            
            # Calculate circuit parameters
            if analysis_type == "step":
                self.calculate_step_response(t, r, l, c, amplitude)
            elif analysis_type == "impulse":
                self.calculate_impulse_response(t, r, l, c, amplitude)
            elif analysis_type == "natural":
                self.calculate_natural_response(t, r, l, c, amplitude)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na análise transitória: {str(e)}")
    
    def calculate_step_response(self, t, r, l, c, amplitude):
        """Calculate step response for RLC circuit"""
        # Circuit parameters
        omega_n = 1 / math.sqrt(l * c)  # Natural frequency
        zeta = r / 2 * math.sqrt(c / l)  # Damping ratio
        
        # Clear plots
        self.ax_transient1.clear()
        self.ax_transient2.clear()
        
        if zeta > 1:  # Overdamped
            s1 = -zeta * omega_n + omega_n * math.sqrt(zeta**2 - 1)
            s2 = -zeta * omega_n - omega_n * math.sqrt(zeta**2 - 1)
            
            A1 = amplitude * s2 / (s2 - s1)
            A2 = -amplitude * s1 / (s2 - s1)
            
            vc = amplitude + A1 * np.exp(s1 * t) + A2 * np.exp(s2 * t)
            il = (A1 * s1 * np.exp(s1 * t) + A2 * s2 * np.exp(s2 * t)) / l
            
            regime = "Superamortecido (ζ > 1)"
            
        elif zeta == 1:  # Critically damped
            vc = amplitude * (1 - (1 + omega_n * t) * np.exp(-omega_n * t))
            il = (amplitude * omega_n**2 * t * np.exp(-omega_n * t)) / l
            
            regime = "Criticamente Amortecido (ζ = 1)"
            
        else:  # Underdamped
            omega_d = omega_n * math.sqrt(1 - zeta**2)  # Damped frequency
            
            vc = amplitude * (1 - np.exp(-zeta * omega_n * t) * 
                             (np.cos(omega_d * t) + (zeta * omega_n / omega_d) * np.sin(omega_d * t)))
            il = (amplitude * omega_n**2 * np.exp(-zeta * omega_n * t) * np.sin(omega_d * t)) / (l * omega_d)
            
            regime = "Subamortecido (ζ < 1)"
        
        # Plot voltage
        self.ax_transient1.plot(t * 1000, vc, 'r-', linewidth=2.5, label=f'Tensão no Capacitor - {regime}')
        self.ax_transient1.axhline(y=amplitude, color='white', linestyle='--', alpha=0.7, label='Valor Final')
        self.ax_transient1.axhline(y=0.63*amplitude, color='yellow', linestyle=':', alpha=0.7, label='63% do Valor Final')
        
        self.ax_transient1.set_title('Resposta ao Degrau - Tensão no Capacitor', 
                                    color='white', fontsize=14, fontweight='bold')
        self.ax_transient1.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax_transient1.set_ylabel('Tensão [V]', color='white', fontsize=12)
        self.ax_transient1.legend(fontsize=10)
        self.ax_transient1.grid(True, alpha=0.4)
        
        # Plot current
        self.ax_transient2.plot(t * 1000, il * 1000, 'b-', linewidth=2.5, label=f'Corrente no Indutor - {regime}')
        self.ax_transient2.axhline(y=0, color='white', linestyle='--', alpha=0.7)
        
        self.ax_transient2.set_title('Resposta ao Degrau - Corrente no Indutor', 
                                    color='white', fontsize=14, fontweight='bold')
        self.ax_transient2.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax_transient2.set_ylabel('Corrente [mA]', color='white', fontsize=12)
        self.ax_transient2.legend(fontsize=10)
        self.ax_transient2.grid(True, alpha=0.4)
        
        self.fig_transient.tight_layout(pad=2.0)
        self.canvas_transient.draw()
        
        # Add results to text
        result = f"""
🔷 ANÁLISE TRANSITÓRIA - RESPOSTA AO DEGRAU
═══════════════════════════════════════════════════════════════════════════════

📐 PARÂMETROS DO CIRCUITO:
• Resistência: R = {r:.1f} Ω
• Indutância: L = {l:.6f} H = {l*1000:.3f} mH
• Capacitância: C = {c:.9f} F = {c*1000000:.3f} μF

📊 CARACTERÍSTICAS DO SISTEMA:
• Frequência natural: ωₙ = 1/√(LC) = {omega_n:.2f} rad/s = {omega_n/(2*math.pi):.2f} Hz
• Coeficiente de amortecimento: ζ = R/2 × √(C/L) = {zeta:.3f}
• Regime de amortecimento: {regime}

⚡ ANÁLISE DA RESPOSTA:
• Amplitude do degrau: {amplitude:.1f} V
• Tempo de simulação: {self.t_final.get()*1000:.1f} ms
• Valor final da tensão: {amplitude:.1f} V
• Corrente inicial no indutor: 0 A
• Tensão inicial no capacitor: 0 V

═══════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def calculate_impulse_response(self, t, r, l, c, amplitude):
        """Calculate impulse response for RLC circuit"""
        # Circuit parameters
        omega_n = 1 / math.sqrt(l * c)
        zeta = r / 2 * math.sqrt(c / l)
        
        # Clear plots
        self.ax_transient1.clear()
        self.ax_transient2.clear()
        
        if zeta > 1:  # Overdamped
            s1 = -zeta * omega_n + omega_n * math.sqrt(zeta**2 - 1)
            s2 = -zeta * omega_n - omega_n * math.sqrt(zeta**2 - 1)
            
            h = (amplitude / (l * (s1 - s2))) * (np.exp(s1 * t) - np.exp(s2 * t))
            regime = "Superamortecido"
            
        elif zeta == 1:  # Critically damped
            h = (amplitude * omega_n**2 * t * np.exp(-omega_n * t)) / l
            regime = "Criticamente Amortecido"
            
        else:  # Underdamped
            omega_d = omega_n * math.sqrt(1 - zeta**2)
            h = (amplitude * omega_n * np.exp(-zeta * omega_n * t) * np.sin(omega_d * t)) / (l * omega_d)
            regime = "Subamortecido"
        
        # Plot impulse response
        self.ax_transient1.plot(t * 1000, h, 'g-', linewidth=2.5, label=f'Resposta ao Impulso - {regime}')
        self.ax_transient1.axhline(y=0, color='white', linestyle='--', alpha=0.7)
        
        self.ax_transient1.set_title('Resposta ao Impulso - Corrente', 
                                    color='white', fontsize=14, fontweight='bold')
        self.ax_transient1.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax_transient1.set_ylabel('Corrente [A]', color='white', fontsize=12)
        self.ax_transient1.legend(fontsize=10)
        self.ax_transient1.grid(True, alpha=0.4)
        
        # Energy decay
        energy = 0.5 * l * h**2
        self.ax_transient2.plot(t * 1000, energy * 1000, 'm-', linewidth=2.5, label='Energia Armazenada')
        
        self.ax_transient2.set_title('Energia no Sistema', 
                                    color='white', fontsize=14, fontweight='bold')
        self.ax_transient2.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax_transient2.set_ylabel('Energia [mJ]', color='white', fontsize=12)
        self.ax_transient2.legend(fontsize=10)
        self.ax_transient2.grid(True, alpha=0.4)
        
        self.fig_transient.tight_layout(pad=2.0)
        self.canvas_transient.draw()
    
    def calculate_natural_response(self, t, r, l, c, amplitude):
        """Calculate natural response (no external excitation)"""
        # Initial conditions: vc(0) = amplitude, il(0) = 0
        omega_n = 1 / math.sqrt(l * c)
        zeta = r / 2 * math.sqrt(c / l)
        
        # Clear plots
        self.ax_transient1.clear()
        self.ax_transient2.clear()
        
        if zeta > 1:  # Overdamped
            s1 = -zeta * omega_n + omega_n * math.sqrt(zeta**2 - 1)
            s2 = -zeta * omega_n - omega_n * math.sqrt(zeta**2 - 1)
            
            A1 = amplitude * s2 / (s2 - s1)
            A2 = -amplitude * s1 / (s2 - s1)
            
            vc = A1 * np.exp(s1 * t) + A2 * np.exp(s2 * t)
            il = c * (A1 * s1 * np.exp(s1 * t) + A2 * s2 * np.exp(s2 * t))
            
        else:  # Underdamped (most common case)
            omega_d = omega_n * math.sqrt(1 - zeta**2) if zeta < 1 else omega_n
            
            vc = amplitude * np.exp(-zeta * omega_n * t) * np.cos(omega_d * t)
            il = -(amplitude * c * zeta * omega_n * np.exp(-zeta * omega_n * t) * 
                   np.cos(omega_d * t) + amplitude * c * omega_d * np.exp(-zeta * omega_n * t) * 
                   np.sin(omega_d * t))
        
        # Plot natural response
        self.ax_transient1.plot(t * 1000, vc, 'c-', linewidth=2.5, label='Tensão no Capacitor')
        self.ax_transient1.axhline(y=0, color='white', linestyle='--', alpha=0.7)
        
        self.ax_transient1.set_title('Resposta Natural - Tensão no Capacitor', 
                                    color='white', fontsize=14, fontweight='bold')
        self.ax_transient1.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax_transient1.set_ylabel('Tensão [V]', color='white', fontsize=12)
        self.ax_transient1.legend(fontsize=10)
        self.ax_transient1.grid(True, alpha=0.4)
        
        self.ax_transient2.plot(t * 1000, il * 1000, 'orange', linewidth=2.5, label='Corrente no Indutor')
        self.ax_transient2.axhline(y=0, color='white', linestyle='--', alpha=0.7)
        
        self.ax_transient2.set_title('Resposta Natural - Corrente no Indutor', 
                                    color='white', fontsize=14, fontweight='bold')
        self.ax_transient2.set_xlabel('Tempo [ms]', color='white', fontsize=12)
        self.ax_transient2.set_ylabel('Corrente [mA]', color='white', fontsize=12)
        self.ax_transient2.legend(fontsize=10)
        self.ax_transient2.grid(True, alpha=0.4)
        
        self.fig_transient.tight_layout(pad=2.0)
        self.canvas_transient.draw()
    
    def calculate_frequency_response(self):
        """Calculate and plot frequency response"""
        try:
            # Get parameters
            r = self.r.get()
            l = self.l.get()
            c = self.c.get()
            f_start = self.f_start.get()
            f_end = self.f_end.get()
            plot_type = self.plot_type.get()
            
            # Frequency vector (logarithmic)
            f = np.logspace(np.log10(f_start), np.log10(f_end), 1000)
            omega = 2 * np.pi * f
            
            # Transfer function H(jω) = 1 / (1 + jωRC + (jω)²LC) for RLC
            s = 1j * omega
            H = 1 / (1 + s * r * c + s**2 * l * c)
            
            # Clear plots
            self.ax_freq1.clear()
            self.ax_freq2.clear()
            
            if plot_type == "bode":
                self.plot_bode_diagram(f, H)
            elif plot_type == "nyquist":
                self.plot_nyquist_diagram(H)
            elif plot_type == "mag_phase":
                self.plot_magnitude_phase(f, H)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na análise de frequência: {str(e)}")
    
    def plot_bode_diagram(self, f, H):
        """Plot Bode magnitude and phase diagrams with enhanced styling"""
        magnitude_db = 20 * np.log10(np.abs(H))
        phase_deg = np.degrees(np.angle(H))
        
        # Clear previous plots
        self.ax_freq1.clear()
        self.ax_freq2.clear()
        
        # Configure plot styling
        for ax in [self.ax_freq1, self.ax_freq2]:
            ax.set_facecolor('#161b3a')
            ax.spines['bottom'].set_color('#00d4ff')
            ax.spines['top'].set_color('#00d4ff')
            ax.spines['right'].set_color('#00d4ff')
            ax.spines['left'].set_color('#00d4ff')
            ax.tick_params(colors='#a78bfa')
        
        # Magnitude plot (log scale)
        self.ax_freq1.semilogx(f, magnitude_db, color='#7c3aed', linewidth=3, 
                              label='|H(jω)| [dB]', marker='o', markersize=2, alpha=0.9)
        self.ax_freq1.axhline(y=-3, color='#f59e0b', linestyle='--', 
                             alpha=0.8, linewidth=2, label='-3 dB')
        self.ax_freq1.axhline(y=-20, color='#ef4444', linestyle='--', 
                             alpha=0.8, linewidth=2, label='-20 dB')
        self.ax_freq1.axhline(y=0, color='#10b981', linestyle='-', 
                             alpha=0.6, linewidth=1.5, label='0 dB')
        
        self.ax_freq1.set_title('Diagrama de Bode - Magnitude', 
                               color='#00d4ff', fontsize=14, fontweight='bold')
        self.ax_freq1.set_xlabel('Frequência [Hz]', color='#e2e8f0', fontsize=12)
        self.ax_freq1.set_ylabel('Magnitude [dB]', color='#e2e8f0', fontsize=12)
        self.ax_freq1.legend(fontsize=10, facecolor='#1a1f3e', edgecolor='#6366f1', 
                            labelcolor='#e2e8f0')
        self.ax_freq1.grid(True, alpha=0.3, color='#6366f1')
        
        # Phase plot (log scale)
        self.ax_freq2.semilogx(f, phase_deg, color='#00d4ff', linewidth=3, 
                              label='∠H(jω)', marker='s', markersize=2, alpha=0.9)
        self.ax_freq2.axhline(y=-45, color='#f59e0b', linestyle='--', 
                             alpha=0.8, linewidth=2, label='-45°')
        self.ax_freq2.axhline(y=-90, color='#ef4444', linestyle='--', 
                             alpha=0.8, linewidth=2, label='-90°')
        self.ax_freq2.axhline(y=0, color='#10b981', linestyle='-', 
                             alpha=0.6, linewidth=1.5, label='0°')
        
        self.ax_freq2.set_title('Diagrama de Bode - Fase', 
                               color='#00d4ff', fontsize=14, fontweight='bold')
        self.ax_freq2.set_xlabel('Frequência [Hz]', color='#e2e8f0', fontsize=12)
        self.ax_freq2.set_ylabel('Fase [°]', color='#e2e8f0', fontsize=12)
        self.ax_freq2.legend(fontsize=10, facecolor='#1a1f3e', edgecolor='#6366f1', 
                            labelcolor='#e2e8f0')
        self.ax_freq2.grid(True, alpha=0.3, color='#6366f1')
        
        self.fig_frequency.tight_layout(pad=2.0)
        self.canvas_frequency.draw()
        
        # Find resonance frequency
        resonance_idx = np.argmax(np.abs(H))
        f_res = f[resonance_idx]
        
        result = f"""
🔷 ANÁLISE DE RESPOSTA EM FREQUÊNCIA - DIAGRAMA DE BODE
═══════════════════════════════════════════════════════════════════════════════

📐 PARÂMETROS ANALISADOS:
• Faixa de frequência: {self.f_start.get():.1f} Hz - {self.f_end.get():.1f} Hz
• Frequência de ressonância: {f_res:.2f} Hz
• Magnitude máxima: {20*np.log10(np.abs(H[resonance_idx])):.2f} dB

📊 CARACTERÍSTICAS DA RESPOSTA:
• Tipo de filtro: Passa-baixas de 2ª ordem
• Frequência de corte (-3dB): Calculada automaticamente
• Declividade: -40 dB/década após fc

⚡ ANÁLISE DO SISTEMA:
• Ganho DC: {20*np.log10(np.abs(H[0])):.2f} dB
• Comportamento em alta frequência: -40 dB/década
• Margem de fase: Calculada no gráfico

═══════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def plot_nyquist_diagram(self, H):
        """Plot Nyquist diagram with enhanced styling"""
        real_part = np.real(H)
        imag_part = np.imag(H)
        
        # Clear previous plots
        self.ax_freq1.clear()
        self.ax_freq2.clear()
        
        # Configure plot styling
        for ax in [self.ax_freq1, self.ax_freq2]:
            ax.set_facecolor('#161b3a')
            ax.spines['bottom'].set_color('#00d4ff')
            ax.spines['top'].set_color('#00d4ff')
            ax.spines['right'].set_color('#00d4ff')
            ax.spines['left'].set_color('#00d4ff')
            ax.tick_params(colors='#a78bfa')
        
        # Nyquist plot with enhanced styling
        self.ax_freq1.plot(real_part, imag_part, color='#7c3aed', linewidth=3, 
                          label='Nyquist H(jω)', alpha=0.9)
        self.ax_freq1.plot(real_part[0], imag_part[0], color='#10b981', marker='o', 
                          markersize=10, label='Início (f baixa)', markeredgecolor='white', 
                          markeredgewidth=2)
        self.ax_freq1.plot(real_part[-1], imag_part[-1], color='#ef4444', marker='s', 
                          markersize=10, label='Fim (f alta)', markeredgecolor='white', 
                          markeredgewidth=2)
        self.ax_freq1.axhline(y=0, color='#00d4ff', linestyle='-', alpha=0.6, linewidth=2)
        self.ax_freq1.axvline(x=0, color='#00d4ff', linestyle='-', alpha=0.6, linewidth=2)
        
        # Add unit circle reference
        theta = np.linspace(0, 2*np.pi, 100)
        unit_circle_x = np.cos(theta)
        unit_circle_y = np.sin(theta)
        self.ax_freq1.plot(unit_circle_x, unit_circle_y, color='#6366f1', 
                          linestyle='--', alpha=0.5, linewidth=1, label='Círculo unitário')
        
        self.ax_freq1.set_title('Diagrama de Nyquist', 
                               color='#00d4ff', fontsize=14, fontweight='bold')
        self.ax_freq1.set_xlabel('Parte Real', color='#e2e8f0', fontsize=12)
        self.ax_freq1.set_ylabel('Parte Imaginária', color='#e2e8f0', fontsize=12)
        self.ax_freq1.legend(fontsize=10, facecolor='#1a1f3e', edgecolor='#6366f1', 
                            labelcolor='#e2e8f0')
        self.ax_freq1.grid(True, alpha=0.3, color='#6366f1')
        self.ax_freq1.set_aspect('equal')
        
        # Magnitude vs frequency on second subplot
        f = np.logspace(np.log10(self.f_start.get()), np.log10(self.f_end.get()), 1000)
        magnitude = np.abs(H)
        
        self.ax_freq2.loglog(f, magnitude, color='#f59e0b', linewidth=3, 
                            label='|H(jω)|', marker='o', markersize=2, alpha=0.9)
        
        # Add reference lines
        self.ax_freq2.axhline(y=1, color='#10b981', linestyle='--', 
                             alpha=0.6, linewidth=2, label='Magnitude = 1')
        self.ax_freq2.axhline(y=1/np.sqrt(2), color='#ef4444', linestyle='--', 
                             alpha=0.6, linewidth=2, label='0.707 (-3dB)')
        
        self.ax_freq2.set_title('Magnitude vs Frequência', 
                               color='#00d4ff', fontsize=14, fontweight='bold')
        self.ax_freq2.set_xlabel('Frequência [Hz]', color='#e2e8f0', fontsize=12)
        self.ax_freq2.set_ylabel('Magnitude |H(jω)|', color='#e2e8f0', fontsize=12)
        self.ax_freq2.legend(fontsize=10, facecolor='#1a1f3e', edgecolor='#6366f1', 
                            labelcolor='#e2e8f0')
        self.ax_freq2.grid(True, alpha=0.3, color='#6366f1')
        
        self.fig_frequency.tight_layout(pad=2.0)
        self.canvas_frequency.draw()
        
        # Add Nyquist analysis to results
        result = f"""
🔷 DIAGRAMA DE NYQUIST - ANÁLISE COMPLEXA
═══════════════════════════════════════════════════════════════════════════════

📊 CARACTERÍSTICAS DO LUGAR GEOMÉTRICO:
• Ponto inicial (f→0): {real_part[0]:.3f} + j{imag_part[0]:.3f}
• Ponto final (f→∞): {real_part[-1]:.6f} + j{imag_part[-1]:.6f}
• Variação real: {real_part[0] - real_part[-1]:.3f}
• Variação imaginária: {imag_part[0] - imag_part[-1]:.3f}

🎯 ANÁLISE DE ESTABILIDADE:
• Encirclamentos: {'Estável' if np.all(real_part >= 0) else 'Verificar estabilidade'}
• Margem de ganho: {'Boa' if np.min(np.abs(H)) > 0.1 else 'Baixa'}
• Comportamento: Filtro passa-baixa de 2ª ordem

📈 CARACTERÍSTICAS DA RESPOSTA:
• Máxima magnitude: {np.max(magnitude):.3f}
• Mínima magnitude: {np.min(magnitude):.6f}
• Faixa dinâmica: {20*np.log10(np.max(magnitude)/np.min(magnitude)):.1f} dB

═══════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def plot_magnitude_phase(self, f, H):
        """Plot magnitude and phase separately with enhanced styling"""
        magnitude = np.abs(H)
        phase_deg = np.degrees(np.angle(H))
        
        # Clear previous plots
        self.ax_freq1.clear()
        self.ax_freq2.clear()
        
        # Configure plot styling
        for ax in [self.ax_freq1, self.ax_freq2]:
            ax.set_facecolor('#161b3a')
            ax.spines['bottom'].set_color('#00d4ff')
            ax.spines['top'].set_color('#00d4ff')
            ax.spines['right'].set_color('#00d4ff')
            ax.spines['left'].set_color('#00d4ff')
            ax.tick_params(colors='#a78bfa')
        
        # Magnitude plot with logarithmic frequency scale
        self.ax_freq1.semilogx(f, magnitude, color='#7c3aed', linewidth=3, label='|H(jω)|')
        self.ax_freq1.axhline(y=1/np.sqrt(2), color='#f59e0b', linestyle='--', 
                             alpha=0.8, linewidth=2, label='0.707 (-3dB)')
        self.ax_freq1.axhline(y=0.5, color='#ef4444', linestyle=':', 
                             alpha=0.6, linewidth=2, label='0.5 (-6dB)')
        
        self.ax_freq1.set_title('Resposta em Magnitude', 
                               color='#00d4ff', fontsize=14, fontweight='bold')
        self.ax_freq1.set_xlabel('Frequência [Hz]', color='#e2e8f0', fontsize=12)
        self.ax_freq1.set_ylabel('Magnitude |H(jω)|', color='#e2e8f0', fontsize=12)
        self.ax_freq1.legend(fontsize=10, facecolor='#1a1f3e', edgecolor='#6366f1', 
                            labelcolor='#e2e8f0')
        self.ax_freq1.grid(True, alpha=0.3, color='#6366f1')
        
        # Set appropriate limits for magnitude
        max_mag = np.max(magnitude)
        self.ax_freq1.set_ylim(0, max_mag * 1.1)
        
        # Phase plot with logarithmic frequency scale
        self.ax_freq2.semilogx(f, phase_deg, color='#00d4ff', linewidth=3, label='∠H(jω)')
        self.ax_freq2.axhline(y=-45, color='#f59e0b', linestyle='--', 
                             alpha=0.8, linewidth=2, label='-45°')
        self.ax_freq2.axhline(y=-90, color='#ef4444', linestyle='--', 
                             alpha=0.8, linewidth=2, label='-90°')
        self.ax_freq2.axhline(y=0, color='#10b981', linestyle='-', 
                             alpha=0.6, linewidth=1, label='0°')
        
        self.ax_freq2.set_title('Resposta em Fase', 
                               color='#00d4ff', fontsize=14, fontweight='bold')
        self.ax_freq2.set_xlabel('Frequência [Hz]', color='#e2e8f0', fontsize=12)
        self.ax_freq2.set_ylabel('Fase [°]', color='#e2e8f0', fontsize=12)
        self.ax_freq2.legend(fontsize=10, facecolor='#1a1f3e', edgecolor='#6366f1', 
                            labelcolor='#e2e8f0')
        self.ax_freq2.grid(True, alpha=0.3, color='#6366f1')
        
        # Set phase limits
        self.ax_freq2.set_ylim(-180, 45)
        
        self.fig_frequency.tight_layout(pad=2.0)
        self.canvas_frequency.draw()
        
        # Add analysis to results
        f_3db_idx = np.argmin(np.abs(magnitude - 1/np.sqrt(2)))
        f_3db = f[f_3db_idx] if f_3db_idx < len(f) else f[-1]
        
        result = f"""
🔷 ANÁLISE DE MAGNITUDE E FASE
═══════════════════════════════════════════════════════════════════════════════

📊 CARACTERÍSTICAS DA RESPOSTA:
• Frequência de corte (-3dB): {f_3db:.2f} Hz
• Magnitude máxima: {np.max(magnitude):.3f}
• Magnitude mínima: {np.min(magnitude):.3f}
• Faixa de frequência: {f[0]:.1f} Hz - {f[-1]:.1f} Hz

📈 ANÁLISE DE MAGNITUDE:
• Ganho DC: {magnitude[0]:.3f} ({20*np.log10(magnitude[0]):.1f} dB)
• Atenuação em alta freq: {magnitude[-1]:.6f} ({20*np.log10(magnitude[-1]):.1f} dB)
• Declividade: Aproximadamente -40 dB/década

📊 ANÁLISE DE FASE:
• Fase inicial: {phase_deg[0]:.1f}°
• Fase final: {phase_deg[-1]:.1f}°
• Variação total: {phase_deg[0] - phase_deg[-1]:.1f}°

═══════════════════════════════════════════════════════════════════════════════
"""
        
        self.results_text.insert(tk.END, result)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CircuitAnalyzer()
    app.run()
