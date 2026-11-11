# Fase 2 — seleção proposta de componentes e validação mecânica

**Data da pesquisa: 11/11/2026. Estado: proposta para aprovação, não liberação para compra integral ou impressão.** O nome deste arquivo identifica a consolidação da Fase 2; as interfaces não estão finalizadas. Nenhum encaixe OpenSCAD foi alterado. Não foram implementados firmware ou interface web.

## 1. Recomendação

Adotar **1 MG996R na base, 2 DS3218 posicionais de 180° no ombro/cotovelo e 1 MG90S posicional na garra**, com alimentação dos servos inicialmente especificada em 5,0 V e apoios mecânicos independentes. A compra depende de confirmar versão, procedência, faixa de alimentação e dados da unidade; sobretudo os nomes MG996R/MG90S aparecem em produtos com características diferentes.

O cenário de 50 g resulta em **0,534 N·m estático no ombro** e **0,182 N·m no cotovelo**. Com fator de projeto exploratório 2, os alvos são **1,069 e 0,364 N·m**, respectivamente. Esses valores não são capacidade comprovada do braço. A base deverá ser presa a uma placa rígida e à bancada.

O custo previsto da solução completa é **R$ 996–1.698**, incluindo um rolo inteiro de filamento, ferragens compradas em pequenas quantidades, alimentação, eletrônica reservada para a próxima fase e testador de servo. Com reserva de 20%: **R$ 1.195,20–2.037,60**, mais frete e eventual usinagem. O orçamento discrimina preços observados e provisões ainda sem cotação. Reaproveitar fonte, ESP32, filamento e ferramentas do laboratório é a principal oportunidade de economia.

## 2. Revisão do modelo existente

Foram examinados `cad/main.scad`, `cad/parameters.scad`, `cad/lib/parts.scad`, `cad/lib/assembly.scad`, os requisitos, a arquitetura, a documentação mecânica e os relatórios da Fase 1.

| Observação do CAD atual | Consequência para a Fase 2 |
| --- | --- |
| Elos de 110 e 100 mm; ponta a 308 mm em pose vertical | Manter esses comprimentos no cálculo de referência; apoios reais podem alterar a altura total |
| Base de 120 × 120 × 6 mm, prato Ø88 × 6 mm | Cabe na Ender 3, mas não assegura estabilidade nem espaço para transmissão |
| Vão de apenas 4 mm sob o prato | Não acomoda o cartucho de rolamentos proposto; há revisão obrigatória da base |
| Placas de 5 mm e bosses de Ø24 mm | Alojamentos de rolamentos precisam de ombro, tampa e espessura local; não basta alargar o furo |
| Vão interno do elo superior: 31 mm; antebraço: 15 mm | Um servo DS3218 tem menor dimensão de catálogo de 20 mm: não cabe dentro do antebraço atual. Propor montagem externa no segmento proximal, com eixo apoiado |
| Separação entre centros das placas: 36 mm no braço e 20 mm no antebraço | Hubs, anéis, parafusos e cabos precisam de revisão de espaço e acesso |
| `pin_hole_d=5,4 mm` é furo de passagem | Não é alojamento Ø16 de 625ZZ nem ajuste de eixo/rolamento |
| Palma fixada lateralmente por dois pontos | Gera torção; propor uma travessa que distribua a carga às duas placas |
| Dedo de 8 mm de largura, pivô com furo de 3,4 mm | Instalar uma bucha maior exigirá boss local reforçado, ainda não modelado |
| `servo_*` e `bearing_*` continuam `undef` | Preencher somente após medir as peças e aprovar o redesenho |

**Compatibilidade de altura pendente:** dois 608 de 7 mm separados por 30 mm entre centros ocupam pelo menos 37 mm na direção vertical, antes de tampas, folgas e transmissão. Substituir o vão de 4 mm por um módulo de aproximadamente 40–50 mm elevaria o conceito para aproximadamente **344–354 mm**, mantendo os outros parâmetros. Essa faixa é reserva de integração, não desenho acabado. Para manter uma meta estrita de 300 mm será preciso rever comprimentos/altura do ombro ou escolher outro apoio de base. Reduzir elos também reduz torque, mas exige novos cálculos e revisão das assertions; não foi feito nesta fase.

## 3. Servomotores e critérios de seleção

Todos devem ser **posicionais**, com engrenagens metálicas. Não comprar versão de rotação contínua/360° como substituta. O curso mecânico seguro do braço será menor que o curso anunciado do servo.

| Junta | Seleção principal | Dado de fabricante usado na triagem | Justificativa |
| --- | --- | --- | --- |
| Base | MG996R | 9,4 kgf·cm de bloqueio a 4,8 V; 11 a 6 V; massa publicada 55 g | O eixo vertical demanda principalmente torque de inércia/atrito; os rolamentos devem receber peso e momento |
| Ombro | DS3218, versão posicional 180° | 18 kgf·cm de bloqueio a 5 V; 21,5 a 6,8 V; 60 g | Alvo de 10,90 kgf·cm com margem fica abaixo do bloqueio publicado; precisa comprovar sustentação térmica |
| Cotovelo | DS3218, mesma versão | Mesmos dados do ombro | Padroniza suporte, horn e reposição; dá margem para atrito e futuras adaptações, sem grande penalidade de massa |
| Garra | MG90S, versão posicional | 1,8 kgf·cm de bloqueio a 4,8 V; massa publicada 13,4 g | Reduz massa distal; alvo de aproximadamente 0,95 kgf·cm para a hipótese de preensão calculada abaixo |

Fontes técnicas: [DSSERVO — DS3218, páginas 1–2](https://www.dsservo.com/d_file/DS3218%20datasheet.pdf), [TowerPro — MG996R](https://towerpro.com.tw/product/mg996R/) e [TowerPro — MG90S](https://towerpro.com.tw/product/mg90s-3/). Valores de bloqueio não são valores contínuos. Não existe, nessas fontes consultadas, curva suficiente para certificar o ciclo térmico deste braço.

**Alimentação da garra ainda exige confirmação documental:** a página oficial do MG90S apresenta operação em 4,8 V e pontos de desempenho em outras tensões, sem uma faixa inequívoca. Comprar somente uma unidade cuja documentação correspondente confirme operação em **5,0 V**. Não atribuir automaticamente a todo “MG90S” uma faixa de 4,8–6 V. Se isso não for confirmado, trocar o candidato ou rever a alimentação antes de energizar. Os cálculos da garra usam o ponto publicado de 4,8 V, sem interpolação de torque.

Para o MG996R, também se usa o ponto de 4,8 V como referência conservadora para a bancada de 5,0 V. O DS3218 tem ponto publicado exatamente em 5 V. A tensão deve ser medida **no conector do servo sob carga**, não apenas na saída da fonte.

### Alternativas e limites da escolha

- **Ombro com mais margem:** DS3225 de versão comprovada. A ficha DSSERVO **DS3225(Red)** consultada informa 24,5 kgf·cm a 5 V e 28 a 6,8 V; não confundir com fichas antigas ou anúncios de outra revisão. A disponibilidade/custo encontrados foram inconsistentes; por isso não integra a BOM principal. Fonte: [ficha do fabricante hospedada pela Banggood](https://myosuploads3.banggood.com/products/20220907/20220907032153DS3225datasheet.pdf).
- **Cotovelo mais barato:** MG996R pode ser ensaiado: seu bloqueio de catálogo de 9,4 kgf·cm a 4,8 V supera o alvo de 3,71 kgf·cm. A escolha principal continua DS3218 pela padronização e margem. Não trocar sem conferir massa/folga/temperatura.
- **Ombro com MG996R direto não recomendado:** o alvo de 10,90 kgf·cm excede o ponto de 9,4 kgf·cm usado nesta alimentação. Trabalhar perto do bloqueio não é solução para sustentação.
- Se o ombro aquecer ou perder posição, reduzir alcance/massa, limitar ciclo, estudar contrabalanço ou redução mecânica. Uma redução 2:1 reduz curso/velocidade na saída e acrescenta massa/atrito; não está incluída como peça já resolvida.
- A especificação “15 kg” de alguns anúncios MG996R não foi usada no cálculo. O fabricante alerta para cópias, e a [RoboCore informa que não garante a origem TowerPro de seu fornecedor](https://www.robocore.net/atuador/servo-towerpro-mg996r-metalico). Preço e nome no anúncio não validam desempenho.

## 4. Massas: geometria existente, motores e reservas

Usou-se o volume dos STL verificados da Fase 1 e densidade de PLA de **1,24 g/cm³**, conforme [ficha PLA EasyFill EF05 da 3D Fila](https://www.3dfila.com.br/downloads/PLA-EF05-REVD.pdf). Cálculo: `massa_g = volume_mm³ / 1000 × 1,24`.

Isso representa **volume integral do sólido CAD**, sem vazios de preenchimento, e serve como referência conservadora para essas peças atuais. Não é massa pesada nem massa de fatiamento. Não cobre automaticamente peças novas, suportes de impressão ou alterações geométricas; por isso foram somadas reservas específicas. Não multiplicar o peso sólido simplesmente por “30% de infill”: paredes e superfícies também consomem material.

| Peça atual | Quantidade | Volume unitário (cm³) | Massa sólida unitária (g) |
| --- | ---: | ---: | ---: |
| Base | 1 | 85,899 | 106,515 |
| Prato | 1 | 36,034 | 44,683 |
| Pedestal | 2 | 8,673 | 10,755 |
| Lateral superior | 2 | 15,137 | 18,769 |
| Espaçador superior | 2 | 2,695 | 3,342 |
| Lateral do antebraço | 2 | 13,891 | 17,225 |
| Espaçador do antebraço | 2 | 1,304 | 1,617 |
| Palma | 1 | 10,745 | 13,323 |
| Dedo fixo | 1 | 1,760 | 2,182 |
| Dedo móvel | 1 | 1,805 | 2,239 |

Total das 15 peças: **272,36 g de PLA sólido equivalente**. Cupom separado: 6,89 g. Conjuntos: braço superior impresso **44,223 g**, antebraço impresso **37,685 g**, garra impressa **17,745 g**. O custo de filamento efetivamente consumido será calculado pelo fatiador; prever inicialmente 0,35–0,50 kg com novos suportes, cupons e retrabalho, sem garantia antes do redesenho.

### Cenário de dimensionamento horizontal

Origem X no eixo do ombro; cotovelo em X=0,110 m. Para o cálculo, o DS3218 do cotovelo fica **preso ao braço superior**, com centro de massa conservador em X=0,130 m. Mesmo que seu corpo ultrapasse a posição do eixo, ele não pertence ao segmento móvel do cotovelo. Se a montagem mudar essa relação, recalcular.

| Grupo | Massa adotada (g) | X a partir do ombro (m) | Origem da estimativa |
| --- | ---: | ---: | --- |
| Braço superior e fixadores | 56,223 | 0,055 | 44,223 de CAD + 12 de fixadores |
| Apoio do cotovelo, fixo no braço superior | 28,000 | 0,110 | 10 para dois rolamentos + 18 para suporte/adaptação; reserva de projeto |
| Servo do cotovelo | 67,000 | 0,130 | 60 de catálogo + 7 de reserva para variante/acessórios |
| Antebraço e ferragens | 77,685 | 0,160 | 37,685 de CAD + 40 para eixo/hubs/colares/fixadores/cabos |
| Travessa de distribuição da palma | 12,000 | 0,210 | Peça futura, reserva de massa |
| Garra completa | 51,745 | 0,230 | 17,745 de CAD + 14 do microservo + 8 de ferragens/pads + 12 de suporte/linkagem |
| Objeto | 50,000 | 0,255 | Carga útil especificada; centro 45 mm além da extremidade do antebraço |

Massa total desses grupos, incluindo objeto: **342,653 g**. As posições dos grupos compostos são aproximações conservadoras para triagem, não centros obtidos por integração CAD. Pesar e localizar os centros reais antes de aprovar o conjunto. A reserva de 40 g do antebraço contempla aproximadamente 11 g de eixo cortado, 16 g de dois hubs e 13 g de colares/fixadores/cabos. São orçamentos de massa, não pesagens. Se os hubs/ferragens ultrapassarem as reservas, não compensar isso silenciosamente reduzindo outra massa.

Os servos de ombro e base também foram considerados: orçamento de **67 g para o DS3218 do ombro e 69 g para o MG996R da base**. O último valor é reserva acima dos 55 g do fabricante, compatível com a variação anunciada no mercado. Como são sustentados pelo conjunto proximal, não entram no torque gravitacional do ombro/cotovelo. Entram na massa centrada/estabilidade e, quando giram com o prato, na inércia de base. Para estabilidade foi creditada massa centrada de **0,400 kg**, incluindo base/prato/pedestais, esses dois motores e aproximadamente 91 g de ferragens/adaptações. O conjunto proximal completo pode pesar mais; não se creditou esse lastro adicional sem pesagem. Se seu centro se afastar do eixo, substituir a hipótese centrada por sua posição real. A fonte fora do braço não conta como lastro.

## 5. Torque e esforços

### 5.1 Ombro e cotovelo

Com `g=9,80665 m/s²`, `T=g×Σ(m×r)` e massas em kg:

```text
T_ombro = g × (0,0562232112×0,055 + 0,028×0,110 + 0,067×0,130
             +0,0776848896×0,160 + 0,012×0,210
             +0,0517446108×0,230 + 0,050×0,255)

T_cotovelo = g × (0,0776848896×0,050 + 0,012×0,100
                +0,0517446108×0,120 + 0,050×0,145)
```

| Junta | Torque estático (N·m) | Alvo com fator 2 (N·m) | Alvo (kgf·cm) | Comparação com bloqueio de catálogo |
| --- | ---: | ---: | ---: | --- |
| Ombro | 0,534297 | 1,068594 | 10,897 | DS3218: 18 kgf·cm a 5 V; estático ≈30,3% e alvo ≈60,5% do bloqueio |
| Cotovelo | 0,181851 | 0,363701 | 3,709 | DS3218: estático ≈10,3% e alvo ≈20,6% do bloqueio |

Conversão: `1 kgf·cm = 0,0980665 N·m`. A margem 2 é uma escolha preliminar, não um fator de segurança estrutural certificado nem uma simulação dinâmica. Os percentuais de bloqueio não são uma regra de capacidade contínua. Testar sustentação e ciclos na tensão prevista, sem manter o servo travado.

Sensibilidade: **20 g adicionais na garra**, em X=0,230 m, acrescentam aproximadamente **0,0451 N·m no ombro** e **0,0235 N·m no cotovelo**, antes do fator 2. Se os 67 g do servo do cotovelo forem montados no antebraço a 20 mm do eixo, acrescentam **0,0131 N·m** ao cotovelo, além de rever a distribuição das demais massas.

A estimativa anterior da Fase 1 era 0,572218/0,216237 N·m. A diferença vem da substituição de massas genéricas por volumes CAD, microservo leve e reservas explícitas. O cenário antigo permanece preservado; o novo também deve ser revisto depois de pesar as peças.

### 5.2 Base: torque de rotação, não torque de levantamento

Em eixo vertical nivelado, a gravidade provoca momento de tombamento, mas não o mesmo torque em torno de Z. Usar `T_base = I_z×α + T_atrito/cabos`.

Para uma triagem conservadora, concentrar a massa do braço superior a 110 mm, antebraço a 210 mm e garra/objeto a 262 mm, manter os demais X da tabela e acrescentar afastamento lateral de 40 mm aos grupos. Reservar ainda `0,300×0,060² kg·m²` para componentes proximais que giram. Isso dá **I_z ≈ 0,014719 kg·m²**, estimativa superior de planejamento para o envelope assumido, não tensor CAD. Essa reserva inercial não é a massa centrada usada no cálculo de tombamento: a base fixa não gira e massa próxima ao eixo contribui pouco para a inércia.

Adotar aceleração lenta `α=0,5 rad/s²` e provisão de atrito/cabos `0,05 N·m`, a medir. Com margem 2:

```text
T_base_alvo = 2 × (0,014719×0,5 + 0,05)
            = 0,114719 N·m = 1,170 kgf·cm
```

O MG996R tem margem ampla na comparação de bloqueio para esse alvo. Se a base emperrar, corrigir apoio, alinhamento e cabos; não usar torque adicional para vencer um defeito de montagem. A transmissão proposta é 1:1, com duas rodas dentadas formando **um par de engrenagens**, sem redução adicional.

### 5.3 Garra: 50 g não definem sozinhos o esforço

Hipótese: objeto rígido preso por duas faces com pads, coeficiente de atrito experimental `μ=0,30`, gravidade vertical, fator de retenção `S=2`. Esse coeficiente precisa de ensaio com o objeto real. A força normal por face deve satisfazer `2×μ×N ≥ S×m×g`:

```text
N = 2×0,050×9,80665 / (2×0,30) = 1,6344 N por face
T_garra = N×0,040 / 0,70 = 0,093397 N·m = 0,9524 kgf·cm
```

O braço efetivo de 40 mm e eficiência de 70% são hipóteses para uma transmissão 1:1; a linkagem atual ainda não existe. O fator de retenção já está incluído, não multiplicar esse resultado novamente por 2. O MG90S é candidato para esse ensaio, sem alegar que sustenta continuamente esse esforço.

Com `μ=0,15`, a demanda dobra para **1,905 kgf·cm**, acima do ponto de bloqueio de 1,8 usado na comparação: o candidato falha nessa hipótese. Priorizar pads e contato estável; se necessário, redução 2:1 ou outro microservo, contabilizando a mudança de curso e massa. O dedo pivotante não mantém faces paralelas: a área real de contato e o risco de expulsar o objeto precisam ser ensaiados.

### 5.4 Eixos, rolamentos e polímero

Para eixo maciço de Ø5 mm transmitindo o alvo do ombro, a triagem de torção é `τ_max=16T/(πd³) ≈ 43,5 MPa`. Isso não inclui flexão, entalhe de parafuso prisioneiro, fadiga nem fator do material. Preferir aço retificado identificado e hub de aperto; não usar barra roscada como superfície de rolamento.

Na base, o momento do braço é aproximadamente 0,534 N·m. Dois apoios separados por 30 mm exigem aproximadamente `M/L=17,8 N` de reação radial oposta, ou **35,6 N** com o fator 2, além das cargas axiais/peso e forças da transmissão. Verificar o rolamento comprado e suas condições de montagem; não transferir capacidade de catálogo SKF para rolamento genérico. O alojamento impresso, sua fixação e o eixo podem limitar antes das pistas de aço.

## 6. Rolamentos, eixos, acoplamentos e suportes propostos

As dimensões abaixo são **nominais de componentes a selecionar**, não medidas liberadas de alojamentos impressos. As famílias dimensionais constam do [catálogo SKF de rolamentos rígidos](https://cdn.skfmediahub.skf.com/api/public/0901d196802809de/pdf_preview_medium/0901d196802809de_pdf_preview_medium.pdf) e da [ficha SKF W 608-2Z](https://docs.rs-online.com/3ac3/A700000007154526.pdf). O material inox da segunda ficha não é exigência da BOM; usa-se a referência dimensional 8 × 22 × 7 mm. Solicitar ficha da marca efetivamente comprada.

| Conjunto | Especificação proposta | Quantidade / montagem |
| --- | --- | --- |
| Ombro | 625ZZ/625-2Z, nominal 5 × 16 × 5 mm, folga normal | 2, um em cada pedestal fixo; eixo Ø5 gira com o braço |
| Cotovelo | Mesma família 625ZZ | 2, nas laterais do braço superior; eixo Ø5 gira com antebraço |
| Base | 608ZZ/608-2Z, nominal 8 × 22 × 7 mm | 2 em cartucho vertical, aproximadamente 30 mm entre centros; resolver localização axial e tampas |
| Eixos de juntas | Aço retificado Ø5 mm | 2 tarugos de 100 mm para corte depois da montagem dimensional; não são comprimentos finais |
| Eixo da base | Aço retificado Ø8 mm | 1 tarugo de 120 mm para corte; verificar ajuste efetivo e material |
| Hubs de eixo Ø5 | Flange metálica com aperto por abraçadeira, ou prisioneiro em face plana preparada | 4: 2 por junta, um para entrada de torque e outro para fixar o conjunto móvel |
| Hubs de eixo Ø8 | Flange metálica de aperto | 2: transmissão e prato; não prender o prato só por atrito em PLA |
| Retenção axial | Colares metálicos de eixo | 4 de Ø5 e 2 de Ø8, com arruelas/calços ajustados; podem ser racionalizados depois do detalhamento |
| Horns | Horn original/compatível medido e, preferencialmente, metálico nos três servos grandes | 3, além do horn do microservo; não presumir intercambiabilidade só por contar 25 dentes |
| Pivô da garra | Parafuso M3 e bucha metálica lisa, ID nominal ≈3,2 mm, OD ≈5 mm | 1 bucha; comprimento deve limitar aperto sem travar o dedo. Cotas de fabricação pendentes |
| Contato da garra | Borracha/silicone aderente | 2 pads, um por face; espessura e adesivo a ensaiar |

**Princípio de montagem:** cada eixo estrutural é apoiado nos rolamentos e transmite torque ao segmento móvel por hub. O servo atua por horn e adaptador; seu eixo não deve receber sozinho o peso do braço. Os corpos dos servos são fixados ao segmento proximal correspondente: base fixa, prato/pedestais para ombro, braço superior para cotovelo, palma para garra.

No apoio da base, prever um rolamento localizador com ombros/retenção dos anéis e outro com possibilidade de acomodar a montagem, evitando pré-carga acidental pela impressão. O peso deve passar por colar/ombro, anel interno, rolamento, anel externo e cartucho. Calços devem encostar no anel correto, nunca apertar simultaneamente pista interna, externa e blindagem. Confirmar a capacidade axial do produto escolhido.

### Peças de adaptação que ainda precisam ser projetadas

1. **Três suportes de servo padrão e um de microservo**, com acesso às abas, saída de cabo e possibilidade de ajuste de alinhamento. O suporte do cotovelo fica externo: não tentar colocar o servo no vão de 15 mm.
2. **Um cartucho de base com duas tampas**, alojamentos dos 608 e fixação atravessante. Reforçar a região ligada à base.
3. **Quatro regiões de alojamento/retentores para os 625**, integradas a pedestais/elos, com ombro e tampa ou encaixe dividido. Parede de 5 mm não comporta largura de 5 mm do rolamento mais retenção robusta sem ressalto local.
4. **Dois adaptadores de horn para hub Ø5**, duas uniões hub–segmento e uma união hub–prato, sem estria impressa. Hubs comerciais podem exigir alargar espaçamentos; medir antes.
5. **Um par de engrenagens de base 1:1**, uma presa ao horn do MG996R e outra ao hub Ø8; eixo do servo paralelo e deslocado do eixo central. A transmissão permite servo ao lado do cartucho, sem empilhar o servo inteiro sob os rolamentos. Módulo, número de dentes, folga e afastamento ficam para o CAD medido. Rodas impressas estão incluídas na reserva de filamento, não são peças existentes.
6. **Uma travessa da palma e uma linkagem da garra**, com pads e batentes. Reforçar o boss do dedo antes de alojar a bucha de aproximadamente Ø5; 8 mm de largura atual deixa pouca borda.

Os esforços radiais da engrenagem sobre o servo da base também precisam de verificação. Preferir baixa aceleração, bom alinhamento e engrenamento livre; se a saída do servo não aceitar esse esforço, adicionar apoio próprio à transmissão e atualizar a BOM. Não montar os seis rolamentos em furos do CAD atual por simples escala.

## 7. Parafusos e consumíveis mecânicos

Usar parafusos métricos de aço, preferencialmente Allen com cabeça cilíndrica/abaulada e arruela; evitar escareado comprimindo PLA. Porcas autotravantes em juntas sujeitas a vibração. Não apertar até deformar o polímero; retenção do pivô não pode impedir movimento.

Comprimentos abaixo são **candidatos derivados das espessuras atuais**, medidos sob a cabeça. Conferir `L = pilha real + arruelas + porca + 1–2 filetes expostos`, sem invadir partes móveis. Roscas de horn e parafusos centrais do servo seguem a peça original, não esta lista genérica.

| Uso | Quantidade | Parafuso candidato / justificativa |
| --- | ---: | --- |
| Espaçadores superiores | 2 | M3 × 50; pilha atual 5+31+5 = 41 mm, antes de arruelas/porca |
| Espaçadores do antebraço | 2 | M3 × 35; pilha atual 5+15+5 = 25 mm |
| Pedestais no prato | 4 | M3 × 20; pilha 5+6 = 11 mm |
| Palma no antebraço atual | 1 + 1 | M3 × 20 e M5 × 20; pilha 5+0,5+5 mm. Redimensionar na travessa proposta |
| Dedo fixo | 2 | M3 × 16, dois pontos impedem rotação |
| Dedo móvel | 1 | M3 × 20, com bucha e arruelas; rosca não é superfície de deslizamento |
| Base em placa de madeira de 15 mm | 4 | M4 × 30 com arruelas largas e porcas; pilha 6+15 = 21 mm |
| Abas dos três servos grandes | Reserva de 12 | M3 × 10/16, somente se os furos medidos permitirem; usar ilhoses/calços do kit quando aplicáveis |
| Abas do microservo | Reserva de 2 | M2 × 10/12, ou fixador especificado pelo fabricante; não forçar M3 |
| Tampas, cartucho, adaptadores e reforços | Reserva de 16–24 | M3 × 10/16/20, a fechar após desenho |

Compra inicial sugerida do lote mecânico: **24 M3×10, 16 M3×16, 20 M3×20, 2 M3×35, 2 M3×50; 60 porcas M3 e 120 arruelas M3; 4 M4×30, 4 porcas M4 e 8 arruelas largas; 1 M5×20, 1 porca M5 e 2 arruelas M5; 4 M2×10 e 4 M2×12 com 8 porcas/16 arruelas**. São peças de montagem e reservas, não contagem de furos já modelados. Se o kit de servo/hub já trouxer fixadores adequados, descontá-los. Colares e hubs devem vir com seus próprios parafusos de aperto.

## 8. Fixação e tombamento

Base atual: borda a `b=0,060 m`. Para cada grupo da tabela de massas, separar o momento em torno da borda:

```text
M_tomba = g × Σ[m × max(x−b, 0)] = 0,335437 N·m
M_restaura = g × [0,400×b + Σ(m × max(b−x, 0))] = 0,238116 N·m
Razão = M_restaura/M_tomba = 0,710 < 1
```

Logo, **o braço pode tombar livremente no cenário adotado**, mesmo sem aceleração. Para razão estática 1,5, seria necessária massa centrada total de **0,850 kg**, aproximadamente **0,450 kg extra** além dos 0,400 kg creditados. Não é recomendável resolver isso apenas imprimindo plástico maciço.

**Solução principal:** placa de compensado de aproximadamente **240 × 240 × 15 mm**, presa à bancada por **dois sargentos**, e base impressa presa à placa por quatro M4 com arruelas largas. A placa não precisa caber na impressora. Distribuir os sargentos e as zonas de aperto para reagir a momentos em qualquer direção de giro, sem usar um único ponto como articulação; adicionar calços antideslizantes. Se a bancada permitir furação, parafusos atravessantes são alternativa aos sargentos.

Os centros dos quatro furos atuais ficam em `X/Y=±48 mm`, espaçamento 96 mm. Como referência de reação, um momento de projeto de aproximadamente 1,069 N·m dividido por 0,096 m implica um casal de forças de **11,1 N entre linhas de fixação**. Isso não dimensiona sozinho fixadores, madeira, arrancamento, arruelas ou grampos: verificar assentamento, bordas, resistência e efeitos de impacto.

A placa mais larga melhora o apoio, mas não considerar a estrutura autoportante sem novo cálculo com a massa/centro reais. Ensaiar estabilidade em todos os azimutes previstos. Com potência desligada, o braço pode baixar pela gravidade: apoiar os elos durante manutenção e posicionar um berço sob a carga para o ensaio de corte.

## 9. Alimentação e componentes eletrônicos reservados

Propor **fonte regulada de 5 V / 10 A contínuos**, protegida, com cabos/conectores de saída capazes de transportar a corrente. A potência nominal é 50 W. Não ligar os servos ao regulador da placa ESP32 ou à protoboard. Preferir fonte externa fechada, mantendo rede elétrica fora do braço. O anúncio de uma fonte com plug P4 não comprova que esse conector/cabo suporta 10 A: exigir especificação e medir queda de tensão.

Orçamento de corrente de triagem:

| Grupo | Corrente usada | Natureza do dado |
| --- | ---: | --- |
| 2 DS3218 | 2 × 1,8 A | Bloqueio a 5 V na ficha DSSERVO |
| MG996R | 2,5 A | Provisão de projeto acima dos 1,4 A publicados; cobre incerteza da unidade, sem garantir limite superior |
| MG90S | 1,0 A | Provisão, não corrente medida nem dado do fabricante |
| Total reservado | 7,1 A | Margem da fonte de 10 A a validar em partidas simultâneas |

O ESP32 fica inicialmente em **alimentação USB de 5 V separada**, com terra comum e ligação planejada para não haver retorno de potência entre fontes. Isso simplifica testes sem implementar controle. Confirmar a placa e a forma de alimentação antes de conectá-la. Não presumir que todo servo reconhece 3,3 V como nível alto; reservar um buffer **74AHCT125** alimentado em 5 V, com interface de habilitação definida depois. Referência de compatibilidade elétrica: [Texas Instruments — SN74AHCT125](https://www.ti.com/product/SN74AHCT125).

Prever distribuição em estrela, fusível geral e ramais, chave de corte com **capacidade DC declarada ≥10 A**, conectores travados e alívio de tração. Reserva para fusível geral de 7,5 A e ramais de 3 A nos servos grandes/1 A no microservo, a ajustar conforme cabos, curvas dos fusíveis e correntes medidas. Fusível protege cabeamento; não substitui limitação de torque/corrente ou parada de movimento.

Sugestão inicial de chicote: alimentação principal em cobre de 1,5 mm², até 0,5 m por condutor; ramais curtos em 0,5 mm², até aproximadamente 0,3 m por condutor, com conectores compatíveis com a corrente. Conferir tensão mínima de 4,8 V nos servos em movimento e ajustar comprimento/seção se necessário. Reservar dois capacitores de 1.000–2.200 µF/10 V e desacoplamento cerâmico; capacitor não compensa fonte insuficiente. PCA9685 não é obrigatório para quatro canais e não está na BOM principal.

## 10. Lista de materiais e orçamento no Brasil

**Valores em reais, sem frete, pesquisa em 11/11/2026.** `P` = faixa de planejamento ancorada em preço público observado; `E` = provisão de engenharia ainda sem cotação específica. As faixas não são ofertas firmes nem garantia de estoque/autenticidade. Nos itens E, validar preço, conteúdo e disponibilidade antes de comprar. A faixa contempla varejo em pequenas quantidades, não inclui remuneração do trabalho, instrumentos do laboratório, energia ou impressão terceirizada.

| Item | Qtd. | Especificação de compra proposta | R$/un. | Subtotal R$ | Base |
| --- | ---: | --- | ---: | ---: | --- |
| DS3218 | 2 | Posicional 180°, versão documentada; ombro/cotovelo | 100–150 | 200–300 | P1 |
| MG996R | 1 | Posicional; base; verificar procedência | 45–70 | 45–70 | P2 |
| MG90S | 1 | Posicional; garra; confirmar 5 V na unidade | 30–50 | 30–50 | P2 |
| Horns metálicos | 3 | Compatíveis com os três servos grandes, com parafusos centrais corretos | 15–25 | 45–75 | E |
| 625ZZ | 4 | 5 × 16 × 5 mm, folga normal, marca identificada | 5–15 | 20–60 | P3 |
| 608ZZ | 2 | 8 × 22 × 7 mm, marca identificada | 7–15 | 14–30 | E; nominal em P4 |
| Eixos Ø5 | 2 | Aço retificado, tarugo de 100 mm | 12–20 | 24–40 | E |
| Eixo Ø8 | 1 | Aço retificado, tarugo de 120 mm | 15–25 | 15–25 | E |
| Hubs flangeados Ø5 | 4 | Metálicos, aperto adequado ao torque | 15–30 | 60–120 | E |
| Hubs flangeados Ø8 | 2 | Metálicos, prato e transmissão | 15–30 | 30–60 | E |
| Colares Ø5 | 4 | Retenção axial | 6–12 | 24–48 | E |
| Colares Ø8 | 2 | Retenção axial | 8–15 | 16–30 | E |
| Bucha do dedo | 1 | Tubo liso metálico a cortar/ajustar após medir | 5–10 | 5–10 | E; usinagem especial fora da faixa |
| Lote de parafusos/porcas/arruelas | 1 | Quantidades da seção 7, incluindo reservas | 50–80 | 50–80 | E |
| Placa de compensado | 1 | Aproximadamente 240 × 240 × 15 mm | 20–40 | 20–40 | E |
| Sargentos | 2 | Abertura compatível com bancada e placa | 20–35 | 40–70 | E |
| Pads da garra | 1 par | Borracha/silicone com fixação | 5–10 | 5–10 | E |
| Filamento PLA | 1 rolo | 1 kg, 1,75 mm; inclui reserva para peças futuras/cuponagem | 75–110 | 75–110 | P5 |
| ESP32 DevKit | 1 | ESP32 clássico com USB e regulador; confirmar variante/pinagem | 43–65 | 43–65 | P6 |
| Fonte USB da lógica | 1 | 5 V, 2 A, externa e protegida | 25–40 | 25–40 | E |
| Cabo USB de dados | 1 | Compatível com a placa | 10–20 | 10–20 | E |
| Fonte dos servos | 1 | 5 V, 10 A contínuos, saída/conector adequados | 90–140 | 90–140 | P7 |
| Chave de corte | 1 | Capacidade DC ≥10 A comprovada | 15–30 | 15–30 | E |
| Distribuição e fusíveis | 1 lote | 1 geral + 4 ramais, porta-fusíveis, fusíveis e reservas | 25–45 | 25–45 | E |
| Chicote e conectores | 1 lote | Principal 1,5 mm², ramais 0,5 mm², sinal e terminais | 25–45 | 25–45 | E |
| Capacitores | 1 lote | 2 eletrolíticos e 4 cerâmicos de desacoplamento | 5–10 | 5–10 | E |
| Buffer de sinal | 1 conjunto | 74AHCT125, soquete/adaptação e desacoplamento | 10–20 | 10–20 | E |
| Testador de servo | 1 | Posicional, ajuste manual e alimentação compatível | 15–25 | 15–25 | P2 |
| Placa de conexão/caixa da lógica | 1 conjunto | Sem potência dos servos em trilhas de protótipo frágeis | 15–30 | 15–30 | E |
| **Total** | | **Rolo inteiro e reservas incluídos** | | **996–1.698** | |

As 15 peças estruturais atuais e as adaptações propostas da seção 6 serão impressas; o custo de material está na linha do filamento, sem duplicação. O testador é instrumento de comissionamento, não parte obrigatória do produto final. Não ligar automaticamente os quatro motores em potência através de um testador cujas trilhas não tenham corrente nominal adequada; testar um por vez inicialmente.

### Evidências de preço e disponibilidade

- **P1:** [Brasília Modelismo — DS3218MG](https://brasiliamodelismo.com.br/produtos/servo-digital-ds-3218mg-20kg-48v-a-6-8v-metal-gear-1opjn/?entry_path=category), **R$ 97,01**, com indicação de última unidade. A quantidade de dois não foi confirmada; faixa da BOM é provisão para recotação. O anúncio informa 19 kgf·cm a 5 V, mas a triagem técnica usa os 18 da ficha DSSERVO correspondente; exigir identificação da versão.
- **P2:** [Casa da Robótica — servos](https://www.casadarobotica.com/robotica/servos): MG996R **R$ 46,99**, MG90S posicional **R$ 34,99** e testador **R$ 14,99**. Valores anunciados sem desconto à vista. O torque comercial do anúncio não foi aceito como especificação técnica; confirmar versão/estoque/procedência.
- **P3:** [Saravati — 625ZZ](https://www.saravati.com.br/rolamento-625zz-5x16x5mm-blindagem-de-aco.html), **R$ 4,99**; [Daaz — 625ZZ NSK C3](https://www.daazrolamentos.com/rolamento-625zzc3-nsk-5-x-16-x-5), **R$ 13,61**, última unidade. A oferta C3 é referência de preço, **não substituição automática** da folga normal desejada.
- **P4:** [Impacto CNC — 608ZZ](https://www.impactocnc.com/produto/rolamento-608zz-8x22x7mm.html), produto nominal 8 × 22 × 7 mm localizado; **preço não confirmado na extração**. Faixa E da BOM precisa ser cotada.
- **P5:** [3D Fila — catálogo](https://3dfila.com.br/shop-2/), PLA anunciado a partir de **R$ 74,90 no Pix**. O produto possui variantes: confirmar seleção de **1 kg**, material e preço antes do pedido. A BOM usa uma faixa de orçamento, não afirma que toda variante custa esse valor.
- **P6:** [RoboCore — placas de desenvolvimento](https://www.robocore.net/development-boards), ESP32 WiFi + Bluetooth **R$ 42,90**; [página do produto](https://www.robocore.net/wifi/esp32-wifi-bluetooth). Confirmar placa entregue, conector USB e disponibilidade.
- **P7:** [Copel Eletrônica — fonte MXT 5 V/10 A](https://www.copeleletronica.com.br/p-fonte-5v-10a-chaveada-50w-22682), **R$ 87,00**, anunciada como pronta entrega e com plug P4. É referência de orçamento: aprovação depende de corrente contínua real e especificação do cabo/conector. Não comprar apenas pelo rótulo “10 A”.

Para a alternativa DS3225, a [Fabmodelismo](https://www.fabmodelismo.com.br/produto/pecas-e-acessorios/servos-acessorios/8810-servo-digital-25kg-metal-gear-waterproof-com-braco-aluminio-ds3225mg) mostrava **R$ 119,99 e aviso de indisponibilidade**, enquanto uma [oferta da Alfa Hobby](https://www.alfahobby.com.br/loja/eletronica/servos/dsservo-servo-rc-a-prova-d-agua-ds3218-20kg-ds3225-2-76428-496/) mostrava **R$ 819,98**. Não tratar o menor valor sem estoque como compra disponível, nem produtos de revisão diferente como equivalentes.

**Economia por etapas:** primeiro adquirir/emprestar um servo de cada família, os rolamentos e amostras de fixadores para medição. Confirmar dois DS3218 da mesma versão antes da compra do restante. Reutilizar o horn metálico fornecido quando houver; reaproveitar filamento/fonte/ESP32 do laboratório reduz desembolso. Não eliminar rolamentos, retenções e ancoragem para reduzir a conta. Se forem necessárias flanges usinadas ou marcas industriais de rolamento, recotar: as provisões de ferragens não garantem esses preços.

## 11. Medições físicas obrigatórias

Registrar modelo/lote, instrumento/resolução, data, operador, foto e croqui com origem/eixos. Valores de catálogo servem para reservar envelope; os encaixes dependem da unidade. Nenhum padrão de furação comercial foi gravado no CAD nesta fase.

| Componente | Medir/confirmar antes de finalizar |
| --- | --- |
| Cada servo | Corpo completo com ressaltos, tampa, abas, alturas, envelope do conector e curvatura de cabo |
| Abas | Distâncias entre centros X/Y, diâmetros, espessura, posição em relação ao corpo, ilhoses e cabeça do parafuso |
| Eixo do servo | Posição do centro em três eixos, altura útil, ressalto e espaço de montagem do horn |
| Horn | Estria e compatibilidade real, espessura, offsets, furos/roscas, parafuso central e profundidade útil |
| Rolamentos | ID/OD/largura da unidade, raios/chanfros, tipo de blindagem, folga, marca e capacidade declarada |
| Eixos/hubs/colares | Diâmetro real em vários pontos, retidão, comprimento de engate, face de aperto, flange, espessura e furação |
| Fixadores | Diâmetro da cabeça, altura, comprimento sob cabeça, região roscada, porca/arruela e acesso da ferramenta |
| Pivô da garra | Bucha e folga livre sob aperto, curso e alinhamento das faces/pads |
| Impressão | Cupom de furos e alojamentos, erro XY/Z, ovalização, pé de elefante e contração após resfriamento |
| Massa/centro | Peças fatiadas, peças prontas e subconjuntos com motores/horns/cabos/ferragens |
| Bancada/base | Espessura, região de grampeamento, coplanaridade, aderência e espaço para cabo/eletrônica |
| Servo em ensaio | Curso efetivo sem batente, sentido, folga, corrente, tensão mínima, aquecimento e posição sob carga |

O cupom atual só testa passagem de pinos de aproximadamente 5 mm. Criar depois da aprovação cupons específicos para alojamentos de 16/22 mm, bucha, nut pockets e interfaces de servo. Não aplicar automaticamente `+0,4 mm` a um alojamento de rolamento: o tipo de retenção e o ajuste precisam ser definidos e ensaiados.

## 12. Melhorias propostas para impressão e resistência

Estas são propostas para a próxima revisão; não alteram a liberação de impressão.

| Melhoria | Justificativa e limite |
| --- | --- |
| Preservar faces largas dos elos na mesa | Favorece continuidade de material no plano principal de flexão; avaliar também torção e ligação entre camadas |
| Adicionar nervuras/raios aos pedestais | Reduz concentração na raiz do L; revisar a orientação ou dividir pedestal em placas aparafusadas para reduzir esforço entre camadas |
| Bosses locais com tampas de rolamento | Reforço onde necessário, sem engrossar o elo inteiro; permitir desmontagem sem forçar o rolamento no PLA |
| Travessa simétrica para palma | Distribui torque entre as duas placas; massa extra de 12 g foi reservada, mas deve ser pesada |
| Reforçar o pivô do dedo | Evita borda muito fina ao introduzir bucha; manter parafuso apoiado em metal e rotação livre |
| Reduzir massa distal primeiro | Pequena redução na garra/antebraço beneficia ombro e cotovelo; não retirar material ao redor de furos/apoios |
| Revisar base maciça | A base atual equivale a 106,5 g de PLA sólido; usar placa externa e nervuras pode economizar material, mas exige nova massa de estabilidade |
| Janelas arredondadas após ensaio | Só em regiões de baixo esforço, preservando caminhos contínuos entre pivôs e fixadores; não recortar antes de verificar deflexão |
| Encaixes divididos e porcas acessíveis | Reduz suporte de impressão, facilita ajuste e troca de peças; não imprimir estria de servo |
| Evitar cabos passando entre juntas | Criar pontos de alívio e canais abertos longe de pivôs, com acesso para manutenção |

Perfil **experimental** de partida, após aprovação: bico calibrado de 0,4 mm, camada de aproximadamente 0,20 mm, 4–5 paredes nos elos, 5–6 junto a bosses/pedestais, 5–6 camadas de topo/fundo e preenchimento de 25–35%, com reforço local nos pontos de aperto. Esses números são propostas de ensaio, não resistência garantida. Em peças de 5 mm, paredes e tampas já ocupam grande fração do volume. Inspecionar o fatiamento antes de definir porcentagens finais.

A documentação da [Prusa sobre paredes e perímetros](https://help.prusa3d.com/article/layers-and-perimeters_1748) recomenda considerar paredes para resistência, em vez de depender apenas de infill. PLA comum é uma opção inicial para cupons e estrutura em ambiente interno controlado; não usar formulação decorativa/silk sem dados mecânicos. PETG pode ser avaliado nos suportes sujeitos a impacto/temperatura, mas requer novo perfil, ajuste e ensaio de rigidez; não presumir que será mais rígido. Referência de processamento: [Prusa — PETG](https://help.prusa3d.com/article/petg_2059?product=mmu3).

Na Ender 3 original, verificar condição do hotend/PTFE e limites reais antes de escolher um perfil de maior temperatura. Não adotar automaticamente temperaturas de outra impressora. Manter todas as peças revisadas dentro de **220 × 220 × 250 mm**, reservando margem para brim/grampos; o verificador atual usa 210 × 210 mm em XY. Preferir mudanças de orientação/divisão das peças que economizem suportes sem enfraquecer a junta.

## 13. Verificações realizadas e próximos critérios de aprovação

### Realizadas nesta fase

- Revisão estática do CAD e dos relatórios existentes; volumes lidos de `build/verification.json`, cujo estado é `passed`.
- Recálculo de massas, torques dos quatro movimentos, estabilidade e soma da BOM por Python, sem alterar os modelos.
- Verificação final aprovada: execução do trecho Python deste documento, 29 linhas da BOM conferidas por quantidade × preço, totais e reserva de 20% corretos. Os hashes SHA-256 dos quatro arquivos SCAD permaneceram iguais aos registrados antes da redação. Evidência local regenerável desta sessão: `build/fase2-verificacao.json` (ignorada pelo Git).
- Reexecução de `python scripts/torque.py`: cenário histórico preservado e resultado da Fase 1 reproduzido. Esse script não representa a nova distribuição detalhada de massas; as equações e o trecho reproduzível abaixo são a referência da Fase 2.
- Conferência das fontes técnicas e preços, com divergências/indisponibilidades registradas.
- Nenhum teste de bancada, fatiamento novo, impressão, montagem, ensaio de torque ou validação elétrica foi realizado.

Para reproduzir os principais cálculos desta fase, executar o trecho abaixo com Python 3; ele não depende de bibliotecas externas. Os números completos de massa são derivados dos volumes documentados acima.

```python
g = 9.80665
# massa kg, x m a partir do ombro, pertence ao segmento do cotovelo?
rows = [
    (0.0562232112, 0.055, False),
    (0.028,        0.110, False),
    (0.067,        0.130, False),
    (0.0776848896, 0.160, True),
    (0.012,        0.210, True),
    (0.0517446108, 0.230, True),
    (0.050,        0.255, True),
]
shoulder = g * sum(m*x for m, x, distal in rows)
elbow = g * sum(m*(x-0.110) for m, x, distal in rows if distal)
b = 0.060
overturn = g * sum(m*max(x-b, 0) for m, x, distal in rows)
restore = g * (0.400*b + sum(m*max(b-x, 0) for m, x, distal in rows))
required_centered = (1.5*overturn/g - sum(m*max(b-x, 0) for m,x,d in rows))/b
r_bound = [0.110, 0.110, 0.130, 0.210, 0.210, 0.262, 0.262]
inertia = sum(m*(r*r+0.040**2) for (m,x,d),r in zip(rows,r_bound)) + 0.300*0.060**2
base_target = 2 * (inertia*0.5 + 0.05)
normal = 2*0.050*g/(2*0.30)
gripper_target = normal*0.040/0.70
print('Ombro/cotovelo estaticos Nm:', shoulder, elbow)
print('Alvos com fator 2 Nm:', 2*shoulder, 2*elbow)
print('Razao estabilidade / massa centrada necessaria kg:', restore/overturn, required_centered)
print('Base / garra alvo Nm:', base_target, gripper_target)
```

### Antes de liberar uma revisão para impressão

1. Aprovar a seleção e o teto de orçamento; confirmar duas unidades iguais de DS3218 e a especificação de alimentação do microservo.
2. Medir os componentes recebidos, inclusive interfaces e massas. Aprovar a solução de altura da base, transmissão e posição dos motores.
3. Redesenhar suportes, alojamentos, retenções, travessa e linkagem; revisar torque com as novas massas e comprimentos. Verificar curso, cabos e acesso a ferramentas em todas as poses.
4. Rodar novamente `python scripts/verify.py` no CAD revisado e inspecionar o fatiamento. Aprovar primeiro cupons e uma junta, não o conjunto completo.
5. Após aprovação específica, ensaiar uma junta apoiada: movimento sem carga, depois 10/25/50 g na posição prevista, corrente/tensão/temperatura e deflexão. Propor inicialmente movimentos lentos e pausas curtas; aumentar o tempo de sustentação até o ciclo de trabalho acadêmico acordado, interrompendo se houver aquecimento progressivo, perda de posição, trinca ou corrente anormal.
6. Como metas iniciais de avaliação, a confirmar pelo usuário: 20 ciclos com 50 g, sem soltar fixadores, sem trincas/deslizamento e sem crescimento de folga; registrar desvio de posição e deflexão na ponta. Não chamar isso de vida útil ou capacidade certificada.

**Conclusão de engenharia:** a seleção proposta é plausível para ensaios de um braço lento com carga de 50 g, mas a base, as transmissões e os encaixes ainda exigem projeto medido. A estrutura continua sem aprovação para impressão definitiva.
