import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import time

class CircuitAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ ANÁLISE CIRCUITO PRO - Análise Básica de Circuitos RLC")
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
        
        # Animation variables
        self.animation_running = False
        self.animation_speed = tk.DoubleVar(value=1.0)
        self.current_animation = None
        self.time_offset = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create gradient-like header
        header_frame = tk.Frame(self.root, bg='#0a0e27', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title with modern styling
        title_container = tk.Frame(header_frame, bg='#161b3a')
        title_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(title_container, text="⚡ CIRCUIT ANALYZER BASIC", 
                              font=("Segoe UI", 24, "bold"), fg='#00d4ff', bg='#161b3a')
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(title_container, text="v1.0 Educational", 
                                font=("Segoe UI", 10), fg='#7c3aed', bg='#161b3a')
        version_label.pack(side=tk.RIGHT, anchor='se')
        
        subtitle_label = tk.Label(title_container, text="🔬 Análise Básica de Circuitos RLC - Engenharia da Computação", 
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
        
        self.entries = {}
        for i, (label, var) in enumerate(params):
            frame = tk.Frame(params_frame, bg='#1a1f3e')
            frame.pack(fill=tk.X, padx=8, pady=4)
            
            label_widget = tk.Label(frame, text=label, font=("Segoe UI", 10), 
                                   fg='#e2e8f0', bg='#1a1f3e', width=18, anchor='w')
            label_widget.pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, textvariable=var, font=("Segoe UI", 10), 
                           bg='#374151', fg='#f9fafb', bd=1, relief=tk.FLAT,
                           insertbackground='#00d4ff', width=12)
            entry.pack(side=tk.RIGHT, padx=(5, 0))
            self.entries[label] = entry
        
        # Action buttons with modern styling
        buttons_frame = tk.Frame(self.sidebar, bg='#1a1f3e')
        buttons_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Calculate button
        calc_btn = tk.Button(buttons_frame, text="🔄 Calcular Circuito",
                            command=self.calculate_circuit,
                            font=("Segoe UI", 11, "bold"), bg='#10b981', fg='white',
                            relief=tk.FLAT, bd=0, pady=10, cursor='hand2')
        calc_btn.pack(fill=tk.X, pady=3)
        
        # Analyze button
        analyze_btn = tk.Button(buttons_frame, text="📊 Analisar Sinais",
                               command=self.analyze_circuit,
                               font=("Segoe UI", 11, "bold"), bg='#3b82f6', fg='white',
                               relief=tk.FLAT, bd=0, pady=10, cursor='hand2')
        analyze_btn.pack(fill=tk.X, pady=3)
        
        # Plot signals button
        signals_btn = tk.Button(buttons_frame, text="📈 Plotar Sinais",
                               command=self.plot_signals,
                               font=("Segoe UI", 11, "bold"), bg='#8b5cf6', fg='white',
                               relief=tk.FLAT, bd=0, pady=10, cursor='hand2')
        signals_btn.pack(fill=tk.X, pady=3)
        
        # Plot phasor button
        phasor_btn = tk.Button(buttons_frame, text="⚡ Diagrama Fasorial",
                              command=self.plot_phasor_diagrams,
                              font=("Segoe UI", 11, "bold"), bg='#f59e0b', fg='white',
                              relief=tk.FLAT, bd=0, pady=10, cursor='hand2')
        phasor_btn.pack(fill=tk.X, pady=3)
    
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
        # Animation controls frame
        controls_frame = tk.Frame(self.signals_frame, bg='#161b3a', height=80)
        controls_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        controls_frame.pack_propagate(False)
        
        # Animation control buttons
        btn_frame = tk.Frame(controls_frame, bg='#161b3a')
        btn_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(btn_frame, text="🎬 CONTROLES DE ANIMAÇÃO", 
                 bg='#161b3a', fg='#00d4ff', font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
        
        self.anim_btn = tk.Button(btn_frame, text="▶️ INICIAR ANIMAÇÃO", 
                                  command=self.plot_signals,
                                  bg='#10b981', fg='white', font=("Segoe UI", 10, "bold"),
                                  relief=tk.FLAT, bd=0, padx=15, pady=5)
        self.anim_btn.pack(side=tk.LEFT, padx=(20, 10))
        
        # Speed control
        speed_frame = tk.Frame(controls_frame, bg='#161b3a')
        speed_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(speed_frame, text="⚡ Velocidade:", 
                 bg='#161b3a', fg='#e2e8f0', font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        speed_scale = tk.Scale(speed_frame, variable=self.animation_speed, from_=0.1, to=3.0, 
                               resolution=0.1, orient=tk.HORIZONTAL, bg='#161b3a', fg='#00d4ff',
                               activebackground='#3b82f6', troughcolor='#374151', highlightthickness=0,
                               font=("Segoe UI", 9))
        speed_scale.pack(side=tk.LEFT, padx=(10, 0))
        
        # Info label
        info_frame = tk.Frame(controls_frame, bg='#161b3a')
        info_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(info_frame, text="📊 Gráficos em movimento mostram evolução temporal dos sinais", 
                 bg='#161b3a', fg='#a78bfa', font=("Segoe UI", 10, "italic")).pack()
        
        # Signals analysis interface
        signals_container = tk.Frame(self.signals_frame, bg='#0f172a')
        signals_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Matplotlib figure for signals
        self.fig_signals, self.ax_signals = plt.subplots(3, 1, figsize=(12, 10), facecolor='#1e293b')
        
        for ax in self.ax_signals:
            ax.set_facecolor('#334155')
            ax.spines['bottom'].set_color('#64748b')
            ax.spines['top'].set_color('#64748b')
            ax.spines['right'].set_color('#64748b')
            ax.spines['left'].set_color('#64748b')
            ax.tick_params(colors='white')
        
        self.canvas_signals = FigureCanvasTkAgg(self.fig_signals, signals_container)
        self.canvas_signals.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_phasor_tab(self):
        # Phasor diagram interface
        phasor_container = tk.Frame(self.phasor_frame, bg='#0f172a')
        phasor_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Matplotlib figure for phasor diagrams
        self.fig_phasor, self.ax_phasor = plt.subplots(1, 2, figsize=(12, 6), facecolor='#1e293b')
        
        for ax in self.ax_phasor:
            ax.set_facecolor('#334155')
            ax.spines['bottom'].set_color('#64748b')
            ax.spines['top'].set_color('#64748b')
            ax.spines['right'].set_color('#64748b')
            ax.spines['left'].set_color('#64748b')
            ax.tick_params(colors='white')
        
        self.canvas_phasor = FigureCanvasTkAgg(self.fig_phasor, phasor_container)
        self.canvas_phasor.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_circuit_tab(self):
        # Circuit visualization interface
        circuit_container = tk.Frame(self.circuit_frame, bg='#0f172a')
        circuit_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Circuit type selector
        controls_frame = tk.Frame(circuit_container, bg='#1e293b', width=250, relief=tk.RAISED, bd=2)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        controls_frame.pack_propagate(False)
        
        # Right: Circuit drawing
        drawing_frame = tk.Frame(circuit_container, bg='#1e293b', relief=tk.RAISED, bd=2)
        drawing_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Circuit type selection
        circuit_title = tk.Label(controls_frame, text="TIPOS DE CIRCUITO", 
                                 font=("Arial", 11, "bold"), fg='#3b82f6', bg='#1e293b')
        circuit_title.pack(pady=(15, 10))
        
        # Circuit type variable
        self.circuit_type = tk.StringVar(value="rlc_series")
        
        # Circuit options
        circuit_options = [
            ("RLC Série", "rlc_series"),
            ("RLC Paralelo", "rlc_parallel"),
            ("Malhas DC", "dc_mesh")
        ]
        
        for text, value in circuit_options:
            rb = tk.Radiobutton(controls_frame, text=text, variable=self.circuit_type, value=value,
                               font=("Arial", 10), fg='white', bg='#1e293b', 
                               selectcolor='#3b82f6', command=self.update_circuit_drawing)
            rb.pack(anchor='w', padx=15, pady=5)
        
        # Matplotlib figure for circuit drawing
        self.fig_circuit, self.ax_circuit = plt.subplots(1, 1, figsize=(10, 8), facecolor='#1e293b')
        self.ax_circuit.set_facecolor('#334155')
        self.ax_circuit.spines['bottom'].set_color('#64748b')
        self.ax_circuit.spines['top'].set_color('#64748b')
        self.ax_circuit.spines['right'].set_color('#64748b')
        self.ax_circuit.spines['left'].set_color('#64748b')
        self.ax_circuit.tick_params(colors='white')
        
        self.canvas_circuit = FigureCanvasTkAgg(self.fig_circuit, drawing_frame)
        self.canvas_circuit.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Draw initial circuit
        self.update_circuit_drawing()
    
    def setup_results_tab(self):
        # Modern results display with header
        header_results = tk.Frame(self.results_frame, bg='#161b3a', height=50)
        header_results.pack(fill=tk.X, pady=(0, 15))
        header_results.pack_propagate(False)
        
        header_title = tk.Label(header_results, text="📊 RELATÓRIOS E ANÁLISES DETALHADAS", 
                               font=("Segoe UI", 16, "bold"), fg='#00d4ff', bg='#161b3a')
        header_title.pack(pady=15)
        
        # Scrollable text area with modern styling
        self.results_text = scrolledtext.ScrolledText(
            self.results_frame,
            font=("Consolas", 10),
            bg='#1f2937',
            fg='#f9fafb',
            insertbackground='#00d4ff',
            selectbackground='#374151',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=15,
            wrap=tk.WORD
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Clear button
        clear_btn = tk.Button(self.results_frame, text="🗑️ Limpar Resultados",
                             command=lambda: self.results_text.delete(1.0, tk.END),
                             font=("Segoe UI", 10, "bold"), bg='#ef4444', fg='white',
                             relief=tk.FLAT, bd=0, pady=8)
        clear_btn.pack(pady=(0, 15))

    def calculate_circuit(self):
        """Perform basic circuit calculations"""
        try:
            f = self.f.get()
            vm = self.vm.get()
            im = self.im.get()
            theta_v = math.radians(self.theta_v.get())
            theta_i = math.radians(self.theta_i.get())
            
            # Calculate RMS values
            vrms = vm / math.sqrt(2)
            irms = im / math.sqrt(2)
            
            # Calculate power factor
            phase_diff = theta_v - theta_i
            fp = math.cos(phase_diff)
            
            # Calculate powers
            p_active = vrms * irms * fp
            q_reactive = vrms * irms * math.sin(phase_diff)
            s_apparent = vrms * irms
            
            result = f"""
🔷 CÁLCULOS BÁSICOS DO CIRCUITO
═══════════════════════════════════════════════════════════════════════════════

📐 PARÂMETROS DE ENTRADA:
• Frequência: {f:.1f} Hz
• Tensão máxima: {vm:.1f} V
• Corrente máxima: {im:.1f} A
• Ângulo da tensão: {math.degrees(theta_v):.1f}°
• Ângulo da corrente: {math.degrees(theta_i):.1f}°

⚡ VALORES CALCULADOS:
• Tensão RMS: {vrms:.2f} V
• Corrente RMS: {irms:.2f} A
• Defasagem: {math.degrees(phase_diff):.1f}°
• Fator de potência: {fp:.3f}

🔋 ANÁLISE DE POTÊNCIAS:
• Potência ativa: {p_active:.1f} W
• Potência reativa: {q_reactive:.1f} VAr
• Potência aparente: {s_apparent:.1f} VA

═══════════════════════════════════════════════════════════════════════════════
"""
            
            self.results_text.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro nos cálculos: {str(e)}")
    
    def analyze_circuit(self):
        """Analyze circuit components"""
        try:
            r = self.r.get()
            l = self.l.get()
            c = self.c.get()
            f = self.f.get()
            
            # Calculate reactances
            xl = 2 * math.pi * f * l
            xc = 1 / (2 * math.pi * f * c)
            
            # Total impedance
            z_total = complex(r, xl - xc)
            z_mag = abs(z_total)
            z_angle = math.degrees(cmath.phase(z_total))
            
            result = f"""
🔷 ANÁLISE DOS COMPONENTES
═══════════════════════════════════════════════════════════════════════════════

🔧 COMPONENTES:
• Resistência: {r:.1f} Ω
• Indutância: {l:.6f} H ({l*1000:.3f} mH)
• Capacitância: {c:.9f} F ({c*1000000:.1f} μF)

⚡ REATÂNCIAS:
• XL = 2πfL = {xl:.2f} Ω
• XC = 1/(2πfC) = {xc:.2f} Ω
• X = XL - XC = {xl-xc:.2f} Ω

🎯 IMPEDÂNCIA TOTAL:
• Z = {r:.1f} + j{xl-xc:.2f} Ω
• |Z| = {z_mag:.2f} Ω
• ∠Z = {z_angle:.1f}°

📊 CARACTERÍSTICAS:
• Tipo: {'Indutivo' if xl > xc else 'Capacitivo' if xc > xl else 'Resistivo'}
• Frequência de ressonância: {1/(2*math.pi*math.sqrt(l*c)):.1f} Hz

═══════════════════════════════════════════════════════════════════════════════
"""
            
            self.results_text.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na análise: {str(e)}")
    
    def plot_signals(self):
        """Plot voltage, current and power signals with animation"""
        try:
            # Stop any existing animation
            if self.current_animation:
                self.current_animation.event_source.stop()
            
            # Clear previous plots
            for ax in self.ax_signals:
                ax.clear()
            
            # Parameters
            f = self.f.get()
            vm = self.vm.get()
            im = self.im.get()
            theta_v = math.radians(self.theta_v.get())
            theta_i = math.radians(self.theta_i.get())
            
            # Time vector (3 periods)
            t_final = 3 / f
            t = np.linspace(0, t_final, 1000)
            omega = 2 * math.pi * f
            
            # Configure axes style
            for ax in self.ax_signals:
                ax.set_facecolor('#161b3a')
                ax.spines['bottom'].set_color('#00d4ff')
                ax.spines['top'].set_color('#00d4ff')
                ax.spines['right'].set_color('#00d4ff')
                ax.spines['left'].set_color('#00d4ff')
                ax.tick_params(colors='#a78bfa')
                ax.grid(True, alpha=0.3, color='#6366f1')
            
            # Initialize line objects for animation
            self.v_line, = self.ax_signals[0].plot([], [], color='#ef4444', linewidth=3, label='v(t)')
            self.i_line, = self.ax_signals[1].plot([], [], color='#3b82f6', linewidth=3, label='i(t)')
            self.p_line, = self.ax_signals[2].plot([], [], color='#10b981', linewidth=3, label='p(t)')
            
            # Moving point indicators
            self.v_point, = self.ax_signals[0].plot([], [], 'o', color='#fbbf24', markersize=8)
            self.i_point, = self.ax_signals[1].plot([], [], 'o', color='#fbbf24', markersize=8)
            self.p_point, = self.ax_signals[2].plot([], [], 'o', color='#fbbf24', markersize=8)
            
            # Set up axes
            self.ax_signals[0].set_xlim(0, t_final * 1000)
            self.ax_signals[0].set_ylim(-vm * 1.1, vm * 1.1)
            self.ax_signals[0].set_title('Tensão v(t) - EM MOVIMENTO', color='#00d4ff', fontsize=14, fontweight='bold')
            self.ax_signals[0].set_ylabel('Tensão [V]', color='#e2e8f0')
            self.ax_signals[0].legend()
            
            self.ax_signals[1].set_xlim(0, t_final * 1000)
            self.ax_signals[1].set_ylim(-im * 1.1, im * 1.1)
            self.ax_signals[1].set_title('Corrente i(t) - EM MOVIMENTO', color='#00d4ff', fontsize=14, fontweight='bold')
            self.ax_signals[1].set_ylabel('Corrente [A]', color='#e2e8f0')
            self.ax_signals[1].legend()
            
            p_max = max(abs(vm * im), 1)
            self.ax_signals[2].set_xlim(0, t_final * 1000)
            self.ax_signals[2].set_ylim(-p_max * 1.1, p_max * 1.1)
            self.ax_signals[2].set_title('Potência p(t) - EM MOVIMENTO', color='#00d4ff', fontsize=14, fontweight='bold')
            self.ax_signals[2].set_xlabel('Tempo [ms]', color='#e2e8f0')
            self.ax_signals[2].set_ylabel('Potência [W]', color='#e2e8f0')
            self.ax_signals[2].legend()
            
            # Animation function
            def animate(frame):
                # Time progression
                current_time = frame * 0.05 * self.animation_speed.get()  # Adjustable speed
                
                # Calculate how many points to show (progressive drawing)
                num_points = int((current_time / t_final) * len(t))
                if num_points > len(t):
                    num_points = len(t)
                
                if num_points > 0:
                    # Get current time arrays
                    t_current = t[:num_points]
                    
                    # Calculate signals
                    v_current = vm * np.sin(omega * t_current + theta_v)
                    i_current = im * np.sin(omega * t_current + theta_i)
                    p_current = v_current * i_current
                    
                    # Update lines (progressive drawing)
                    self.v_line.set_data(t_current * 1000, v_current)
                    self.i_line.set_data(t_current * 1000, i_current)
                    self.p_line.set_data(t_current * 1000, p_current)
                    
                    # Update moving points (current position)
                    if len(t_current) > 0:
                        self.v_point.set_data([t_current[-1] * 1000], [v_current[-1]])
                        self.i_point.set_data([t_current[-1] * 1000], [i_current[-1]])
                        self.p_point.set_data([t_current[-1] * 1000], [p_current[-1]])
                
                return [self.v_line, self.i_line, self.p_line, self.v_point, self.i_point, self.p_point]
            
            # Start animation
            self.current_animation = FuncAnimation(
                self.fig_signals, animate, frames=200, interval=50, blit=False, repeat=True
            )
            
            self.fig_signals.tight_layout(pad=2.0)
            self.canvas_signals.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao plotar sinais: {str(e)}")
    
    def toggle_animation(self):
        """Toggle animation on/off"""
        if self.current_animation:
            if self.animation_running:
                self.current_animation.event_source.stop()
                self.animation_running = False
            else:
                self.current_animation.event_source.start()
                self.animation_running = True
    
    def plot_phasor_diagrams(self):
        """Plot phasor diagrams for voltage and current"""
        try:
            # Clear previous plots
            for ax in self.ax_phasor:
                ax.clear()
            
            # Parameters
            vm = self.vm.get()
            im = self.im.get()
            theta_v = math.radians(self.theta_v.get())
            theta_i = math.radians(self.theta_i.get())
            
            # Phasor representation
            v_real = vm * math.cos(theta_v)
            v_imag = vm * math.sin(theta_v)
            i_real = im * math.cos(theta_i)
            i_imag = im * math.sin(theta_i)
            
            # Configure axes style
            for ax in self.ax_phasor:
                ax.set_facecolor('#161b3a')
                ax.spines['bottom'].set_color('#00d4ff')
                ax.spines['top'].set_color('#00d4ff')
                ax.spines['right'].set_color('#00d4ff')
                ax.spines['left'].set_color('#00d4ff')
                ax.tick_params(colors='#a78bfa')
                ax.grid(True, alpha=0.3, color='#6366f1')
                ax.set_aspect('equal')
            
            # Voltage phasor - with proper scaling
            max_v = max(abs(vm), 1)  # Prevent zero scale
            v_limit = max_v * 1.2
            
            self.ax_phasor[0].arrow(0, 0, v_real, v_imag, head_width=max_v*0.05, 
                                   head_length=max_v*0.08, fc='#ef4444', ec='#ef4444', linewidth=3)
            self.ax_phasor[0].set_xlim(-v_limit, v_limit)
            self.ax_phasor[0].set_ylim(-v_limit, v_limit)
            self.ax_phasor[0].set_title('Fasor Tensão', color='#00d4ff', fontsize=14, fontweight='bold')
            self.ax_phasor[0].set_xlabel('Parte Real [V]', color='#e2e8f0')
            self.ax_phasor[0].set_ylabel('Parte Imaginária [V]', color='#e2e8f0')
            
            # Add circular reference grid
            circle = plt.Circle((0, 0), max_v, fill=False, color='#4ade80', alpha=0.3, linestyle='--')
            self.ax_phasor[0].add_patch(circle)
            
            # Add magnitude and angle text
            self.ax_phasor[0].text(0.1*v_limit, 0.8*v_limit, 
                                  f'|V| = {vm:.1f} V\n∠V = {math.degrees(theta_v):.1f}°\nReal: {v_real:.1f} V\nImag: {v_imag:.1f} V', 
                                  bbox=dict(boxstyle="round,pad=0.3", facecolor='#1a1f3e', alpha=0.9),
                                  color='#00d4ff', fontsize=10, fontweight='bold')
            
            # Current phasor - with proper scaling
            max_i = max(abs(im), 1)  # Prevent zero scale
            i_limit = max_i * 1.2
            
            self.ax_phasor[1].arrow(0, 0, i_real, i_imag, head_width=max_i*0.05, 
                                   head_length=max_i*0.08, fc='#3b82f6', ec='#3b82f6', linewidth=3)
            self.ax_phasor[1].set_xlim(-i_limit, i_limit)
            self.ax_phasor[1].set_ylim(-i_limit, i_limit)
            self.ax_phasor[1].set_title('Fasor Corrente', color='#00d4ff', fontsize=14, fontweight='bold')
            self.ax_phasor[1].set_xlabel('Parte Real [A]', color='#e2e8f0')
            self.ax_phasor[1].set_ylabel('Parte Imaginária [A]', color='#e2e8f0')
            
            # Add circular reference grid
            circle = plt.Circle((0, 0), max_i, fill=False, color='#4ade80', alpha=0.3, linestyle='--')
            self.ax_phasor[1].add_patch(circle)
            
            # Add magnitude and angle text
            self.ax_phasor[1].text(0.1*i_limit, 0.8*i_limit, 
                                  f'|I| = {im:.1f} A\n∠I = {math.degrees(theta_i):.1f}°\nReal: {i_real:.1f} A\nImag: {i_imag:.1f} A', 
                                  bbox=dict(boxstyle="round,pad=0.3", facecolor='#1a1f3e', alpha=0.9),
                                  color='#00d4ff', fontsize=10, fontweight='bold')
            
            # Add phase difference annotation
            phase_diff = math.degrees(theta_v - theta_i)
            self.ax_phasor[1].text(-0.9*i_limit, -0.9*i_limit, 
                                  f'Defasagem V-I: {phase_diff:.1f}°\nFator de Potência: {math.cos(math.radians(phase_diff)):.3f}', 
                                  bbox=dict(boxstyle="round,pad=0.3", facecolor='#ef4444', alpha=0.9),
                                  color='white', fontsize=10, fontweight='bold')
            
            self.fig_phasor.tight_layout(pad=2.0)
            self.canvas_phasor.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao plotar fasores: {str(e)}")
    
    def update_circuit_drawing(self):
        """Update circuit diagram based on selected type"""
        try:
            self.ax_circuit.clear()
            self.ax_circuit.set_facecolor('#161b3a')
            
            circuit_type = self.circuit_type.get()
            
            if circuit_type == "rlc_series":
                self.draw_rlc_series()
            elif circuit_type == "rlc_parallel":
                self.draw_rlc_parallel()
            elif circuit_type == "dc_mesh":
                self.draw_dc_mesh()
            
            self.ax_circuit.set_xlim(-1, 11)
            self.ax_circuit.set_ylim(-1, 6)
            self.ax_circuit.set_aspect('equal')
            self.ax_circuit.axis('off')
            self.canvas_circuit.draw()
            
        except Exception as e:
            print(f"Erro ao desenhar circuito: {e}")
    
    def draw_rlc_series(self):
        """Draw RLC series circuit"""
        # Voltage source
        circle = patches.Circle((1, 3), 0.5, linewidth=3, edgecolor='#10b981', facecolor='none')
        self.ax_circuit.add_patch(circle)
        self.ax_circuit.text(1, 3, 'V', ha='center', va='center', color='#10b981', fontsize=12, fontweight='bold')
        
        # Resistor
        rect = patches.Rectangle((3, 2.5), 1.5, 1, linewidth=3, edgecolor='#ef4444', facecolor='none')
        self.ax_circuit.add_patch(rect)
        self.ax_circuit.text(3.75, 3, 'R', ha='center', va='center', color='#ef4444', fontsize=12, fontweight='bold')
        
        # Inductor (coil)
        for i in range(4):
            circle = patches.Circle((5.5 + i*0.3, 3), 0.15, linewidth=2, edgecolor='#3b82f6', facecolor='none')
            self.ax_circuit.add_patch(circle)
        self.ax_circuit.text(6, 2.3, 'L', ha='center', va='center', color='#3b82f6', fontsize=12, fontweight='bold')
        
        # Capacitor
        self.ax_circuit.plot([8, 8], [2.3, 3.7], 'white', linewidth=4)
        self.ax_circuit.plot([8.3, 8.3], [2.3, 3.7], 'white', linewidth=4)
        self.ax_circuit.text(8.15, 2, 'C', ha='center', va='center', color='white', fontsize=12, fontweight='bold')
        
        # Connecting wires
        self.ax_circuit.plot([1.5, 3], [3, 3], 'white', linewidth=2)  # V to R
        self.ax_circuit.plot([4.5, 5.2], [3, 3], 'white', linewidth=2)  # R to L
        self.ax_circuit.plot([6.8, 8], [3, 3], 'white', linewidth=2)  # L to C
        self.ax_circuit.plot([8.3, 9.5], [3, 3], 'white', linewidth=2)  # C to bottom
        self.ax_circuit.plot([9.5, 9.5], [3, 1], 'white', linewidth=2)  # Right vertical
        self.ax_circuit.plot([9.5, 1], [1, 1], 'white', linewidth=2)  # Bottom horizontal
        self.ax_circuit.plot([1, 1], [1, 2.5], 'white', linewidth=2)  # Left vertical
        
        self.ax_circuit.set_title('Circuito RLC Série', color='#00d4ff', fontsize=16, fontweight='bold', pad=20)
    
    def draw_rlc_parallel(self):
        """Draw RLC parallel circuit"""
        # Voltage source
        circle = patches.Circle((2, 3), 0.5, linewidth=3, edgecolor='#10b981', facecolor='none')
        self.ax_circuit.add_patch(circle)
        self.ax_circuit.text(2, 3, 'V', ha='center', va='center', color='#10b981', fontsize=12, fontweight='bold')
        
        # Top horizontal line
        self.ax_circuit.plot([3, 9], [4.5, 4.5], 'white', linewidth=2)
        # Bottom horizontal line  
        self.ax_circuit.plot([3, 9], [1.5, 1.5], 'white', linewidth=2)
        # Left vertical connections
        self.ax_circuit.plot([2.5, 3], [3, 3], 'white', linewidth=2)
        self.ax_circuit.plot([3, 3], [1.5, 4.5], 'white', linewidth=2)
        # Right vertical connection
        self.ax_circuit.plot([9, 9], [1.5, 4.5], 'white', linewidth=2)
        
        # Resistor branch
        rect = patches.Rectangle((4, 2.5), 1, 1, linewidth=3, edgecolor='#ef4444', facecolor='none')
        self.ax_circuit.add_patch(rect)
        self.ax_circuit.text(4.5, 3, 'R', ha='center', va='center', color='#ef4444', fontsize=12, fontweight='bold')
        self.ax_circuit.plot([4, 4], [1.5, 2.5], 'white', linewidth=2)
        self.ax_circuit.plot([5, 5], [1.5, 2.5], 'white', linewidth=2)
        self.ax_circuit.plot([4, 4], [3.5, 4.5], 'white', linewidth=2)
        self.ax_circuit.plot([5, 5], [3.5, 4.5], 'white', linewidth=2)
        
        # Inductor branch
        for i in range(3):
            circle = patches.Circle((6.2 + i*0.25, 3), 0.12, linewidth=2, edgecolor='#3b82f6', facecolor='none')
            self.ax_circuit.add_patch(circle)
        self.ax_circuit.plot([6, 6], [1.5, 3], 'white', linewidth=2)
        self.ax_circuit.plot([7, 7], [1.5, 3], 'white', linewidth=2)
        self.ax_circuit.plot([6, 6], [3, 4.5], 'white', linewidth=2)
        self.ax_circuit.plot([7, 7], [3, 4.5], 'white', linewidth=2)
        self.ax_circuit.text(6.5, 2.3, 'L', ha='center', va='center', color='#3b82f6', fontsize=10, fontweight='bold')
        
        # Capacitor branch
        self.ax_circuit.plot([8, 8], [2.3, 3.7], 'white', linewidth=4)
        self.ax_circuit.plot([8.2, 8.2], [2.3, 3.7], 'white', linewidth=4)
        self.ax_circuit.plot([8.1, 8.1], [1.5, 2.3], 'white', linewidth=2)
        self.ax_circuit.plot([8.1, 8.1], [3.7, 4.5], 'white', linewidth=2)
        self.ax_circuit.text(8.1, 2, 'C', ha='center', va='center', color='white', fontsize=10, fontweight='bold')
        
        # Source connections
        self.ax_circuit.plot([2, 2], [1.5, 2.5], 'white', linewidth=2)
        self.ax_circuit.plot([2, 2], [3.5, 4.5], 'white', linewidth=2)
        
        self.ax_circuit.set_title('Circuito RLC Paralelo', color='#00d4ff', fontsize=16, fontweight='bold', pad=20)
    
    def draw_dc_mesh(self):
        """Draw DC mesh analysis example"""
        # Mesh 1 - Left
        # Voltage source 1
        circle = patches.Circle((2, 4), 0.4, linewidth=3, edgecolor='#10b981', facecolor='none')
        self.ax_circuit.add_patch(circle)
        self.ax_circuit.text(2, 4, 'V₁', ha='center', va='center', color='#10b981', fontsize=10, fontweight='bold')
        
        # Resistor R1
        rect = patches.Rectangle((3.5, 3.5), 1, 1, linewidth=3, edgecolor='#ef4444', facecolor='none')
        self.ax_circuit.add_patch(rect)
        self.ax_circuit.text(4, 4, 'R₁', ha='center', va='center', color='#ef4444', fontsize=10, fontweight='bold')
        
        # Mesh 2 - Right  
        # Voltage source 2
        circle = patches.Circle((8, 4), 0.4, linewidth=3, edgecolor='#10b981', facecolor='none')
        self.ax_circuit.add_patch(circle)
        self.ax_circuit.text(8, 4, 'V₂', ha='center', va='center', color='#10b981', fontsize=10, fontweight='bold')
        
        # Shared resistor R2
        rect = patches.Rectangle((5.5, 3.5), 1, 1, linewidth=3, edgecolor='#f59e0b', facecolor='none')
        self.ax_circuit.add_patch(rect)
        self.ax_circuit.text(6, 4, 'R₂', ha='center', va='center', color='#f59e0b', fontsize=10, fontweight='bold')
        
        # Resistor R3
        rect = patches.Rectangle((7.5, 2), 1, 1, linewidth=3, edgecolor='#8b5cf6', facecolor='none')
        self.ax_circuit.add_patch(rect)
        self.ax_circuit.text(8, 2.5, 'R₃', ha='center', va='center', color='#8b5cf6', fontsize=10, fontweight='bold')
        
        # Connecting wires
        # Left mesh
        self.ax_circuit.plot([2, 2], [2, 3.6], 'white', linewidth=2)
        self.ax_circuit.plot([2, 3.5], [2, 2], 'white', linewidth=2)
        self.ax_circuit.plot([2.4, 3.5], [4, 4], 'white', linewidth=2)
        self.ax_circuit.plot([4.5, 5.5], [4, 4], 'white', linewidth=2)
        self.ax_circuit.plot([6, 6], [2, 3.5], 'white', linewidth=2)
        self.ax_circuit.plot([3.5, 6], [2, 2], 'white', linewidth=2)
        
        # Right mesh  
        self.ax_circuit.plot([6.5, 7.6], [4, 4], 'white', linewidth=2)
        self.ax_circuit.plot([8.4, 8.5], [4, 4], 'white', linewidth=2)
        self.ax_circuit.plot([8.5, 8.5], [2, 4], 'white', linewidth=2)
        self.ax_circuit.plot([8, 8], [2, 3.6], 'white', linewidth=2)
        self.ax_circuit.plot([7.5, 8.5], [2, 2], 'white', linewidth=2)
        
        # Current arrows
        self.ax_circuit.annotate('I₁', xy=(3, 3), xytext=(2.5, 3.5), 
                                arrowprops=dict(arrowstyle='->', color='#06d6a0', lw=2),
                                color='#06d6a0', fontsize=12, fontweight='bold')
        self.ax_circuit.annotate('I₂', xy=(7.5, 3), xytext=(7, 3.5), 
                                arrowprops=dict(arrowstyle='->', color='#06d6a0', lw=2),
                                color='#06d6a0', fontsize=12, fontweight='bold')
        
        self.ax_circuit.set_title('Análise de Malhas DC', color='#00d4ff', fontsize=16, fontweight='bold', pad=20)

if __name__ == "__main__":
    app = CircuitAnalyzer()
    app.root.mainloop()
