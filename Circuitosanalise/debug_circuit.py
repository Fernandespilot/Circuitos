print("🔍 Debug step-by-step...")

try:
    print("1. Imports básicos...")
    from enum import Enum
    from dataclasses import dataclass
    from typing import Dict, List, Tuple, Optional
    import uuid
    import json
    print("✅ OK")

    print("2. NumPy...")
    import numpy as np
    print("✅ OK")
    
    print("3. Plotly...")
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    print("✅ OK")
    
    print("4. ComponentType...")
    class ComponentType(Enum):
        VOLTAGE_SOURCE = "voltage_source"
        CURRENT_SOURCE = "current_source"
        RESISTOR = "resistor"
        CAPACITOR = "capacitor"
        INDUCTOR = "inductor"
        GROUND = "ground"
        SWITCH = "switch"
    print("✅ OK")
    
    print("5. Component dataclass...")
    @dataclass
    class Component:
        id: str
        type: ComponentType
        x: float
        y: float
        value: float = 0.0
        unit: str = ""
        connections: List[str] = None
        
        def __post_init__(self):
            if self.connections is None:
                self.connections = []
    print("✅ OK")
    
    print("6. CircuitBuilder básico...")
    class CircuitBuilder:
        def __init__(self):
            self.components: Dict[str, Component] = {}
            self.connections: Dict[str, Tuple[str, str]] = {}
    print("✅ OK")
    
    print("🎉 Debug concluído! Sem erros encontrados.")
    
except Exception as e:
    print(f"❌ Erro encontrado: {e}")
    import traceback
    traceback.print_exc()
