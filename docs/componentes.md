# Componentes, compras e medições

Nenhum modelo comercial foi escolhido. Quantidades são preliminares; custos, fornecedor e especificações ficam pendentes. Não comprar os quatro atuadores iguais por conveniência antes de avaliar a demanda de cada junta.

| Componente | Quantidade prevista | O que decidir/medir |
| --- | --- | --- |
| ESP32 em placa de desenvolvimento | 1 | Modelo, alimentação, dimensões, conectores, furos, GPIO disponíveis/boot e compatibilidade de sinais |
| Servo posicional da base | 1 | Torque por atrito/inércia, curso, massa, corrente, envelope e interfaces |
| Servo posicional do ombro | 1 | Demanda sustentada e dinâmica, redução/contrabalanço se necessário, massa, corrente e aquecimento |
| Servo posicional do cotovelo | 1 | Torque e massa distal, curso, corrente e envelope |
| Atuador da garra | 1 | Força de aperto, curso, geometria de transmissão e corrente |
| Horns originais compatíveis | Até 4 | Estria, parafuso central, altura, diâmetro e padrão exato de furação; não imprimir spline nesta versão |
| Eixos/pinos de base, ombro e cotovelo | 3 conjuntos | Diâmetro, comprimento, material, retenção, ajuste e superfícies de apoio |
| Buchas/rolamentos + apoio axial da base | A dimensionar | ID/OD/largura reais, carga radial/axial, folga e alojamento; não há encaixe modelado |
| Fixadores de placas/espaçadores | 4 conjuntos atravessantes | Diâmetro candidato 3 mm, comprimento útil, cabeças, arruelas, porcas e acesso |
| Fixadores pedestais/prato | 4 conjuntos | Diâmetro candidato 3 mm, espessura do pé/prato, acesso inferior ao prato |
| Fixadores palma/antebraço | 2 conjuntos | Furo distal candidato 5 mm e outro 3 mm, arruela de afastamento; revisar assimetria |
| Fixadores dedos | 3 conjuntos | Dois travam dedo fixo; um pivô do móvel com bucha/arruelas e retenção sem travar rotação |
| Ancoragem à bancada | 4 posições | Furos candidatos de 4 mm; dimensionar conforme bancada e esforço |
| Fonte dos atuadores | 1 | Tensão real dos servos, picos simultâneos, proteção, cabos e conectores |
| Regulador para lógica | Conforme fonte/placa | Tensão e corrente compatíveis com a placa; não alimentar motores pelo ESP32 |
| Corte de potência, proteção e distribuição | 1 conjunto | Corrente, fusível, chave acessível, retorno comum, desacoplamento e alívio de tração |
| Filamento e material de contato da garra | Conforme fatiamento | Material disponível, rigidez, temperatura, aderência e atrito dos pads |

As especificações elétricas de servos variam e a corrente de partida/bloqueio importa para a fonte. Referência técnica: [Pololu — características elétricas de servos](https://www.pololu.com/blog/16/electrical-characteristics-of-servos-and-introduction-to-the-servo-control-interface). Usar datasheet do modelo escolhido e medição; não deduzir corrente pelo tamanho externo.

## Ficha obrigatória por atuador

Copiar uma linha por base/ombro/cotovelo/garra. Campos vazios continuam pendentes, não zero.

| Campo | Registro inicial |
| --- | --- |
| Junta, fabricante, modelo, unidade/lote e fonte do datasheet | Pendente |
| Tensão nominal/faixa, nível de sinal aceito e pinagem | Pendente |
| Torque nominal contínuo, bloqueio, velocidade e condições de teste | Pendente; se contínuo não informado, caracterizar em ensaio |
| Corrente em repouso, movimento, partida/bloqueio e proteção | Pendente |
| Massa com horn/cabo e posição aproximada do centro de massa | Pendente |
| Corpo X/Y/Z, abas e envelope total com conector | Pendente |
| Distâncias entre centros de furos X/Y, diâmetros e espessura das abas | Pendente |
| Posição do eixo em relação ao corpo e altura do horn montado | Pendente |
| Estria, parafuso central e furação do horn | Pendente |
| Curso medido, sentido, folga, posição neutra e batentes | Pendente |
| Instrumento, resolução, data, operador e foto/croqui cotado | Pendente |

Use paquímetro e croqui com origem e eixos. Verifique medidas em mais de uma orientação. Meça também cabeça de parafuso, porca, arruela, ressalto e raio de canto: passagem do corpo não garante acesso para montagem. Meça peças compradas antes de preencher `servo_*` ou `bearing_*`; esses campos `undef` são um registro de pendências e ainda não geram suportes automaticamente.

## Lista impressa conceitual

| Seletor `part` | Quantidade no braço | Função |
| --- | ---: | --- |
| `base` | 1 | Fixação na bancada |
| `turntable` | 1 | Prato móvel |
| `pedestal` | 2 | Apoios do ombro |
| `upper_link` | 2 | Laterais do braço |
| `fore_link` | 2 | Laterais do antebraço |
| `upper_spacer` | 2 | União das laterais do braço |
| `fore_spacer` | 2 | União das laterais do antebraço |
| `palm` | 1 | Suporte da garra |
| `fixed_finger` | 1 | Dedo fixo |
| `moving_finger` | 1 | Dedo móvel |
| `tolerance_coupon` | 0 (1 para ensaio) | Furos de calibração |

Total: 15 peças estruturais e um cupom de ensaio. Não inclui peças de adaptação de servos, apoios da base e retenções ainda não projetados.
