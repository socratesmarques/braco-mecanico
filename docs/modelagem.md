# Visualização, parâmetros e exportação

## Arquivos e convenções

Abra `cad/main.scad`, que inclui os parâmetros, sólidos e montagem. Não abrir `parts.scad` isoladamente: ele depende dos parâmetros. CAD em mm; rotações em graus. Na montagem global Z é vertical; as juntas de ombro/cotovelo têm eixo transversal. Na definição dos elos, X vai entre os centros, Y é a largura e Z a espessura. A montagem transforma esse sistema local.

`part="assembly"` mostra o conjunto, `"exploded"` afasta peças e os demais nomes selecionam peças na orientação de exportação. `show_hardware=false` oculta pinos ilustrativos na montagem; peças isoladas nunca incluem pinos. Cores: azul = elos, laranja = prato/espaçadores/palma, cinza escuro = base/pedestais/dedos, cinza claro = referências de pinos.

| Parâmetros | Função e cuidado |
| --- | --- |
| `upper_length`, `fore_length` | Comprimentos entre eixos, não extensão externa total |
| `base_size`, `base_thickness` | Envelope e espessura da base; recalcular estabilidade |
| `turntable_d`, `turntable_thickness`, `base_support_gap` | Prato e espaço reservado para apoio ainda indefinido |
| `shoulder_height` | Altura do eixo a partir do topo do prato |
| `plate_width`, `plate_thickness` | Seções dos elos e peças associadas; alterar exige reavaliar rigidez |
| `upper_offset`, `fore_offset`, `pedestal_offset` | Metade da separação entre centros dos apoios/placas |
| `spacer_width`, `spacer_depth` | Seção dos espaçadores; comprimento derivado da distância entre faces internas |
| `pin_nominal_d`, `bolt_nominal_d`, `anchor_nominal_d` | Diâmetros candidatos genéricos, não medidas de servo |
| `hole_clearance_d` | Acréscimo diametral de todos os furos genéricos; padrão experimental 0,4 mm |
| `axial_clearance` | Afastamento de 0,5 mm na montagem da palma; requer arruela/espaçador real |
| `palm_*`, `finger_*`, `gripper_mount_pitch` | Dimensões e pontos de fixação da garra conceitual |
| `base_angle`, `shoulder_angle`, `elbow_angle`, `gripper_angle` | Somente pose; não representam calibração ou limites seguros |
| `servo_*`, `bearing_*` | `undef`: dados ainda desconhecidos, sem geração de encaixe nesta versão |
| `bed`, `bed_margin` | Envelope e margem de referência; o verificador mantém a Ender 3 fixa independentemente desses valores |

O acréscimo de 0,4 mm é no **diâmetro**: folga radial nominal de 0,2 mm. É hipótese de passagem, não tolerância garantida. O cupom tem quatro furos, da esquerda para a direita (X crescente): diâmetro de pino + 0,0 / 0,2 / 0,4 / 0,6 mm. No padrão: 5,0 / 5,2 / 5,4 / 5,6 mm. O cupom não recebe o acréscimo global, pois compara folgas distintas.

As assertions cobrem apenas algumas relações geométricas. Mudanças grandes podem exigir nova topologia. É preciso renderizar novamente, inspecionar o conjunto e fatiar as peças; passar nas assertions não demonstra compatibilidade mecânica completa.

## OpenSCAD gráfico

1. Alterar `part` em `main.scad` ou no Customizer. F5 para prévia, arrastar para orbitar e usar Zoom to Fit.
2. Para pose vertical, usar `shoulder_angle=90`, `elbow_angle=0`; para horizontal, ambos 0. Essas vistas ajudam a estudar geometria e esforço, não são autorização de movimento.
3. Selecionar uma peça. F6 faz a renderização sólida; verificar o console.
4. Usar File → Export → Export as STL. Nomear pelo seletor e revisão. Nunca exportar o conjunto para impressão: peças encostadas podem se unir e referências não são peças fabricáveis.

## Linha de comando reproduzível

Na raiz, `python scripts/verify.py` exporta os 11 tipos (10 estruturais e o cupom), verifica malhas e uma variante dimensional, testa entradas inválidas e produz quatro imagens. A lista de quantidades está em `docs/componentes.md`. Em Windows, o script prefere a instalação padrão `openscad.com` quando não encontra o programa no PATH; esse executável permite capturar a saída do console.

Prefira o verificador para exportar no PowerShell 5.1, cuja passagem de aspas a programas nativos pode variar. Para exportação individual com dimensões alternativas, salve e execute o exemplo abaixo como arquivo Python na raiz; assim as definições são passadas como argumentos separados:

```python
from pathlib import Path
import subprocess
Path("build").mkdir(exist_ok=True)
subprocess.run([
    r"C:\Program Files\OpenSCAD\openscad.com",  # no Linux/macOS, caminho local
    "-o", "build/upper_link.stl",
    "-D", 'part="upper_link"', "-D", "upper_length=120",
    "cad/main.scad",
], check=True)
```

As opções `-o` e `-D` seguem a [documentação de linha de comando do OpenSCAD](https://files.openscad.org/documentation/manual/Using_OpenSCAD_in_a_command_line_environment.html). O próprio verificador também examina mensagens ERROR/WARNING porque saída do processo isoladamente pode não detectar todas as falhas do OpenSCAD.

Em ambiente sem suporte gráfico, `--skip-images` executa malhas/CSG sem PNG e registra essa limitação; a inspeção visual ainda precisa ocorrer em outra máquina. A exportação de cada peça tem timeout de 120 segundos.

## Preparação para ensaio de impressão

Todas as peças isoladas saem com Z mínimo zero. As placas ficam deitadas, espaçadores em pé com furo vertical e pedestais apoiados no pé. **Orientação geométrica não significa orientação estrutural aprovada**: o pedestal precisa de atenção à parede, furo horizontal, camadas e acesso ao fixador. Avaliar rotação e suporte no fatiador antes de imprimir.

Para um primeiro cupom, registrar material, marca/lote, bico, camada, fluxo, temperaturas, velocidade, paredes, preenchimento, orientação e acabamento. Usar o perfil já calibrado da impressora/material. Medir furos e distâncias externas após resfriamento, conferir encaixe livre sem forçar e só então ajustar folgas. Não definir temperatura universal nem assumir compensação de contração constante.

As maiores peças são base de 120 × 120 mm e elo superior com 134 mm de comprimento externo. O verificador reserva 5 mm por lado em XY. Isso não verifica grampos, nivelamento, brim escolhido ou altura de suporte no fatiador. Fatiar cada peça separada, conferir preview de todas as camadas, paredes junto aos furos e quantidade de material antes de qualquer ensaio.
