"""
Teste rápido do construtor de circuitos
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from circuit_editor import CircuitBuilder, ComponentType, CircuitTemplates

def test_circuit_builder():
    print("🔧 Testando o Construtor de Circuitos...")
    
    # Criar o builder
    builder = CircuitBuilder()
    print("✅ CircuitBuilder criado com sucesso!")
    
    # Testar adição de componentes
    print("\n📌 Adicionando componentes...")
    
    # Adicionar fonte de tensão
    voltage_id = builder.add_component(ComponentType.VOLTAGE_SOURCE, 100, 100, 12.0, "V")
    print(f"   ⊕ Fonte de tensão: {voltage_id[:8]}...")
    
    # Adicionar resistor
    resistor_id = builder.add_component(ComponentType.RESISTOR, 200, 100, 1000.0, "Ω")
    print(f"   ⬛ Resistor: {resistor_id[:8]}...")
    
    # Adicionar capacitor
    capacitor_id = builder.add_component(ComponentType.CAPACITOR, 300, 100, 100.0, "µF")
    print(f"   ⚏ Capacitor: {capacitor_id[:8]}...")
    
    # Conectar componentes
    print("\n🔗 Conectando componentes...")
    connection1 = builder.connect_components(voltage_id, resistor_id)
    print(f"   🔗 Conexão 1: {connection1[:8]}...")
    
    connection2 = builder.connect_components(resistor_id, capacitor_id)
    print(f"   🔗 Conexão 2: {connection2[:8]}...")
    
    # Calcular parâmetros
    print("\n📊 Calculando parâmetros...")
    params = builder.calculate_circuit_parameters()
    print(f"   📋 Componentes: {params['num_components']}")
    print(f"   ⚡ Resistência total: {params['total_resistance']:.1f} Ω")
    print(f"   ⚏ Capacitância total: {params['total_capacitance']:.1f} µF")
    
    # Testar templates
    print("\n📋 Testando templates...")
    rc_template = CircuitTemplates.get_rc_circuit()
    print(f"   📄 Template RC: {rc_template['name']}")
    print(f"   🧩 Componentes: {len(rc_template['components'])}")
    
    # Criar diagrama
    print("\n🎨 Criando diagrama...")
    try:
        fig = builder.create_circuit_diagram()
        print("   ✅ Diagrama criado com sucesso!")
    except Exception as e:
        print(f"   ❌ Erro no diagrama: {e}")
    
    # Exportar circuito
    print("\n💾 Exportando circuito...")
    circuit_data = builder.export_circuit()
    print(f"   📦 Dados exportados: {len(str(circuit_data))} caracteres")
    
    print("\n🎉 Teste concluído com sucesso!")
    return True

if __name__ == "__main__":
    try:
        test_circuit_builder()
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
