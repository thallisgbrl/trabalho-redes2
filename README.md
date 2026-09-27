# Trabalho Prático de Redes II - Roteamento IP

Projeto desenvolvido para a disciplina de Redes de Computadores II (UNISINOS) sob orientação do Prof. Cristiano Bonato Both.

## Integrantes
- Thallis Gabriel de Mello da Silva

## Descrição da Topologia
Ambiente experimental em Docker Compose contendo:
- **5 Roteadores FRRouting (FRR):** R1, R2, R3, R4, R5
- **2 Hosts de Acesso:** PC-A (10.0.1.100) e PC-B (10.0.5.100)
- Múltiplos caminhos alternativos para testes de redundância e convergência diante de falhas de enlace.

## Como Executar

### 1. Subir a Infraestrutura
```bash
docker compose up -d

## Link do Vídeo Demonstrativo
https://youtu.be/ixYSdVVnl9s
