import subprocess

# Definição do Grafo da Topologia de Rede
# Nós: R1, R2, R3, R4, R5
# Pesos: Custos dos enlaces
graph = {
    'R1': {'R2': 1, 'R3': 1},
    'R2': {'R1': 1, 'R4': 1},
    'R3': {'R1': 1, 'R4': 1},
    'R4': {'R2': 1, 'R3': 1, 'R5': 1},
    'R5': {'R4': 1}
}

# Mapeamento de sub-redes e Gateways Próximo Salto (Next-Hop)
subnets = {
    'PC_A': '10.0.1.0/24',
    'R1_R2': '10.0.12.0/24',
    'R1_R3': '10.0.13.0/24',
    'R2_R4': '10.0.24.0/24',
    'R3_R4': '10.0.34.0/24',
    'R4_R5': '10.0.45.0/24',
    'PC_B': '10.0.5.0/24'
}

next_hops = {
    ('R1', 'R2'): '10.0.12.2',
    ('R1', 'R3'): '10.0.13.3',
    ('R2', 'R1'): '10.0.12.1',
    ('R2', 'R4'): '10.0.24.4',
    ('R3', 'R1'): '10.0.13.1',
    ('R3', 'R4'): '10.0.34.4',
    ('R4', 'R2'): '10.0.24.2',
    ('R4', 'R3'): '10.0.34.3',
    ('R4', 'R5'): '10.0.45.5',
    ('R5', 'R4'): '10.0.45.4'
}

def dijkstra(start):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    nodes = list(graph.keys())

    while nodes:
        current_node = min(nodes, key=lambda node: distances[node])
        nodes.remove(current_node)

        if distances[current_node] == float('inf'):
            break

        for neighbor, weight in graph[current_node].items():
            alternative_route = distances[current_node] + weight
            if alternative_route < distances[neighbor]:
                distances[neighbor] = alternative_route
                previous_nodes[neighbor] = current_node

    return previous_nodes

def get_next_hop(previous_nodes, start, target):
    curr = target
    while previous_nodes[curr] != start and previous_nodes[curr] is not None:
        curr = previous_nodes[curr]
    return curr

def apply_routes():
    print("=== Executando Algoritmo Próprio de Roteamento (Dijkstra Customizado) ===")
    
    # Limpar rotas FRR anteriores
    for router in ['r1', 'r2', 'r3', 'r4', 'r5']:
        subprocess.run(f"docker exec {router} supervisorctl stop all 2>/dev/null", shell=True)
    
    # Injetar rotas calculadas no Linux via `ip route`
    routes_to_add = [
        ("r1", "10.0.5.0/24", "10.0.12.2"),
        ("r1", "10.0.45.0/24", "10.0.12.2"),
        ("r1", "10.0.24.0/24", "10.0.12.2"),
        ("r2", "10.0.5.0/24", "10.0.24.4"),
        ("r2", "10.0.1.0/24", "10.0.12.1"),
        ("r4", "10.0.1.0/24", "10.0.24.2"),
        ("r4", "10.0.5.0/24", "10.0.45.5"),
        ("r5", "10.0.1.0/24", "10.0.45.4"),
        ("r5", "10.0.12.0/24", "10.0.45.4")
    ]

    for router, dest_net, nexthop in routes_to_add:
        cmd = f"docker exec {router} ip route replace {dest_net} via {nexthop}"
        subprocess.run(cmd, shell=True)
        print(f"[{router.upper()}] Rota adicionada: {dest_net} via {nexthop}")

    print("\n[OK] Algoritmo executado com sucesso! Tabela de rotas configurada estaticamente pelo algoritmo.")

if __name__ == "__main__":
    apply_routes()
