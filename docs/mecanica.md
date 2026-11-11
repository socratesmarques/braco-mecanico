# Avaliação mecânica preliminar

Todas as massas e fatores abaixo são **hipóteses para triagem**, não medições ou capacidade garantida. O cálculo está em `scripts/torque.py`, com entradas explícitas em `docs/load_scenario.json`. Executar `python scripts/torque.py`. O cenário deve ser atualizado manualmente quando comprimentos ou componentes mudarem.

## Geometria e massa

Altura do eixo do ombro: 6 + 4 + 6 + 30 = 46 mm. Elos: 110 e 100 mm entre eixos. Em pose vertical (ombro 90°, cotovelo 0°), a ponta do dedo fixo chega a 46 + 110 + 100 + 8 + 40 + 4 = **308 mm**. Alcance horizontal geométrico até a ponta: 262 mm. Não equivale a espaço de trabalho livre de colisões; a pose inicial usa 75° e −35°.

| Massa de cenário | kg | Centro de massa a partir do ombro, braço horizontal |
| --- | ---: | ---: |
| Elo superior completo, placas/espaçadores/ferragens | 0,100 | 0,055 m |
| Atuador do cotovelo | 0,060 | 0,110 m |
| Antebraço completo, sem garra | 0,080 | 0,160 m |
| Garra completa, incluindo seu atuador | 0,090 | 0,230 m |
| Objeto (meta exploratória) | 0,050 | 0,255 m |
| Massa centrada fixa/base/atuadores proximais | 0,300 | 0 m |

Se o motor do cotovelo ficar no antebraço com centro deslocado, sua contribuição ao torque do cotovelo deixa de ser zero; recalcular. Fontes externas não contam como lastro. Pesar cada subconjunto com cabos e ferragens. Volume STL é de um sólido, não a massa de uma peça fatiada; obter massa estimada no fatiador com material/preenchimento reais e conferir na balança.

## Torque de ombro e cotovelo

Adotar g = 9,80665 m/s² e braço horizontal, condição desfavorável de gravidade para esta cadeia. T = g × Σ(m × distância horizontal ao eixo). Usar kg e m; **1 kgf·cm = 0,0980665 N·m**. O rótulo comercial “kg·cm” normalmente pretende kgf·cm, mas confirmar no datasheet.

```text
T_ombro = g × [0,100×0,055 + 0,060×0,110 + 0,080×0,160
               + 0,090×0,230 + 0,050×0,255]
T_cotovelo = g × [0,080×0,050 + 0,090×0,120 + 0,050×0,145]
```

| Junta | Estático | Alvo preliminar com fator 2 | Conversão do alvo |
| --- | ---: | ---: | ---: |
| Ombro | 0,572218 N·m | 1,144436 N·m | 11,67 kgf·cm |
| Cotovelo | 0,216237 N·m | 0,432473 N·m | 4,41 kgf·cm |

O fator 2 é margem exploratória para partida, atrito e incertezas; não modela aceleração nem certifica resistência. **Não selecionar servo cujo torque de bloqueio apenas iguale esses alvos.** Verificar torque sustentado, tensão real, temperatura, duração e velocidade. Se só houver torque de bloqueio, faltam dados para aprovação. Uma redução ou mola/contrapeso pode ser necessária, mas acrescenta esforço, massa e manutenção.

Base vertical: gravidade não produz diretamente torque de rotação em torno de Z, porém produz momento de tombamento e esforço no apoio. Dimensionar acionamento por `T = I_z × aceleração_angular + atrito + torque_dos_cabos`, e apoio axial/radial pelo peso e momento. Não copiar automaticamente o servo do ombro. Para a garra, `T ≈ força_no_dedo × braço_efetivo / eficiência`, conforme transmissão; definir atrito, objeto e força admissível antes de escolher servo. O conceito não determina ainda a força de preensão.

## Tombamento e ancoragem

Para a base de 120 mm, considerar a borda a 0,060 m na direção do alcance (caso conservador para a base quadrada). Calcular momentos sobre essa borda, separando massas externas e internas:

```text
M_tomba = g × Σ[m × max(x − 0,060; 0)]
M_restaura = g × [massa_centrada × 0,060 + Σ(m × max(0,060 − x; 0))]
```

O cenário retorna **0,353530 N·m** de tombamento e **0,181423 N·m** de restauração: razão **0,513**, portanto não se sustenta livremente nessa hipótese. Para razão estática 1,5 seria necessária massa centrada total de cerca de **0,893 kg** (aproximadamente 0,593 kg além da hipótese de 0,300 kg), sem contar efeitos dinâmicos ou deslizamento.

A decisão inicial é **ancorar a base à bancada**, usando as quatro posições disponíveis após dimensionar fixadores e superfície. Não tratar os furos candidatos como prova de ancoragem suficiente. Uma base mais larga ou lastro pode ser estudada; recalcular peso, apoio, aderência e envelope da impressora.

## Caminho de carga e esforços

- Objeto → dedos → palma → antebraço → eixo do cotovelo → braço → eixo do ombro → pedestais → prato → apoio axial/radial → base → bancada. O eixo do servo deve principalmente fornecer torque; não substituir toda essa cadeia de apoio.
- Os elos duplos distribuem esforço, mas o compartilhamento depende de eixos, espaçadores e aperto reais. Um eixo contínuo entre dois apoios permite estudar duplo cisalhamento; não presumir que a condição já está garantida pelo desenho.
- Como triagem: flexão `σ = M·c/I`, cisalhamento médio de pino em duplo corte `τ ≈ F/(2A)`, pressão de contato `p ≈ F/(d·t)`. Determinar forças/reação e geometria efetiva antes de substituir valores. Falta material caracterizado para calcular margens confiáveis.
- Furos concentram tensões; camadas, poros, orientação e temperatura alteram resistência. Verificar esmagamento sob arruelas, trinca entre furo e borda, deformação prolongada e folga após ciclos. Não usar resistência de material maciço como aprovação de peça FDM.
- O pé em L do pedestal sofre flexão e força de arrancamento. A orientação inicial deixa a parede vertical; avaliar camadas e necessidade de nervura/novo suporte após ensaio. Os furos horizontais podem exigir acabamento/suporte.
- A palma lateral introduz torção no antebraço. Confirmar acesso aos dois fixadores e, se necessário, criar travessa simétrica com interface real de servo.
- Eixos precisam de retenção axial, espaçamento e ajustes medidos; folga diametral de passagem não é especificação de bucha. O prato necessita suporte de momento, não apenas um parafuso central.
- Não há batentes, canal de cabos, rolamentos ou acoplamentos completos. Inspecionar interferências em todo o curso; cabos devem ter alívio e laço sem entrar nas juntas. Limitar rotação de base para não enrolar cabos.

## Alimentação e testes futuros

Dimensionar a fonte com tensão compatível e picos simultâneos dos servos, considerando limite/proteção e queda em cabos. Separar distribuição de potência e lógica com terra comum. A referência [Pololu sobre servos](https://www.pololu.com/blog/16/electrical-characteristics-of-servos-and-introduction-to-the-servo-control-interface) explica a relação entre corrente e estado do motor; dados finais devem vir dos modelos comprados.

Ensaiar primeiro sem carga, depois incrementar massa, com base ancorada e área livre. Medir corrente, tensão no servo, aquecimento, deflexão e repetibilidade. Não manter servo deliberadamente travado para “comprovar” torque. Definir velocidade e duty cycle antes da aprovação. O corte de potência pode fazer o braço cair: prever apoio mecânico/posição segura durante testes e manutenção.
