# Requisitos e critérios de aceitação

Versão conceitual de 11/11/2026. Estado inicial: somente `README.md` com o título do projeto, commit `4437e69`; árvore de trabalho limpa, sem CAD, firmware, dependências ou instruções locais. Não houve código legado a preservar.

| ID | Requisito | Critério / situação |
| --- | --- | --- |
| MEC-01 | Aproximadamente 30 cm de altura | Conceito vertical com 308 mm até a ponta; medir conjunto real com atuadores |
| MEC-02 | Base, ombro, cotovelo e garra | Três rotações de posicionamento e abertura da garra; sem punho independente; acionamentos pendentes |
| MEC-03 | Modular e de baixo custo | Placas repetidas, espaçadores e ferragens comuns; custo depende de cotação e torque, sem orçamento inventado |
| MEC-04 | Compatível com Ender 3 original | Cada peça isolada ≤ 220 × 220 × 250 mm; verificador usa 210 × 210 mm em XY para margem |
| MEC-05 | Dimensões e encaixes paramétricos | Centralizados, documentados, com variação exportada e entradas inválidas rejeitadas |
| MEC-06 | Suportar carga útil definida | Meta exploratória de 50 g, ainda não aceita como capacidade; validar peso, alcance e ciclo de trabalho |
| MEC-07 | Resistência e estabilidade | Apoios bilaterais no conceito; base ancorada; buchas/rolamentos, eixos e retenção a dimensionar |
| MEC-08 | Fabricação e manutenção | Peças separadas, acesso aos parafusos e passagem de cabos a verificar; cupom de tolerâncias antes do conjunto |
| ELE-01 | ESP32 e quatro atuadores | Escolher placa, servos posicionais, fonte e proteção; não usar servo de rotação contínua como substituto direto de posicional |
| ELE-02 | Alimentação robusta | Fonte de servos dimensionada com corrente e tensão reais; ESP32 regulado; terra comum; testar queda de tensão e reset |
| SW-01 | Firmware C++/PlatformIO | Somente arquitetura nesta entrega; futuros limites, interpolação e parada no ESP32 |
| WEB-01 | Controle responsivo pelo celular | Somente requisitos; futura UI com conexão, posições, limites e parada claramente visíveis |
| AUTO-01 | Salvar e executar sequências | Futuras poses de quatro canais + duração, versão do formato, validação e cancelamento |
| SAFE-01 | Falhas previsíveis | Futuro boot sem movimento inesperado, perda de conexão definida, interrupção de sequência, limite calibrado por eixo |

## Limites de escopo

A entrega permite visualizar, alterar e exportar o conceito. Não inclui suporte de servo específico, spline/horn, transmissão da base/garra, eletrônica montada, firmware, interface web, capacidade de carga certificada ou STL de produção. A renderização não demonstra montagem funcional nem ausência de colisão.

## Portas de validação

1. Escolher e medir componentes; aprovar alcance, carga, velocidades e orçamento.
2. Revisar torque/corrente, apoios e fixação; resolver interfaces reais no CAD.
3. Imprimir cupom e uma junta; medir folga, atrito, resistência e retenção.
4. Montar estrutura sem energia e verificar curso, cabos, acesso e estabilidade.
5. Só então implementar eletrônica e controle; testar um eixo por vez, depois o conjunto com carga progressiva.
