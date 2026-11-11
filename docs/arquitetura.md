# Arquitetura e decisões

## Fronteiras do projeto

```text
cad/main.scad ── parameters.scad
             ├─ lib/parts.scad       sólidos isolados
             └─ lib/assembly.scad    transformações e poses
scripts/verify.py ── OpenSCAD ── build/{STL,PNG,CSG,logs,verification.json}
docs/load_scenario.json ── scripts/torque.py ── build/torque.json

FUTURO:
celular / web ── API local ── ESP32 / firmware
                              ├─ validação e limites por eixo
                              ├─ planejador/interpolador + sequenciador
                              ├─ armazenamento versionado
                              └─ acionamento de quatro servos
fonte de servos ── proteção/corte ── atuadores
regulador lógico ── ESP32 (terra comum com acionamento)
```

O CAD não depende do software embarcado. Dimensões físicas e calibração futura serão explicitamente versionadas; ângulos de visualização não são comandos PWM. O script de torque usa um cenário independente e declarado: ao alterar comprimento no CAD, atualizar também o cenário, convertendo mm para m.

## Decisões mecânicas

| Decisão | Motivo e consequência |
| --- | --- |
| Dois elos de 110 e 100 mm entre eixos | Atingir cerca de 30 cm com base e garra; reduzir torque reduzindo alcance continua possível |
| Duas placas por elo e dois espaçadores | Peças simples, faces largas na mesa, substituição individual; parafusos atravessantes precisam unir as placas aos espaçadores |
| Placas externas no braço, internas no antebraço | Cotovelo intercalado com eixo comum; folgas axiais precisam de arruelas/buchas reais |
| Ombro entre dois pedestais | Apoio nos dois lados; servo deve transmitir torque, sem ser o único apoio de carga |
| Base quadrada ancorável e prato giratório | Separar ancoragem de rotação; o vão de 4 mm é reserva conceitual, não rolamento projetado |
| Garra com dedo fixo e dedo móvel | Menos peças; falta definir servo, acoplamento/linkagem e batentes; a abertura geométrica não equivale a força de preensão |
| Palma presa por dois pontos numa placa do antebraço | Não cria quinto movimento; montagem lateral introduz torção e deve ser revista ao definir atuador |
| Furos de passagem, sem rosca impressa | Facilita ajuste e troca; arruelas/porcas ou insertos medidos serão acrescentados depois |
| Sem recortes agressivos de alívio nesta versão | Primeiro validar caminho de carga; reduzir massa distal depois de medir rigidez |

A montagem mostra pinos cinza apenas como referências. Não há parafusos, rolamentos, servos, porcas ou arruelas completos na cena. O prato parece suspenso: o apoio independente que ocupará esse vão ainda precisa ser selecionado. A vista explodida é didática, não define comprimentos de fixadores nem sequência executável de montagem.

## Software futuro — sem implementação

`firmware/` receberá o projeto PlatformIO depois da escolha da placa. Separar domínio de movimento, drivers, armazenamento e transporte. Definir máquina de estados (inativo, manual, sequência, falha), cancelamento, tempo máximo de comando, limites calibrados e formato versionado de poses. Evitar movimentos bloqueantes e validação apenas no cliente.

`web/` receberá a interface responsiva. A API deverá informar estado confirmado pelo ESP32; prever perda de comunicação, rejeição de comandos e parada. A seleção entre AP local/STA e HTTP/WebSocket fica para a etapa de controle. Não há pinagem, dependência, endpoint nem configuração PlatformIO fictícios nesta etapa.
