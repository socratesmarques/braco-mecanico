# Instruções de desenvolvimento

Projeto acadêmico: braço de aproximadamente 30 cm, quatro ações (base, ombro, cotovelo e garra), ESP32, C++/PlatformIO, futura interface web móvel e sequências graváveis. Primeira etapa exclusivamente documental e CAD conceitual. Não implementar firmware ou web sem nova solicitação.

## Mecânica

- Ender 3 original: envelope 220 × 220 × 250 mm; reservar margem de mesa/brim.
- CAD em mm/graus; cálculos em kg, m, N, N·m. Declarar conversões.
- Centralizar parâmetros em `cad/parameters.scad`; não espalhar encaixes pelos módulos.
- Nunca presumir medidas de servos, estrias, horns, abas, rolamentos ou porcas. Exigir ficha técnica e medição da unidade. Dados desconhecidos ficam `undef`/pendentes.
- Distinguir escolhas conceituais de medições. Nunca apresentar STL conceitual como validado fisicamente.
- Prever apoios independentes do eixo do servo, ancoragem, cabos, acesso a parafusos e orientação de camadas.
- Avaliar massa distal, torque, deflexão, estabilidade e corrente antes da escolha de atuadores. Torque de bloqueio não é torque contínuo.

## Organização e verificação

- Sólidos em `cad/lib/parts.scad`; montagem em `assembly.scad`; seleção em `main.scad`.
- Uma peça por STL, sem hardware de referência.
- Após mudar CAD, executar `python scripts/verify.py`; após mudar hipóteses mecânicas, executar `python scripts/torque.py` e atualizar documentação.
- Falhar em erros/avisos OpenSCAD, malhas abertas, peças desconectadas e envelope excedido. Testar também alterações de parâmetros.
- Inspecionar imagens; registrar ferramentas, comandos, resultados e limitações em `docs/validacao.md`.
- Não versionar `build/`, ambientes locais, STL regeneráveis ou credenciais. Não fazer commit automaticamente.
- Documentação em português; identificadores simples; evitar dependências desnecessárias.

## Etapas futuras

Quando autorizadas: PlatformIO em `firmware/`, interface responsiva em `web/`. Limites e parada pertencem ao dispositivo; validar comandos e versionar sequências. A segurança do movimento não deve depender do navegador.
