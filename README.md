### 👤 Identificação do Candidato

- **Nome completo: Elilúcio Teixeira Félix Filho**  
- **GitHub: Elilucio7**  

---

## 1️⃣ Visão Geral da Solução

O projeto foi feito com a ideia de um sistema de alerta automático para superaquecimento de usinas nucleares, havendo também métodos para ativá-lo manualmente para casos de mal funcionamento ou para outros possíveis alertas.
As medidas ultilizadas como parâmetros para o alarme e aumento de temperatura são meramente ilustrativas e não descrevem os cenários reais de tais locais, mas são úteis para a demonstração.

---

## 2️⃣ Arquitetura do Sistema Embarcado

O programa começa com a temperatura base de 130 graus, substituindo a leitura real de um sensor, e após isso entra em seu loop, onde ocorrem os seguintes passos:

- delay de 0.1 segundo para melhor observação da temperatura
- aumento de um grau
- *se* o botão de alerta está pressionado, o led fica aceso e uma flag é levantada
- *senão, se* a temperatura for maior que 140 graus, o led é acendido
- *se* a temperatura for menor que 120 graus *e* a flag não está levantada, o led é desligado
- *se* o botão de resfriamento está precionado, a temperatura cai em 4 graus (com o aumento no início se totalizam em 3)

o loop tem a seguinte lógica, caso a temperatura suba além do desejado, o alerta dispara informando o problema. Com essa informação, pode-se ativar o sistema de resfriamento até atingir um valor de graus celsius aceitável. Caso o alarme seja disparado manualmente, ele não pode ser desligado pela leitura de temperatura, pois o problema alertado não está em seus parâmetros.

---

## 3️⃣ Componentes Utilizados na Simulação

Foram usados:
- ESP32
- led vermelho, como sistema de alerta
- botão vermelho, para disparar alerta manualmente
- botão verde, para resfriamento

## 4️⃣ Decisões Técnicas Relevantes

Para um fluxo de trabalho mais ágil, o projeto foi minimalista:
- não houve uso de um OLED para expor temperatura mas sim o terminal, 
- para diminuir o aquecimento foi usado um botão no lugar de uma queda automática,
- uso de apenas *if*s em seu loop,
- sem presença de funções ou classes,
- led para representar um alarme que se estenderia por toda a usina.
- não há diferenciação de um alerta manual e de um alerta de temperatura

---

## 5️⃣ Resultados Obtidos

O sistema e a eletrônica realizam seus papéis perfeitamente bem, havendo apenas problemas com *clicks* no lugar de manter os botões pressionados, pois há o delay para melhor leitura da temperatura no terminal.
O led acende quando o aquecimento supera o parâmetro passado (140) e desliga quando cai significativamente (>120) com o uso do botão de resfriamento, obedecendo a presença da flag manual de ativação do alarme.

---

## 6️⃣ Comentários Adicionais (Opcional)

Por mais que a solução tenha atingido minhas espectativas, sou ciente de que é simplória para o problema apresentado, havendo múltiplos outros fatores e problemas que exijam mais cuidado na produção de algo nesse escopo.
Houveram problemas para o funcionamento correto com o github actions, porém eram apenas causados pelo nome da conexão com o wokwi não estar correspondente com o pedido pelo .yml
Por fim, o projeto prático foi extremamente útil para fixar os aprendizados do curso de uma maneira interativa e desafiadora, tanto para funcionamento do código quanto às ligações dos circuitos da parte eletrônica.

---