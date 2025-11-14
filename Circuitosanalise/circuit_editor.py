# Módulo para construção interativa de circuitos
# Permite ao usuário desenhar e montar circuitos elétricos

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional
import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum

class ComponentType(Enum):
    """Tipos de componentes disponíveis"""
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    INDUCTOR = "inductor"
    VOLTAGE_SOURCE = "voltage_source"
    CURRENT_SOURCE = "current_source"
    GROUND = "ground"
    WIRE = "wire"
    SWITCH = "switch"

@dataclass
class Component:
    """Classe para representar um componente do circuito"""
    id: str
    type: ComponentType
    x: float
    y: float
    rotation: int = 0  # 0, 90, 180, 270 graus
    value: Optional[float] = None
    unit: Optional[str] = None
    label: Optional[str] = None
    connected_to: List[str] = None
    
    def __post_init__(self):
        if self.connected_to is None:
            self.connected_to = []
        if self.label is None:
            self.label = f"{self.type.value}_{self.id[:8]}"

@dataclass
class CircuitConnection:
    """Representa uma conexão entre componentes"""
    id: str
    from_component: str
    to_component: str
    from_terminal: str  # "terminal1" ou "terminal2"
    to_terminal: str

class CircuitBuilder:
    """Construtor interativo de circuitos"""
    
    COMPONENT_SYMBOLS = {
        ComponentType.RESISTOR: "⬛",
        ComponentType.CAPACITOR: "⚏",
        ComponentType.INDUCTOR: "⨂",
        ComponentType.VOLTAGE_SOURCE: "⊕",
        ComponentType.CURRENT_SOURCE: "⊗",
        ComponentType.GROUND: "⏚",
        ComponentType.WIRE: "─",
        ComponentType.SWITCH: "⧄"
    }
    
    COMPONENT_COLORS = {
        ComponentType.RESISTOR: "#e74c3c",
        ComponentType.CAPACITOR: "#3498db", 
        ComponentType.INDUCTOR: "#f39c12",
        ComponentType.VOLTAGE_SOURCE: "#27ae60",
        ComponentType.CURRENT_SOURCE: "#9b59b6",
        ComponentType.GROUND: "#34495e",
        ComponentType.WIRE: "#95a5a6",
        ComponentType.SWITCH: "#e67e22"
    }
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self.connections: Dict[str, CircuitConnection] = {}
        self.grid_size = 20
        self.canvas_width = 800
        self.canvas_height = 600
    
    def add_component(self, component_type: ComponentType, x: float, y: float, 
                     value: float = None, unit: str = None) -> str:
        """Adiciona um componente ao circuito"""
        component_id = str(uuid.uuid4())
        
        # Snap to grid
        x = round(x / self.grid_size) * self.grid_size
        y = round(y / self.grid_size) * self.grid_size
        
        component = Component(
            id=component_id,
            type=component_type,
            x=x,
            y=y,
            value=value,
            unit=unit
        )
        
        self.components[component_id] = component
        return component_id
    
    def move_component(self, component_id: str, x: float, y: float):
        """Move um componente para nova posição"""
        if component_id in self.components:
            # Snap to grid
            x = round(x / self.grid_size) * self.grid_size
            y = round(y / self.grid_size) * self.grid_size
            
            self.components[component_id].x = x
            self.components[component_id].y = y
    
    def remove_component(self, component_id: str):
        """Remove um componente do circuito"""
        if component_id in self.components:
            # Remover todas as conexões relacionadas
            connections_to_remove = []
            for conn_id, connection in self.connections.items():
                if (connection.from_component == component_id or 
                    connection.to_component == component_id):
                    connections_to_remove.append(conn_id)
            
            for conn_id in connections_to_remove:
                del self.connections[conn_id]
            
            del self.components[component_id]
    
    def connect_components(self, from_comp: str, to_comp: str, 
                          from_terminal: str = "terminal1", 
                          to_terminal: str = "terminal1") -> str:
        """Conecta dois componentes"""
        connection_id = str(uuid.uuid4())
        
        connection = CircuitConnection(
            id=connection_id,
            from_component=from_comp,
            to_component=to_comp,
            from_terminal=from_terminal,
            to_terminal=to_terminal
        )
        
        self.connections[connection_id] = connection
        
        # Atualizar listas de conexões dos componentes
        if from_comp in self.components:
            self.components[from_comp].connected_to.append(to_comp)
        if to_comp in self.components:
            self.components[to_comp].connected_to.append(from_comp)
        
        return connection_id
    
    def get_component_at_position(self, x: float, y: float, tolerance: float = 15) -> Optional[str]:
        """Encontra componente na posição especificada"""
        for comp_id, component in self.components.items():
            distance = np.sqrt((component.x - x)**2 + (component.y - y)**2)
            if distance <= tolerance:
                return comp_id
        return None
    
    def create_circuit_diagram(self) -> go.Figure:
        """Cria diagrama visual do circuito"""
        fig = go.Figure()
        
        # Grid de fundo
        self._add_grid_to_figure(fig)
        
        # Componentes
        for component in self.components.values():
            self._add_component_to_figure(fig, component)
        
        # Conexões
        for connection in self.connections.values():
            self._add_connection_to_figure(fig, connection)
        
        # Configurações do layout
        fig.update_layout(
            title="🔧 Editor de Circuitos Interativo",
            xaxis=dict(
                range=[0, self.canvas_width],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                range=[0, self.canvas_height],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1
            ),
            showlegend=False,
            plot_bgcolor='white',
            width=self.canvas_width,
            height=self.canvas_height + 100,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig
    
    def _add_grid_to_figure(self, fig: go.Figure):
        """Adiciona grid ao diagrama"""
        # Linhas verticais
        for x in range(0, self.canvas_width + 1, self.grid_size):
            fig.add_shape(
                type="line",
                x0=x, y0=0, x1=x, y1=self.canvas_height,
                line=dict(color="lightgray", width=0.5)
            )
        
        # Linhas horizontais
        for y in range(0, self.canvas_height + 1, self.grid_size):
            fig.add_shape(
                type="line",
                x0=0, y0=y, x1=self.canvas_width, y1=y,
                line=dict(color="lightgray", width=0.5)
            )
    
    def _add_component_to_figure(self, fig: go.Figure, component: Component):
        """Adiciona componente visual ao diagrama"""
        color = self.COMPONENT_COLORS[component.type]
        symbol = self.COMPONENT_SYMBOLS[component.type]
        
        if component.type == ComponentType.RESISTOR:
            self._draw_resistor(fig, component, color)
        elif component.type == ComponentType.CAPACITOR:
            self._draw_capacitor(fig, component, color)
        elif component.type == ComponentType.INDUCTOR:
            self._draw_inductor(fig, component, color)
        elif component.type == ComponentType.VOLTAGE_SOURCE:
            self._draw_voltage_source(fig, component, color)
        elif component.type == ComponentType.CURRENT_SOURCE:
            self._draw_current_source(fig, component, color)
        elif component.type == ComponentType.GROUND:
            self._draw_ground(fig, component, color)
        else:
            # Componente genérico
            fig.add_scatter(
                x=[component.x],
                y=[component.y],
                mode='markers+text',
                marker=dict(size=20, color=color, symbol='square'),
                text=[symbol],
                textposition='middle center',
                name=component.label,
                hovertemplate=f"<b>{component.label}</b><br>" +
                            f"Tipo: {component.type.value}<br>" +
                            (f"Valor: {component.value} {component.unit}<br>" if component.value else "") +
                            f"Posição: ({component.x}, {component.y})<extra></extra>"
            )
        
        # Label do componente
        fig.add_annotation(
            x=component.x,
            y=component.y - 30,
            text=f"{component.label}" + (f"<br>{component.value} {component.unit}" if component.value else ""),
            showarrow=False,
            font=dict(size=10, color=color),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor=color,
            borderwidth=1
        )
    
    def _draw_resistor(self, fig: go.Figure, component: Component, color: str):
        """Desenha resistor"""
        x, y = component.x, component.y
        
        # Corpo do resistor (retângulo)
        fig.add_shape(
            type="rect",
            x0=x-20, y0=y-8, x1=x+20, y1=y+8,
            line=dict(color=color, width=2),
            fillcolor="white"
        )
        
        # Terminais
        fig.add_shape(type="line", x0=x-30, y0=y, x1=x-20, y1=y, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x+20, y0=y, x1=x+30, y1=y, line=dict(color=color, width=2))
        
        # Pontos de conexão
        fig.add_scatter(
            x=[x-30, x+30], y=[y, y],
            mode='markers',
            marker=dict(size=6, color=color),
            showlegend=False,
            hovertemplate="<extra></extra>"
        )
    
    def _draw_capacitor(self, fig: go.Figure, component: Component, color: str):
        """Desenha capacitor"""
        x, y = component.x, component.y
        
        # Placas do capacitor
        fig.add_shape(type="line", x0=x-5, y0=y-15, x1=x-5, y1=y+15, line=dict(color=color, width=3))
        fig.add_shape(type="line", x0=x+5, y0=y-15, x1=x+5, y1=y+15, line=dict(color=color, width=3))
        
        # Terminais
        fig.add_shape(type="line", x0=x-30, y0=y, x1=x-5, y1=y, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x+5, y0=y, x1=x+30, y1=y, line=dict(color=color, width=2))
        
        # Pontos de conexão
        fig.add_scatter(
            x=[x-30, x+30], y=[y, y],
            mode='markers',
            marker=dict(size=6, color=color),
            showlegend=False,
            hovertemplate="<extra></extra>"
        )
    
    def _draw_inductor(self, fig: go.Figure, component: Component, color: str):
        """Desenha indutor"""
        x, y = component.x, component.y
        
        # Bobinas (semicírculos)
        for i in range(-15, 16, 10):
            fig.add_shape(
                type="path",
                path=f"M {x+i},{y} Q {x+i+5},{y-10} {x+i+10},{y}",
                line=dict(color=color, width=2),
                fillcolor="rgba(0,0,0,0)"
            )
        
        # Terminais
        fig.add_shape(type="line", x0=x-30, y0=y, x1=x-15, y1=y, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x+15, y0=y, x1=x+30, y1=y, line=dict(color=color, width=2))
        
        # Pontos de conexão
        fig.add_scatter(
            x=[x-30, x+30], y=[y, y],
            mode='markers',
            marker=dict(size=6, color=color),
            showlegend=False,
            hovertemplate="<extra></extra>"
        )
    
    def _draw_voltage_source(self, fig: go.Figure, component: Component, color: str):
        """Desenha fonte de tensão"""
        x, y = component.x, component.y
        
        # Círculo
        fig.add_shape(
            type="circle",
            x0=x-15, y0=y-15, x1=x+15, y1=y+15,
            line=dict(color=color, width=2),
            fillcolor="white"
        )
        
        # Símbolos + e -
        fig.add_annotation(x=x-5, y=y, text="+", showarrow=False, font=dict(size=12, color=color))
        fig.add_annotation(x=x+5, y=y, text="−", showarrow=False, font=dict(size=12, color=color))
        
        # Terminais
        fig.add_shape(type="line", x0=x-30, y0=y, x1=x-15, y1=y, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x+15, y0=y, x1=x+30, y1=y, line=dict(color=color, width=2))
        
        # Pontos de conexão
        fig.add_scatter(
            x=[x-30, x+30], y=[y, y],
            mode='markers',
            marker=dict(size=6, color=color),
            showlegend=False,
            hovertemplate="<extra></extra>"
        )
    
    def _draw_current_source(self, fig: go.Figure, component: Component, color: str):
        """Desenha fonte de corrente"""
        x, y = component.x, component.y
        
        # Círculo
        fig.add_shape(
            type="circle",
            x0=x-15, y0=y-15, x1=x+15, y1=y+15,
            line=dict(color=color, width=2),
            fillcolor="white"
        )
        
        # Seta
        fig.add_annotation(
            x=x, y=y,
            text="→",
            showarrow=False,
            font=dict(size=16, color=color)
        )
        
        # Terminais
        fig.add_shape(type="line", x0=x-30, y0=y, x1=x-15, y1=y, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x+15, y0=y, x1=x+30, y1=y, line=dict(color=color, width=2))
        
        # Pontos de conexão
        fig.add_scatter(
            x=[x-30, x+30], y=[y, y],
            mode='markers',
            marker=dict(size=6, color=color),
            showlegend=False,
            hovertemplate="<extra></extra>"
        )
    
    def _draw_ground(self, fig: go.Figure, component: Component, color: str):
        """Desenha terra"""
        x, y = component.x, component.y
        
        # Símbolo do terra
        fig.add_shape(type="line", x0=x, y0=y, x1=x, y1=y-15, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x-15, y0=y-15, x1=x+15, y1=y-15, line=dict(color=color, width=3))
        fig.add_shape(type="line", x0=x-10, y0=y-20, x1=x+10, y1=y-20, line=dict(color=color, width=2))
        fig.add_shape(type="line", x0=x-5, y0=y-25, x1=x+5, y1=y-25, line=dict(color=color, width=1))
        
        # Ponto de conexão
        fig.add_scatter(
            x=[x], y=[y],
            mode='markers',
            marker=dict(size=6, color=color),
            showlegend=False,
            hovertemplate="<extra></extra>"
        )
    
    def _add_connection_to_figure(self, fig: go.Figure, connection: CircuitConnection):
        """Adiciona conexão visual entre componentes"""
        from_comp = self.components.get(connection.from_component)
        to_comp = self.components.get(connection.to_component)
        
        if from_comp and to_comp:
            # Linha conectando os componentes
            fig.add_shape(
                type="line",
                x0=from_comp.x, y0=from_comp.y,
                x1=to_comp.x, y1=to_comp.y,
                line=dict(color="#2c3e50", width=2)
            )
    
    def calculate_circuit_parameters(self) -> Dict:
        """Calcula parâmetros do circuito montado"""
        # Esta é uma implementação simplificada
        # Em uma versão completa, seria necessário resolver o circuito usando análise nodal
        
        total_resistance = 0
        total_capacitance = 0
        total_inductance = 0
        voltage_sources = []
        current_sources = []
        
        for component in self.components.values():
            if component.type == ComponentType.RESISTOR and component.value:
                total_resistance += component.value
            elif component.type == ComponentType.CAPACITOR and component.value:
                total_capacitance += component.value
            elif component.type == ComponentType.INDUCTOR and component.value:
                total_inductance += component.value
            elif component.type == ComponentType.VOLTAGE_SOURCE and component.value:
                voltage_sources.append(component.value)
            elif component.type == ComponentType.CURRENT_SOURCE and component.value:
                current_sources.append(component.value)
        
        return {
            'total_resistance': total_resistance,
            'total_capacitance': total_capacitance,
            'total_inductance': total_inductance,
            'voltage_sources': voltage_sources,
            'current_sources': current_sources,
            'num_components': len(self.components)
        }
    
    def export_circuit(self) -> Dict:
        """Exporta circuito para formato JSON"""
        return {
            'components': [asdict(comp) for comp in self.components.values()],
            'connections': [asdict(conn) for conn in self.connections.values()]
        }
    
    def import_circuit(self, circuit_data: Dict):
        """Importa circuito de formato JSON"""
        self.components = {}
        self.connections = {}
        
        # Importar componentes
        for comp_data in circuit_data.get('components', []):
            comp_data['type'] = ComponentType(comp_data['type'])
            component = Component(**comp_data)
            self.components[component.id] = component
        
        # Importar conexões
        for conn_data in circuit_data.get('connections', []):
            connection = CircuitConnection(**conn_data)
            self.connections[connection.id] = connection

class CircuitTemplates:
    """Templates de circuitos pré-definidos"""
    
    @staticmethod
    def get_rc_circuit() -> Dict:
        """Circuito RC simples"""
        return {
            'name': '🔋 Circuito RC',
            'description': 'Circuito resistor-capacitor simples',
            'components': [
                {
                    'id': 'v1', 'type': 'voltage_source', 'x': 100, 'y': 200,
                    'value': 12, 'unit': 'V', 'label': 'V1', 'connected_to': []
                },
                {
                    'id': 'r1', 'type': 'resistor', 'x': 300, 'y': 200,
                    'value': 1000, 'unit': 'Ω', 'label': 'R1', 'connected_to': []
                },
                {
                    'id': 'c1', 'type': 'capacitor', 'x': 500, 'y': 200,
                    'value': 100, 'unit': 'µF', 'label': 'C1', 'connected_to': []
                },
                {
                    'id': 'gnd1', 'type': 'ground', 'x': 300, 'y': 350,
                    'value': None, 'unit': None, 'label': 'GND', 'connected_to': []
                }
            ],
            'connections': []
        }
    
    @staticmethod
    def get_rl_circuit() -> Dict:
        """Circuito RL simples"""
        return {
            'name': '🌀 Circuito RL',
            'description': 'Circuito resistor-indutor simples',
            'components': [
                {
                    'id': 'v1', 'type': 'voltage_source', 'x': 100, 'y': 200,
                    'value': 24, 'unit': 'V', 'label': 'V1', 'connected_to': []
                },
                {
                    'id': 'r1', 'type': 'resistor', 'x': 300, 'y': 200,
                    'value': 500, 'unit': 'Ω', 'label': 'R1', 'connected_to': []
                },
                {
                    'id': 'l1', 'type': 'inductor', 'x': 500, 'y': 200,
                    'value': 10, 'unit': 'mH', 'label': 'L1', 'connected_to': []
                },
                {
                    'id': 'gnd1', 'type': 'ground', 'x': 300, 'y': 350,
                    'value': None, 'unit': None, 'label': 'GND', 'connected_to': []
                }
            ],
            'connections': []
        }
    
    @staticmethod
    def get_rlc_circuit() -> Dict:
        """Circuito RLC completo"""
        return {
            'name': '⚡ Circuito RLC',
            'description': 'Circuito resistor-indutor-capacitor completo',
            'components': [
                {
                    'id': 'v1', 'type': 'voltage_source', 'x': 100, 'y': 300,
                    'value': 220, 'unit': 'V', 'label': 'V1', 'connected_to': []
                },
                {
                    'id': 'r1', 'type': 'resistor', 'x': 300, 'y': 200,
                    'value': 100, 'unit': 'Ω', 'label': 'R1', 'connected_to': []
                },
                {
                    'id': 'l1', 'type': 'inductor', 'x': 500, 'y': 200,
                    'value': 50, 'unit': 'mH', 'label': 'L1', 'connected_to': []
                },
                {
                    'id': 'c1', 'type': 'capacitor', 'x': 300, 'y': 400,
                    'value': 220, 'unit': 'µF', 'label': 'C1', 'connected_to': []
                },
                {
                    'id': 'gnd1', 'type': 'ground', 'x': 100, 'y': 450,
                    'value': None, 'unit': None, 'label': 'GND', 'connected_to': []
                }
            ],
            'connections': []
        }
