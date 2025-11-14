import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import base64
import io

# Configuração da página
st.set_page_config(
    page_title="Analisador de Circuitos Elétricos Avançado",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session state
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# CSS personalizado melhorado
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #17a2b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1f77b4;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #1f77b4;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .preset-button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        margin: 0.2rem;
        transition: all 0.3s ease;
    }
    .preset-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        display: flex;
        justify-content: center;
        padding: 0.5rem;
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        gap: 8px;
        padding: 12px 20px;
        font-weight: 600;
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f77b4 0%, #17a2b8 100%);
        color: white;
        border: 2px solid #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(31, 119, 180, 0.3);
    }
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedCircuitAnalyzer:
    """Calculadora avançada para análise de circuitos elétricos"""
    
    def __init__(self):
        self.tolerance = 1e-6
    
    def validate_inputs(self, f, vm, im):
        """Valida entradas do usuário"""
        errors = []
        if f <= 0:
            errors.append("Frequência deve ser positiva")
        if vm <= 0:
            errors.append("Tensão máxima deve ser positiva")
        if im <= 0:
            errors.append("Corrente máxima deve ser positiva")
        return errors
    
    def calculate_rms_values(self, vm, im):
        """Calcula valores eficazes (RMS)"""
        return vm / np.sqrt(2), im / np.sqrt(2)
    
    def calculate_power_factor(self, theta_v_deg, theta_i_deg):
        """Calcula fator de potência"""
        return np.cos(np.radians(abs(theta_v_deg - theta_i_deg)))
    
    def determine_circuit_type(self, theta_v_deg, theta_i_deg):
        """Determina tipo de circuito com lógica melhorada"""
        phase_diff = self._normalize_phase_difference(theta_v_deg - theta_i_deg)
        phase_diff_abs = abs(phase_diff)
        
        if phase_diff_abs < 1:
            return "🔴 Em fase (resistivo)", phase_diff_abs, "#28a745"
        elif abs(phase_diff_abs - 90) < 1:
            if phase_diff < 0:
                return "🔵 Adiantado (puramente capacitivo)", phase_diff_abs, "#007bff"
            else:
                return "🟡 Atrasado (puramente indutivo)", phase_diff_abs, "#ffc107"
        elif phase_diff < 0:
            return "🟦 Adiantado (capacitivo)", phase_diff_abs, "#17a2b8"
        else:
            return "🟨 Atrasado (indutivo)", phase_diff_abs, "#fd7e14"
    
    def _normalize_phase_difference(self, phase_diff):
        """Normaliza diferença de fase para -180 a 180 graus"""
        while phase_diff > 180:
            phase_diff -= 360
        while phase_diff < -180:
            phase_diff += 360
        return phase_diff
    
    def calculate_powers(self, vrms, irms, theta_v_deg, theta_i_deg):
        """Calcula todas as potências"""
        phase_diff_rad = np.radians(theta_v_deg - theta_i_deg)
        s_apparent = vrms * irms
        p_active = s_apparent * np.cos(phase_diff_rad)
        q_reactive = s_apparent * np.sin(phase_diff_rad)
        
        return {
            'apparent': s_apparent,
            'active': p_active,
            'reactive': q_reactive,
            'reactive_abs': abs(q_reactive),
            'power_factor': np.cos(phase_diff_rad)
        }
    
    def calculate_impedance(self, vrms, irms, theta_v_rad, theta_i_rad):
        """Calcula impedância complexa"""
        if irms < self.tolerance:
            return complex(float('inf'), 0), float('inf'), 0
        
        v_phasor = vrms * np.exp(1j * theta_v_rad)
        i_phasor = irms * np.exp(1j * theta_i_rad)
        z_complex = v_phasor / i_phasor
        
        return z_complex, abs(z_complex), np.degrees(np.angle(z_complex))
    
    def calculate_instantaneous_values(self, vm, im, f, theta_v_rad, theta_i_rad, t_instant):
        """Calcula valores instantâneos"""
        v = vm * np.sin(2 * np.pi * f * t_instant + theta_v_rad)
        i = im * np.sin(2 * np.pi * f * t_instant + theta_i_rad)
        p = v * i
        return v, i, p
    
    def find_time_for_value(self, amplitude, target_value, frequency, phase_rad):
        """Encontra instante onde grandeza atinge valor específico"""
        if abs(target_value) > abs(amplitude):
            return None
        
        if target_value >= 0:
            t = (np.arcsin(target_value / amplitude) - phase_rad) / (2 * np.pi * frequency)
        else:
            t = (np.arcsin(abs(target_value) / amplitude) - phase_rad) / (2 * np.pi * frequency) + 1 / (2 * frequency)
        
        while t < 0:
            t += 1 / frequency
        return t
    
    def calculate_power_correction(self, vrms, irms, theta_v_deg, theta_i_deg, f, desired_fp):
        """Calcula correção do fator de potência"""
        powers = self.calculate_powers(vrms, irms, theta_v_deg, theta_i_deg)
        
        try:
            q_after = powers['active'] * np.tan(np.arccos(desired_fp))
            q_capacitor = powers['reactive'] - q_after
            
            if abs(q_capacitor) < self.tolerance:
                return None
            
            capacitance = abs(q_capacitor / (vrms**2 * 2 * np.pi * f)) * 1e6  # µF
            i_capacitor = abs(q_capacitor / vrms) if vrms > 0 else 0
            i_total_rms = np.sqrt(irms**2 + i_capacitor**2)
            new_fp = powers['active'] / (vrms * i_total_rms) if i_total_rms > 0 else 0
            
            reduction_percent = ((irms - i_total_rms) / irms) * 100 if irms > 0 else 0
            
            return {
                'capacitance_uF': capacitance,
                'q_capacitor': q_capacitor,
                'i_capacitor': i_capacitor,
                'new_power_factor': new_fp,
                'new_current_total': i_total_rms,
                'current_reduction_percent': reduction_percent,
                'power_savings': reduction_percent * 0.8  # Estimativa
            }
        except:
            return None
    
    def generate_waveforms(self, f, vm, im, theta_v_rad, theta_i_rad, periods):
        """Gera formas de onda otimizadas"""
        t_total = periods / f
        points = min(4000, int(periods * f * 100))  # Otimização dinâmica
        t = np.linspace(-t_total, t_total, points)
        
        v = vm * np.sin(2 * np.pi * f * t + theta_v_rad)
        i = im * np.sin(2 * np.pi * f * t + theta_i_rad)
        p = v * i
        
        return t, v, i, p

class PresetManager:
    """Gerenciador de presets de circuitos"""
    
    PRESETS = {
        "🏠 Residencial 220V": {
            "frequency": 60, "voltage_max": 311.13, "current_max": 14.14,
            "voltage_angle": 0, "current_angle": 0,
            "description": "Circuito residencial brasileiro padrão"
        },
        "🏭 Industrial 380V": {
            "frequency": 60, "voltage_max": 537.4, "current_max": 70.7,
            "voltage_angle": 0, "current_angle": -30,
            "description": "Circuito industrial com carga indutiva"
        },
        "⚙️ Motor Indutivo": {
            "frequency": 60, "voltage_max": 311.13, "current_max": 28.28,
            "voltage_angle": 0, "current_angle": -25,
            "description": "Motor de indução monofásico típico"
        },
        "🔋 Banco Capacitivo": {
            "frequency": 60, "voltage_max": 311.13, "current_max": 7.07,
            "voltage_angle": 0, "current_angle": 90,
            "description": "Banco de capacitores para correção FP"
        },
        "💡 Lâmpada LED": {
            "frequency": 60, "voltage_max": 311.13, "current_max": 1.41,
            "voltage_angle": 0, "current_angle": -15,
            "description": "Carga LED com pequeno componente indutivo"
        }
    }

def create_advanced_charts(analyzer, t, v, i, p, vm, im, vrms, irms, theta_v_deg, theta_i_deg, powers):
    """Cria gráficos avançados e interativos"""
    
    # Gráfico principal de formas de onda
    fig_waves = make_subplots(
        rows=2, cols=1,
        subplot_titles=("📈 Tensão e Corrente vs Tempo", "⚡ Potência vs Tempo"),
        vertical_spacing=0.12,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    # Tensão
    fig_waves.add_trace(
        go.Scatter(
            x=t*1000, y=v,
            name="v(t)",
            line=dict(color='#e74c3c', width=3),
            hovertemplate="<b>Tensão</b><br>Tempo: %{x:.2f} ms<br>Valor: %{y:.2f} V<extra></extra>"
        ),
        row=1, col=1
    )
    
    # Corrente (ajustar escala se necessário)
    scale_factor = 10 if vm/im > 11.454 else 1
    i_scaled = i * scale_factor
    i_name = f"i(t) × {scale_factor}" if scale_factor > 1 else "i(t)"
    
    fig_waves.add_trace(
        go.Scatter(
            x=t*1000, y=i_scaled,
            name=i_name,
            line=dict(color='#3498db', width=3),
            hovertemplate=f"<b>Corrente</b><br>Tempo: %{{x:.2f}} ms<br>Valor: %{{y:.2f}} A<extra></extra>"
        ),
        row=1, col=1
    )
    
    # Potência
    p_scaled = p / 1000 if max(abs(p)) >= 1000 else p
    p_unit = "kW" if max(abs(p)) >= 1000 else "W"
    
    fig_waves.add_trace(
        go.Scatter(
            x=t*1000, y=p_scaled,
            name=f"p(t)",
            line=dict(color='#9b59b6', width=3),
            fill='tonexty',
            fillcolor='rgba(155, 89, 182, 0.1)',
            hovertemplate=f"<b>Potência</b><br>Tempo: %{{x:.2f}} ms<br>Valor: %{{y:.2f}} {p_unit}<extra></extra>"
        ),
        row=2, col=1
    )
    
    # Potência média
    p_avg = powers['active'] / 1000 if max(abs(p)) >= 1000 else powers['active']
    fig_waves.add_hline(
        y=p_avg,
        line=dict(color='#2c3e50', width=2, dash='dash'),
        annotation_text=f"P média = {p_avg:.2f} {p_unit}",
        row=2, col=1
    )
    
    fig_waves.update_layout(
        height=700,
        title="📊 Análise Temporal dos Sinais Elétricos",
        showlegend=True,
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig_waves.update_xaxes(title_text="Tempo (ms)", showgrid=True)
    fig_waves.update_yaxes(title_text="Tensão (V) / Corrente (A)", row=1)
    fig_waves.update_yaxes(title_text=f"Potência ({p_unit})", row=2)
    
    return fig_waves

def main():
    # Header principal
    st.markdown('<h1 class="main-header">⚡ Analisador Avançado de Circuitos Elétricos</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #6c757d; margin-bottom: 2rem;">🎓 Contribuição PET AutoNet/IFMT - Versão Aprimorada com Funcionalidades Avançadas</p>', unsafe_allow_html=True)
    
    analyzer = AdvancedCircuitAnalyzer()
    
    # Sidebar melhorada
    with st.sidebar:
        st.markdown("# ⚙️ Painel de Controle")
        
        # Seção de Presets
        st.markdown("## 🎯 Presets Rápidos")
        preset_names = list(PresetManager.PRESETS.keys())
        
        cols = st.columns(2)
        for i, preset_name in enumerate(preset_names):
            with cols[i % 2]:
                if st.button(preset_name.split(' ', 1)[0], key=f"preset_{i}", help=PresetManager.PRESETS[preset_name]['description']):
                    preset = PresetManager.PRESETS[preset_name]
                    st.session_state.update({
                        'freq_preset': preset['frequency'],
                        'vm_preset': preset['voltage_max'],
                        'im_preset': preset['current_max'],
                        'theta_v_preset': preset['voltage_angle'],
                        'theta_i_preset': preset['current_angle']
                    })
        
        st.markdown("---")
        
        # Parâmetros básicos
        st.markdown("## 🔧 Parâmetros do Circuito")
        f = st.number_input(
            "📊 Frequência (Hz)",
            min_value=1, max_value=1000,
            value=st.session_state.get('freq_preset', 60),
            step=1,
            help="Frequência da rede elétrica"
        )
        
        vm = st.number_input(
            "⚡ Tensão Máxima (V)",
            min_value=0.1, max_value=2000.0,
            value=st.session_state.get('vm_preset', 311.0),
            step=0.1,
            help="Valor de pico da tensão"
        )
        
        im = st.number_input(
            "🔌 Corrente Máxima (A)",
            min_value=0.01, max_value=500.0,
            value=st.session_state.get('im_preset', 14.14),
            step=0.01,
            help="Valor de pico da corrente"
        )
        
        nr_periods = st.slider(
            "🔄 Número de Ciclos",
            min_value=1, max_value=10,
            value=2,
            help="Quantidade de períodos para visualização"
        )
        
        st.markdown("---")
        
        # Ângulos de fase
        st.markdown("## 📐 Ângulos de Fase")
        theta_v_deg = st.slider(
            "📈 Ângulo da Tensão (°)",
            min_value=-180, max_value=180,
            value=st.session_state.get('theta_v_preset', 0),
            help="Ângulo de fase da tensão"
        )
        
        theta_i_deg = st.slider(
            "📉 Ângulo da Corrente (°)",
            min_value=-180, max_value=180,
            value=st.session_state.get('theta_i_preset', -30),
            help="Ângulo de fase da corrente"
        )
        
        st.markdown("---")
        
        # Análise instantânea
        st.markdown("## ⏱️ Análise Instantânea")
        t_instant_ms = st.number_input(
            "🕐 Instante (ms)",
            min_value=0.0, max_value=500.0,
            value=5.0, step=0.1,
            help="Instante específico para análise"
        )
        
        # Valores específicos para análise
        with st.expander("🎯 Encontrar Instantes"):
            vk = st.number_input(f"Tensão desejada (±{vm:.1f}V)", value=vm*0.5, min_value=-vm, max_value=vm)
            ik = st.number_input(f"Corrente desejada (±{im:.1f}A)", value=im*0.5, min_value=-im, max_value=im)
        
        st.markdown("---")
        
        # Correção do fator de potência
        st.markdown("## ⚙️ Correção do Fator de Potência")
        correct_pf = st.checkbox("🔧 Ativar Correção", help="Habilita cálculo de correção do fator de potência")
        desired_pf = None
        if correct_pf:
            desired_pf = st.slider(
                "🎯 FP Desejado",
                min_value=0.0, max_value=1.0,
                value=0.95, step=0.01,
                help="Fator de potência objetivo após correção"
            )
    
    # Validação de entradas
    errors = analyzer.validate_inputs(f, vm, im)
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return
    
    # Cálculos principais
    vrms, irms = analyzer.calculate_rms_values(vm, im)
    theta_v_rad = np.radians(theta_v_deg)
    theta_i_rad = np.radians(theta_i_deg)
    t_instant = t_instant_ms / 1000
    
    powers = analyzer.calculate_powers(vrms, irms, theta_v_deg, theta_i_deg)
    circuit_type, phase_diff, type_color = analyzer.determine_circuit_type(theta_v_deg, theta_i_deg)
    z_complex, z_magnitude, z_angle = analyzer.calculate_impedance(vrms, irms, theta_v_rad, theta_i_rad)
    
    v_instant, i_instant, p_instant = analyzer.calculate_instantaneous_values(
        vm, im, f, theta_v_rad, theta_i_rad, t_instant
    )
    
    # Encontrar instantes específicos
    t_vk = analyzer.find_time_for_value(vm, vk, f, theta_v_rad)
    t_ik = analyzer.find_time_for_value(im, ik, f, theta_i_rad)
    
    # Gerar formas de onda
    t, v, i, p = analyzer.generate_waveforms(f, vm, im, theta_v_rad, theta_i_rad, nr_periods)
    
    # Layout principal com abas melhoradas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Análise Principal",
        "📊 Resultados Detalhados", 
        "⚡ Correção do FP",
        "🎯 Análise Avançada",
        "📋 Relatório Completo"
    ])
    
    with tab1:
        # Métricas principais em cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""<div class="metric-card">
                <h4>📊 Frequência</h4>
                <h2 style="color: #1f77b4;">{f} Hz</h2>
                <p>ω = {2*np.pi*f:.2f} rad/s</p>
                </div>""", unsafe_allow_html=True
            )
            
        with col2:
            st.markdown(
                f"""<div class="metric-card">
                <h4>⚡ Tensão RMS</h4>
                <h2 style="color: #e74c3c;">{vrms:.2f} V</h2>
                <p>Vm/√2 = {vm:.1f}/1.414</p>
                </div>""", unsafe_allow_html=True
            )
            
        with col3:
            st.markdown(
                f"""<div class="metric-card">
                <h4>🔌 Corrente RMS</h4>
                <h2 style="color: #3498db;">{irms:.2f} A</h2>
                <p>Im/√2 = {im:.1f}/1.414</p>
                </div>""", unsafe_allow_html=True
            )
            
        with col4:
            st.markdown(
                f"""<div class="metric-card">
                <h4>🎯 Fator de Potência</h4>
                <h2 style="color: {type_color};">{powers['power_factor']:.3f}</h2>
                <p>{circuit_type.split(' ', 1)[1] if ' ' in circuit_type else circuit_type}</p>
                </div>""", unsafe_allow_html=True
            )
        
        # Análise de potência
        st.markdown('<div class="sub-header">⚡ Análise de Potências</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Potência Ativa", f"{powers['active']:.2f} W", help="Potência efetivamente consumida")
        with col2:
            st.metric("Potência Reativa", f"{powers['reactive_abs']:.2f} VAr", help="Potência não produtiva")
        with col3:
            st.metric("Potência Aparente", f"{powers['apparent']:.2f} VA", help="Potência total do sistema")
        
        # Gráfico principal
        st.markdown('<div class="sub-header">📈 Formas de Onda Interativas</div>', unsafe_allow_html=True)
        fig_waves = create_advanced_charts(analyzer, t, v, i, p, vm, im, vrms, irms, theta_v_deg, theta_i_deg, powers)
        st.plotly_chart(fig_waves, use_container_width=True)
        
        # Análise instantânea
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(f"**📊 Valores no instante t = {t_instant_ms:.2f} ms:**")
            st.write(f"• Tensão: **{v_instant:.2f} V**")
            st.write(f"• Corrente: **{i_instant:.2f} A**") 
            st.write(f"• Potência: **{p_instant:.2f} W**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(f"**🎯 Instantes específicos:**")
            if t_vk is not None:
                st.write(f"• V = {vk:.1f}V em t = **{t_vk*1000:.2f} ms**")
            if t_ik is not None:
                st.write(f"• I = {ik:.1f}A em t = **{t_ik*1000:.2f} ms**")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="sub-header">🔍 Resultados Detalhados</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Fasores
            st.markdown("### 📐 Análise Fasorial")
            fasors_data = {
                "Grandeza": ["Tensão", "Corrente"],
                "Módulo": [f"{vrms:.3f} V", f"{irms:.3f} A"],
                "Ângulo": [f"{theta_v_deg:.1f}°", f"{theta_i_deg:.1f}°"],
                "Forma Polar": [f"{vrms:.3f}∠{theta_v_deg:.1f}°", f"{irms:.3f}∠{theta_i_deg:.1f}°"]
            }
            st.dataframe(pd.DataFrame(fasors_data), use_container_width=True)
            
            # Impedância
            st.markdown("### ⚡ Impedância Equivalente")
            st.metric("Módulo |Z|", f"{z_magnitude:.3f} Ω")
            st.metric("Ângulo ∠Z", f"{z_angle:.2f}°")
            st.write(f"**Forma Retangular:** {z_complex.real:.3f} + {z_complex.imag:.3f}j Ω")
        
        with col2:
            # Triângulo de potências
            st.markdown("### 🔺 Triângulo de Potências")
            
            fig_triangle = go.Figure()
            
            # Triângulo
            fig_triangle.add_trace(go.Scatter(
                x=[0, powers['active'], powers['active'], 0],
                y=[0, 0, powers['reactive'], 0],
                mode='lines+markers',
                fill='toself',
                fillcolor='rgba(31, 119, 180, 0.1)',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8, color='#e74c3c'),
                name='Triângulo de Potência',
                hovertemplate="<extra></extra>"
            ))
            
            # Hipotenusa
            fig_triangle.add_trace(go.Scatter(
                x=[0, powers['active']],
                y=[0, powers['reactive']],
                mode='lines',
                line=dict(color='#e74c3c', width=3, dash='dash'),
                name='Potência Aparente',
                hovertemplate="<extra></extra>"
            ))
            
            # Anotações
            fig_triangle.add_annotation(
                x=powers['active']/2, y=-powers['apparent']*0.1,
                text=f"P = {powers['active']:.1f} W",
                showarrow=False, font=dict(size=14, color='#2c3e50')
            )
            fig_triangle.add_annotation(
                x=powers['active']+powers['apparent']*0.05, y=powers['reactive']/2,
                text=f"Q = {powers['reactive_abs']:.1f} VAr",
                showarrow=False, font=dict(size=14, color='#2c3e50')
            )
            fig_triangle.add_annotation(
                x=powers['active']/2, y=powers['reactive']/2+powers['apparent']*0.05,
                text=f"S = {powers['apparent']:.1f} VA",
                showarrow=False, font=dict(size=14, color='#2c3e50')
            )
            
            fig_triangle.update_layout(
                title="Triângulo de Potências",
                xaxis_title="Potência Ativa (W)",
                yaxis_title="Potência Reativa (VAr)",
                height=400,
                showlegend=False,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_triangle, use_container_width=True)
    
    with tab3:
        if correct_pf and desired_pf is not None:
            st.markdown('<div class="sub-header">⚙️ Correção do Fator de Potência</div>', unsafe_allow_html=True)
            
            correction = analyzer.calculate_power_correction(
                vrms, irms, theta_v_deg, theta_i_deg, f, desired_pf
            )
            
            if correction:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"✅ **Correção Calculada com Sucesso!**")
                    
                    # Métricas de correção
                    st.metric("🔋 Capacitância", f"{correction['capacitance_uF']:.2f} µF")
                    st.metric("⚡ Corrente do Capacitor", f"{correction['i_capacitor']:.3f} A")
                    st.metric("🎯 Novo Fator de Potência", f"{correction['new_power_factor']:.3f}")
                    st.metric("📉 Redução de Corrente", f"{correction['current_reduction_percent']:.1f}%")
                    st.metric("💰 Economia de Energia", f"{correction['power_savings']:.1f}%")
                
                with col2:
                    # Gráfico comparativo
                    fig_comparison = go.Figure()
                    
                    categories = ['Fator de Potência', 'Corrente Total']
                    original = [powers['power_factor'], irms]
                    corrected = [correction['new_power_factor'], correction['new_current_total']]
                    
                    fig_comparison.add_trace(go.Bar(
                        x=categories, y=original,
                        name='Original',
                        marker_color='#e74c3c',
                        text=[f'{val:.3f}' for val in original],
                        textposition='auto'
                    ))
                    
                    fig_comparison.add_trace(go.Bar(
                        x=categories, y=corrected,
                        name='Corrigido',
                        marker_color='#27ae60',
                        text=[f'{val:.3f}' for val in corrected],
                        textposition='auto'
                    ))
                    
                    fig_comparison.update_layout(
                        title="📊 Comparação: Antes vs Depois",
                        yaxis_title="Valores",
                        height=400,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Recomendações
                st.markdown("### 💡 Recomendações Técnicas")
                st.info(f"""
                **🔧 Implementação:**
                • Instale um capacitor de {correction['capacitance_uF']:.2f} µF
                • Corrente nominal do capacitor: {correction['i_capacitor']:.2f} A
                • Tensão nominal: {vrms:.0f} V (capacitor deve suportar pelo menos {vrms*1.2:.0f} V)
                
                **📈 Benefícios:**
                • Redução de {correction['current_reduction_percent']:.1f}% na corrente total
                • Melhoria do fator de potência de {powers['power_factor']:.3f} para {correction['new_power_factor']:.3f}
                • Economia estimada de energia: {correction['power_savings']:.1f}%
                """)
            else:
                st.warning("⚠️ Não foi possível calcular a correção com os parâmetros fornecidos.")
        else:
            st.info("ℹ️ **Ative a correção do fator de potência na barra lateral** para ver os cálculos detalhados.")
            
            # Informações educativas
            st.markdown("### 📚 Sobre Correção do Fator de Potência")
            st.markdown("""
            A correção do fator de potência é importante porque:
            
            **✅ Vantagens:**
            • Reduz perdas na transmissão de energia
            • Diminui a corrente total do sistema
            • Evita penalidades da concessionária
            • Melhora a eficiência energética
            • Reduz o aquecimento de condutores
            
            **🎯 Quando corrigir:**
            • Fator de potência < 0.92 (residencial)
            • Fator de potência < 0.95 (industrial)
            • Cargas indutivas significativas
            """)
    
    with tab4:
        st.markdown('<div class="sub-header">🎯 Análise Avançada</div>', unsafe_allow_html=True)
        
        # Análise harmônica (simulada)
        st.markdown("### 🌊 Análise Espectral")
        col1, col2 = st.columns(2)
        
        with col1:
            # Simulação de harmônicos
            harmonics = np.array([1, 3, 5, 7, 9, 11])
            amplitudes = np.array([1.0, 0.1, 0.05, 0.02, 0.01, 0.005]) * vm
            
            fig_harmonics = go.Figure()
            fig_harmonics.add_trace(go.Bar(
                x=harmonics * f,
                y=amplitudes,
                name='Harmônicos de Tensão',
                marker_color='#9b59b6'
            ))
            
            fig_harmonics.update_layout(
                title="Espectro de Frequências (Simulado)",
                xaxis_title="Frequência (Hz)",
                yaxis_title="Amplitude (V)",
                height=400
            )
            st.plotly_chart(fig_harmonics, use_container_width=True)
        
        with col2:
            # Eficiência energética
            efficiency = powers['active'] / powers['apparent'] * 100
            
            st.markdown("### ⚡ Eficiência Energética")
            st.metric("Eficiência", f"{efficiency:.1f}%")
            
            # Gauge de eficiência
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = efficiency,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Eficiência (%)"},
                delta = {'reference': 95},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Análise de qualidade de energia
        st.markdown("### 📊 Indicadores de Qualidade")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            distortion = (1 - powers['power_factor']) * 100
            st.metric("Distorção Estimada", f"{distortion:.1f}%", 
                     delta=f"{distortion-5:.1f}%" if distortion > 5 else None,
                     delta_color="inverse")
        
        with col2:
            load_factor = (powers['active'] / (vm * im / 2)) * 100
            st.metric("Fator de Carga", f"{load_factor:.1f}%")
            
        with col3:
            power_quality = powers['power_factor'] * efficiency / 100
            st.metric("Índice de Qualidade", f"{power_quality:.3f}")
            
        with col4:
            current_distortion = abs(theta_v_deg - theta_i_deg)
            st.metric("Defasamento", f"{current_distortion:.1f}°")
    
    with tab5:
        st.markdown('<div class="sub-header">📋 Relatório Técnico Completo</div>', unsafe_allow_html=True)
        
        # Informações do relatório
        report_time = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📅 Gerado em:** {report_time}")
            st.markdown(f"**👤 Usuário:** Sistema PET AutoNet/IFMT")
        
        # Relatório detalhado
        st.markdown("### 📊 Parâmetros de Entrada")
        params_df = pd.DataFrame({
            'Parâmetro': [
                'Frequência', 'Tensão Máxima', 'Corrente Máxima',
                'Ângulo Tensão', 'Ângulo Corrente', 'Número de Períodos'
            ],
            'Valor': [
                f"{f} Hz", f"{vm:.2f} V", f"{im:.2f} A",
                f"{theta_v_deg:.1f}°", f"{theta_i_deg:.1f}°", f"{nr_periods}"
            ]
        })
        st.dataframe(params_df, use_container_width=True)
        
        st.markdown("### ⚡ Resultados dos Cálculos")
        results_df = pd.DataFrame({
            'Grandeza': [
                'Tensão RMS', 'Corrente RMS', 'Fator de Potência',
                'Potência Ativa', 'Potência Reativa', 'Potência Aparente',
                'Impedância', 'Defasamento', 'Tipo de Circuito'
            ],
            'Valor': [
                f"{vrms:.3f} V", f"{irms:.3f} A", f"{powers['power_factor']:.3f}",
                f"{powers['active']:.2f} W", f"{powers['reactive']:.2f} VAr", f"{powers['apparent']:.2f} VA",
                f"{z_magnitude:.2f} Ω ∠ {z_angle:.1f}°", f"{phase_diff:.2f}°", circuit_type
            ]
        })
        st.dataframe(results_df, use_container_width=True)
        
        # Análise instantânea
        st.markdown(f"### 🕐 Análise no Instante t = {t_instant_ms:.2f} ms")
        instant_df = pd.DataFrame({
            'Grandeza': ['Tensão Instantânea', 'Corrente Instantânea', 'Potência Instantânea'],
            'Valor': [f"{v_instant:.3f} V", f"{i_instant:.3f} A", f"{p_instant:.3f} W"]
        })
        st.dataframe(instant_df, use_container_width=True)
        
        # Exportação de dados
        st.markdown("### 📥 Exportar Dados")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Baixar Parâmetros (CSV)"):
                csv = params_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="parametros_circuito.csv">📥 Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            if st.button("📈 Baixar Resultados (CSV)"):
                csv = results_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="resultados_circuito.csv">📥 Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col3:
            if st.button("🌊 Baixar Formas de Onda (CSV)"):
                waves_df = pd.DataFrame({
                    'Tempo_ms': t * 1000,
                    'Tensao_V': v,
                    'Corrente_A': i,
                    'Potencia_W': p
                })
                csv = waves_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="formas_onda.csv">📥 Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        # Salvamento no histórico
        if st.button("💾 Salvar no Histórico"):
            calculation_data = {
                'timestamp': report_time,
                'parameters': {
                    'frequency': f, 'vm': vm, 'im': im,
                    'theta_v': theta_v_deg, 'theta_i': theta_i_deg
                },
                'results': {
                    'vrms': vrms, 'irms': irms, 'power_factor': powers['power_factor'],
                    'p_active': powers['active'], 'circuit_type': circuit_type
                }
            }
            st.session_state.calculation_history.append(calculation_data)
            st.success("✅ Cálculo salvo no histórico!")
        
        # Exibir histórico
        if st.session_state.calculation_history:
            st.markdown("### 📚 Histórico de Cálculos")
            history_df = pd.DataFrame([
                {
                    'Data/Hora': calc['timestamp'],
                    'Freq (Hz)': calc['parameters']['frequency'],
                    'Vm (V)': calc['parameters']['vm'],
                    'FP': f"{calc['results']['power_factor']:.3f}",
                    'Tipo': calc['results']['circuit_type'].split(' ')[1] if ' ' in calc['results']['circuit_type'] else 'N/A'
                }
                for calc in st.session_state.calculation_history[-5:]  # Últimos 5
            ])
            st.dataframe(history_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #6c757d;">🎓 <b>Contribuição PET AutoNet/IFMT</b> | '
        'Desenvolvido para fins educacionais | Versão Avançada 2025</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
