### 👤 Identificação do Candidato

- **Nome completo: Elilúcio Teixeira Félix Filho**  
- **GitHub: Elilucio7**  

---

## 1️⃣ Visão Geral da Solução

O projeto foi feito com a ideia de um sistema de alerta automático para superaquecimento de usinas nucleares, havendo também métodos para ativá-lo manualmente para casos de mal funcionamento ou para outros possíveis alertas.
As medidas ultilizadas como parâmetros para o alarme são meramente ilustrativas e não descrevem os cenários reais de tais locais, mas são úteis para a demonstração.

---

## 2️⃣ Arquitetura do Sistema Embarcado

O programa consiste em um loop básico e de baixa complexidade, onde ocorrem os seguintes passos:

- delay de 1 segundo para evitar ao máximo erros de leitura
- leitura dos dados do sensor (caso haja erro continua com leituras até uma aceitável)
- *se* o botão de alerta está pressionado, apenas o led de evacuação fica aceso e o loop encerra, necessitando reiniciar manualmente
- *se* a temperatura for maior que 99 graus e menor que 125 graus, apenas o led de alta temperatura fica aceso
- *se* a temperatura for maior igual a 125 graus, ambos os leds são acesos
- *se* a temperatura for menor que 100 graus, o led de alta temperatura é desligado
- mostra a mensagem escolhida pelo programa no display

O loop tem a seguinte lógica, caso a temperatura suba além do desejado, o alerta dispara informando o problema. Com essa informação, pode-se ativar o sistema de resfriamento até atingir um valor de graus celsius aceitável.
Caso a temperatura venha a ficar descontrolada, o sistema ativa os alarmes de alta temperatura e evacuação.
Caso o alarme seja disparado manualmente, ele não pode ser desligado pela leitura de temperatura, pois o problema alertado não está em seus parâmetros. Também deixando claro que o alarme ativado foi o manual.

---

## 3️⃣ Componentes Utilizados na Simulação

Foram usados:
- ESP32
- sensor ds18x20
- leds vermelho e amarelo, como sistema de alerta
- display oled para visualização dos outputs do sistema
- botão vermelho, para disparar alerta manualmente

## 4️⃣ Decisões Técnicas Relevantes

Para um fluxo de trabalho mais ágil, o projeto foi minimalista:
- uso de apenas uma função
- uso extenso de ifs para lógica simples
- uso de apenas dois leds, além do display, para representar um sistema de alarme robusto
- inexistência de um sistema de resfriamento
- simples botão para disparar um alarme de evacuação

---

## 5️⃣ Resultados Obtidos

O sistema e a eletrônica realizam seus papéis perfeitamente bem, havendo apenas problemas com *clicks* no lugar de manter o botão pressionado, pois há o delay no loop.
Ambos os leds funcionam de acordo com a lógica do sistema e as mensagens apresentadas no display são coerentes com as leituras vindas, com o sistema inteiro parando na ativação do alerta de evacuação;

---

## 6️⃣ Comentários Adicionais (Opcional)

Por mais que a solução tenha atingido minhas espectativas, sou ciente de que é simplória para o problema apresentado, havendo múltiplos outros fatores e problemas que exijam mais cuidado na produção de algo nesse escopo.
Houveram problemas para o funcionamento correto com o github actions, porém eram apenas causados pelo nome da conexão com o wokwi não estar correspondente com o pedido pelo .yml
Por fim, o projeto prático foi extremamente útil para fixar os aprendizados do curso de uma maneira interativa e desafiadora, tanto para funcionamento do código quanto às ligações dos circuitos da parte eletrônica.

---