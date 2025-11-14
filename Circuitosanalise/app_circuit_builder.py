import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json

# Importar o editor de circuitos
from circuit_editor import CircuitBuilder, ComponentType, CircuitTemplates

# Configuração da página
st.set_page_config(
    page_title="🔧 Construtor de Circuitos Interativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .component-button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        border: none;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        cursor: pointer;
        margin: 0.2rem;
        transition: all 0.3s ease;
        font-size: 1rem;
        font-weight: bold;
    }
    .component-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .circuit-info {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .template-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .template-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.2);
        transform: translateY(-2px);
    }
    .toolbar {
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'circuit_builder' not in st.session_state:
    st.session_state.circuit_builder = CircuitBuilder()
if 'selected_component_type' not in st.session_state:
    st.session_state.selected_component_type = None
if 'editing_mode' not in st.session_state:
    st.session_state.editing_mode = 'add'  # 'add', 'move', 'connect', 'delete'
if 'selected_component_id' not in st.session_state:
    st.session_state.selected_component_id = None
if 'click_position' not in st.session_state:
    st.session_state.click_position = None

def main():
    st.markdown('<h1 class="main-header">🔧 Construtor Interativo de Circuitos Elétricos</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #6c757d; margin-bottom: 2rem;">🎨 Monte seu circuito arrastando componentes e conectando-os visualmente</p>', unsafe_allow_html=True)
    
    builder = st.session_state.circuit_builder
    
    # Sidebar com ferramentas
    with st.sidebar:
        st.markdown("# 🛠️ Caixa de Ferramentas")
        
        # Modo de edição
        st.markdown("## 🎯 Modo de Edição")
        editing_mode = st.radio(
            "Selecione o modo:",
            ['add', 'move', 'connect', 'delete'],
            format_func=lambda x: {
                'add': '➕ Adicionar Componentes',
                'move': '↔️ Mover Componentes', 
                'connect': '🔗 Conectar Componentes',
                'delete': '🗑️ Remover Componentes'
            }[x],
            key="editing_mode_radio"
        )
        st.session_state.editing_mode = editing_mode
        
        st.markdown("---")
        
        # Biblioteca de componentes
        if editing_mode == 'add':
            st.markdown("## 🧩 Componentes Disponíveis")
            
            components_info = {
                ComponentType.VOLTAGE_SOURCE: ("⊕", "Fonte de Tensão", "#27ae60"),
                ComponentType.CURRENT_SOURCE: ("⊗", "Fonte de Corrente", "#9b59b6"),
                ComponentType.RESISTOR: ("⬛", "Resistor", "#e74c3c"),
                ComponentType.CAPACITOR: ("⚏", "Capacitor", "#3498db"),
                ComponentType.INDUCTOR: ("⨂", "Indutor", "#f39c12"),
                ComponentType.GROUND: ("⏚", "Terra", "#34495e"),
                ComponentType.SWITCH: ("⧄", "Chave", "#e67e22")
            }
            
            for comp_type, (symbol, name, color) in components_info.items():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f'<span style="font-size: 2rem; color: {color};">{symbol}</span>', unsafe_allow_html=True)
                with col2:
                    if st.button(name, key=f"btn_{comp_type.value}"):
                        st.session_state.selected_component_type = comp_type
                        st.success(f"✅ {name} selecionado!")
            
            # Parâmetros do componente selecionado
            if st.session_state.selected_component_type:
                st.markdown(f"### ⚙️ Configurar {st.session_state.selected_component_type.value.title()}")
                
                component_value = st.number_input("Valor:", min_value=0.0, value=100.0, step=1.0)
                
                unit_options = {
                    ComponentType.RESISTOR: ["Ω", "kΩ", "MΩ"],
                    ComponentType.CAPACITOR: ["µF", "nF", "pF"],
                    ComponentType.INDUCTOR: ["mH", "µH", "H"],
                    ComponentType.VOLTAGE_SOURCE: ["V"],
                    ComponentType.CURRENT_SOURCE: ["A", "mA"]
                }
                
                if st.session_state.selected_component_type in unit_options:
                    component_unit = st.selectbox(
                        "Unidade:",
                        unit_options[st.session_state.selected_component_type]
                    )
                else:
                    component_unit = ""
        
        st.markdown("---")
        
        # Templates pré-definidos
        st.markdown("## 📋 Templates Rápidos")
        
        templates = {
            "RC": CircuitTemplates.get_rc_circuit(),
            "RL": CircuitTemplates.get_rl_circuit(),
            "RLC": CircuitTemplates.get_rlc_circuit()
        }
        
        for template_key, template_data in templates.items():
            if st.button(f"{template_data['name']}", key=f"template_{template_key}"):
                builder.import_circuit(template_data)
                st.success(f"✅ Template {template_data['name']} carregado!")
                st.rerun()
        
        st.markdown("---")
        
        # Informações do circuito
        st.markdown("## 📊 Info do Circuito")
        circuit_params = builder.calculate_circuit_parameters()
        
        st.metric("Componentes", circuit_params['num_components'])
        if circuit_params['total_resistance'] > 0:
            st.metric("Resistência Total", f"{circuit_params['total_resistance']:.1f} Ω")
        if circuit_params['voltage_sources']:
            st.metric("Fontes de Tensão", len(circuit_params['voltage_sources']))
        
        st.markdown("---")
        
        # Controles do circuito
        st.markdown("## 🎮 Controles")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Limpar Tudo"):
                st.session_state.circuit_builder = CircuitBuilder()
                st.success("Circuito limpo!")
                st.rerun()
        
        with col2:
            if st.button("💾 Salvar"):
                circuit_data = builder.export_circuit()
                st.download_button(
                    "📥 Download",
                    data=json.dumps(circuit_data, indent=2),
                    file_name="meu_circuito.json",
                    mime="application/json"
                )
        
        # Upload de circuito
        uploaded_file = st.file_uploader(
            "📁 Carregar Circuito",
            type=['json'],
            help="Carregue um circuito salvo anteriormente"
        )
        
        if uploaded_file:
            try:
                circuit_data = json.loads(uploaded_file.getvalue().decode("utf-8"))
                builder.import_circuit(circuit_data)
                st.success("✅ Circuito carregado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao carregar: {e}")
    
    # Área principal de trabalho
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("## 🎨 Área de Desenho")
        
        # Toolbar
        st.markdown('<div class="toolbar">', unsafe_allow_html=True)
        toolbar_col1, toolbar_col2, toolbar_col3, toolbar_col4 = st.columns(4)
        
        with toolbar_col1:
            st.markdown(f"**Modo:** {editing_mode.title()}")
        with toolbar_col2:
            if st.session_state.selected_component_type:
                st.markdown(f"**Componente:** {st.session_state.selected_component_type.value.title()}")
        with toolbar_col3:
            if st.button("🔄 Atualizar", key="refresh_circuit"):
                st.rerun()
        with toolbar_col4:
            grid_enabled = st.checkbox("📐 Grade", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Desenho do circuito
        circuit_fig = builder.create_circuit_diagram()
        
        # Instruções baseadas no modo
        if editing_mode == 'add':
            if st.session_state.selected_component_type:
                st.info(f"🎯 **Clique na área de desenho** para adicionar um {st.session_state.selected_component_type.value}")
            else:
                st.info("📌 **Selecione um componente** na barra lateral para adicionar ao circuito")
        elif editing_mode == 'move':
            st.info("↔️ **Clique e arraste** componentes para reposicioná-los")
        elif editing_mode == 'connect':
            st.info("🔗 **Clique em dois componentes** para conectá-los")
        elif editing_mode == 'delete':
            st.info("🗑️ **Clique em um componente** para removê-lo")
        
        # Exibir o diagrama
        clicked_data = st.plotly_chart(
            circuit_fig, 
            use_container_width=True, 
            key="circuit_diagram"
        )
        
        # Processar cliques no diagrama
        if clicked_data and hasattr(clicked_data, 'selection'):
            # Esta funcionalidade precisa de implementação adicional
            # para capturar eventos de clique no Plotly
            pass
        
        # Simulador de cliques para demonstração
        st.markdown("### 🖱️ Simulador de Cliques")
        click_col1, click_col2 = st.columns(2)
        
        with click_col1:
            click_x = st.number_input("Posição X:", min_value=0, max_value=800, value=400, step=20)
        with click_col2:
            click_y = st.number_input("Posição Y:", min_value=0, max_value=600, value=300, step=20)
        
        if st.button("🎯 Simular Clique"):
            handle_click_event(builder, click_x, click_y, editing_mode)
    
    with col2:
        st.markdown("## 📊 Análise do Circuito")
        
        if builder.components:
            # Lista de componentes
            st.markdown("### 🧩 Componentes")
            components_df = pd.DataFrame([
                {
                    "ID": comp.id[:8] + "...",
                    "Tipo": comp.type.value.title(),
                    "Valor": f"{comp.value} {comp.unit}" if comp.value else "N/A",
                    "Posição": f"({comp.x}, {comp.y})"
                }
                for comp in builder.components.values()
            ])
            st.dataframe(components_df, use_container_width=True)
            
            # Parâmetros calculados
            st.markdown("### ⚡ Parâmetros")
            params = builder.calculate_circuit_parameters()
            
            if params['total_resistance'] > 0:
                st.metric("Resistência Total", f"{params['total_resistance']:.1f} Ω")
            if params['total_capacitance'] > 0:
                st.metric("Capacitância Total", f"{params['total_capacitance']:.1f} µF")
            if params['total_inductance'] > 0:
                st.metric("Indutância Total", f"{params['total_inductance']:.1f} mH")
            
            # Simulação básica
            if params['voltage_sources'] and params['total_resistance'] > 0:
                st.markdown("### 🔬 Simulação Básica")
                
                voltage = params['voltage_sources'][0] if params['voltage_sources'] else 12
                current = voltage / params['total_resistance']
                power = voltage * current
                
                st.metric("Corrente", f"{current:.3f} A")
                st.metric("Potência", f"{power:.2f} W")
                
                # Gráfico básico da resposta
                t = np.linspace(0, 0.02, 1000)  # 20ms
                frequency = 60  # 60Hz
                
                if params['total_capacitance'] > 0 or params['total_inductance'] > 0:
                    # Resposta transiente (simplificada)
                    if params['total_capacitance'] > 0:
                        # RC Circuit
                        tau = params['total_resistance'] * params['total_capacitance'] * 1e-6
                        v_cap = voltage * (1 - np.exp(-t/tau))
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=t*1000, y=v_cap,
                            name="Tensão no Capacitor",
                            line=dict(color='#3498db', width=2)
                        ))
                        fig.update_layout(
                            title="Resposta Transiente",
                            xaxis_title="Tempo (ms)",
                            yaxis_title="Tensão (V)",
                            height=300
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    # Resposta senoidal para circuito resistivo
                    v_ac = voltage * np.sin(2 * np.pi * frequency * t)
                    i_ac = current * np.sin(2 * np.pi * frequency * t)
                    
                    fig = make_subplots(rows=2, cols=1, 
                                       subplot_titles=("Tensão", "Corrente"))
                    
                    fig.add_trace(go.Scatter(
                        x=t*1000, y=v_ac,
                        name="Tensão",
                        line=dict(color='#e74c3c', width=2)
                    ), row=1, col=1)
                    
                    fig.add_trace(go.Scatter(
                        x=t*1000, y=i_ac,
                        name="Corrente",
                        line=dict(color='#3498db', width=2)
                    ), row=2, col=1)
                    
                    fig.update_layout(
                        title="Formas de Onda AC",
                        height=400
                    )
                    fig.update_xaxes(title_text="Tempo (ms)")
                    fig.update_yaxes(title_text="Tensão (V)", row=1, col=1)
                    fig.update_yaxes(title_text="Corrente (A)", row=2, col=1)
                    
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🎯 **Adicione componentes** para ver a análise do circuito")
            
            # Tutorial visual
            st.markdown("### 🎓 Tutorial Rápido")
            st.markdown("""
            **1.** 📌 Selecione um componente na barra lateral
            
            **2.** 🎯 Clique na área de desenho para posicioná-lo
            
            **3.** 🔗 Use o modo "Conectar" para ligar componentes
            
            **4.** ⚡ Veja a análise automática do seu circuito
            
            **5.** 💾 Salve ou carregue seus projetos
            """)

def handle_click_event(builder: CircuitBuilder, x: float, y: float, mode: str):
    """Processa eventos de clique na área de desenho"""
    
    if mode == 'add' and st.session_state.selected_component_type:
        # Adicionar componente
        try:
            component_value = st.session_state.get('component_value', 100.0)
            component_unit = st.session_state.get('component_unit', '')
            
            component_id = builder.add_component(
                st.session_state.selected_component_type,
                x, y, component_value, component_unit
            )
            st.success(f"✅ Componente adicionado! ID: {component_id[:8]}...")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro ao adicionar componente: {e}")
    
    elif mode == 'delete':
        # Remover componente
        component_id = builder.get_component_at_position(x, y)
        if component_id:
            component_type = builder.components[component_id].type.value
            builder.remove_component(component_id)
            st.success(f"🗑️ {component_type} removido!")
            st.rerun()
        else:
            st.warning("⚠️ Nenhum componente encontrado nesta posição")
    
    elif mode == 'move':
        # Mover componente
        component_id = builder.get_component_at_position(x, y)
        if component_id:
            st.session_state.selected_component_id = component_id
            st.info(f"📌 Componente selecionado. Clique na nova posição.")
        elif st.session_state.selected_component_id:
            builder.move_component(st.session_state.selected_component_id, x, y)
            st.success("✅ Componente movido!")
            st.session_state.selected_component_id = None
            st.rerun()
    
    elif mode == 'connect':
        # Conectar componentes
        component_id = builder.get_component_at_position(x, y)
        if component_id:
            if st.session_state.selected_component_id is None:
                st.session_state.selected_component_id = component_id
                st.info("🔗 Primeiro componente selecionado. Clique no segundo componente.")
            elif st.session_state.selected_component_id != component_id:
                connection_id = builder.connect_components(
                    st.session_state.selected_component_id,
                    component_id
                )
                st.success(f"🔗 Componentes conectados! ID: {connection_id[:8]}...")
                st.session_state.selected_component_id = None
                st.rerun()
            else:
                st.warning("⚠️ Não é possível conectar um componente a ele mesmo")

if __name__ == "__main__":
    main()
