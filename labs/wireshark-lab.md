# Laboratório Wireshark
#### Alunos: Marcio Lima Inácio - 587265
#### Felipe Sampaio de Souza

***

**1. Liste 3 protocolos diferentes que aparecem na coluna protocolo da janela de
listagem de pacotes capturados do Wireshark.**

Os tipos de protocolos apresentados são: DNS, TCP, ICMP, HTTP e TLSv1.2.

**2. Quanto tempo transcorreu desde quando a mensagem HTTP GET foi enviada até
quando a resposta HTTP OK foi recebida?**

A mensagem _GET_ foi enviada aos 242ms desde o início do experimento e a mensagem _OK_ foi recebida aos 405ms. Portanto, tem-se 163ms entre as mensagens.

**3. Perguntas sobre HTTP:**
    <ol type="a">
    **<li>Que versão de HTTP está executando o seu navegador e o servidor?</li>**
    A versão de HTTP executando no navegador é HTTP 1.1.
    A versão de HTTP executando no servidor é HTTP 1.1.
    **<li>Qual é o endereço IP do seu computador e do servidor gaia.cs.umass.edu?</li>**
    O endereço IP do computador é 192.119.100.5.
    O endereço do servidor é 128.119.245.12.
    **<li>Qual é o código de status retornado do servidor para o seu navegador?</li>**
    O código de status retornado pelo servidor foi o de valor 200.
    **<li>Quantos bytes de conteúdo estão sendo devolvidos para o seu navegador?</li>**
    O tamanho do conteúdo transferido foi de 81 bytes.
    </ol>

**4. Perguntas sobre HTTP com GET condicional:**
    <ol type="a">
    **<li>Inspecione o conteúdo da primeira solicitação HTTP GET do seu navegador para o servidor. Você vê uma linha contendo "IF-MODIFIED-SINCE" na mensagem HTTP GET?</li>**
    **<li>Inspecione o conteúdo da resposta do servidor da primeira solicitação do seu navegador (referente ao item a). O servidor retorna explicitamente o conteúdo do arquivo? Justifique sua resposta. Inspecione o conteúdo da segunda solicitação HTTP GET do seu navegador para o servidor. Você vê uma linha “IF-MODIFIED-SINCE:” na mensagem HTTP GET? Se a sua resposta é sim, quais são as informações que seguem o “IF-MODIFIED-SINCE”?</li>**
    **<li>Qual é o código de status de HTTP e frase retornada do servidor em resposta à segunda solicitação HTTP GET (referente ao item c)? O servidor retorna explicitamente o conteúdo do arquivo? Explicar.</li>**
    </ol>

**5. Perguntas sobre recuperação de documentos longos em HTTP:**
    <ol type="a">
    **<li>Quantas mensagens de solicitações HTTP GET seu navegador enviou? Qual é o número do pacote que contém a mensagem GET?</li>**
    **<li>Qual é o número do pacote que contém o código de status e a frase associada com a resposta ao pedido HTTP GET?</li>**
    **<li>Qual é o código de status e a frase na resposta?</li>**
    **<li>Quantos segmentos TCP (contendo os dados) foram necessários para transportar a resposta HTTP e o texto da Declaração dos Direitos dos Estados Unidos?</li>**
    </ol>

**6. Perguntas sobre documentos HTML com objetos incorporados:**
    <ol type="a">
    **<li>Quantas mensagens de solicitação HTTP GET seu navegador enviou? A quais endereços da Internet foram enviadas estas requisições?</li>**
    **<li>Você pode dizer se o navegador baixou estas duas imagens serialmente ou se elas foram baixadas de dois sítios web em paralelo? Explicar.</li>**

**7. Perguntas sobre DNS e Wireshark:**
    <ol type="a">
    **<li>Qual é a porta de destino para a mensagem de consulta DNS? Qual é a porta de origem da mensagem de resposta DNS?</li>**
    **<li>Para qual endereço IP a mensagem de consulta DNS é enviada? Use ipconfig para determinar o endereço IP do seu servidor DNS local. O endereço do IP do servidor que respondeu à consulta DNS e o mesmo do seu servidor DNS local?</li>**
    **<li>Examine a mensagem de consulta DNS. Qual é o tipo (Type) da consulta DNS?</li>**
    **<li>Examine a mensagem de resposta DNS. Quantas respostas “answers” são fornecidas? O que cada uma dessas respostas contém?</li>**
    **<li>Localize o pacote TCP SYN (enviado pelo seu computador e posterior à mensagem de resposta DNS). O endereço IP de destino, do pacote SYN, corresponde a qualquer um dos endereços IP fornecidos na mensagem de resposta DNS?</li>**
    **<li>A página web http://www.ietf.org contém imagens. Antes de recuperar cada imagem, o seu computador emite novas consultas DNS?</li>**
    </ol>

**8. Perguntas sobre nslookup e Wireshark:**
    <ol type="a">
    **<li>Para qual endereço IP a mensagem de consulta DNS foi enviada? É este o endereço IP do seu servidor DNS local? Se não, a quem corresponde este endereço IP?</li>**
    **<li>Examine a mensagem de consulta DNS. Qual é o tipo (Type) desta consulta DNS? A mensagem de consulta contém alguma resposta (answers)?</li>**
    **<li>Fornecer um screenshot (captura de tela) que justifique as suas respostas.</li>**
    </ol>

**9. Perguntas sobre TCP:**
    <ol type="a">
    **<li>Qual é o endereço IP de gaia.cs.umass.edu? Qual é o número da porta pela qual o servidor está recebimento e enviando segmentos TCP para esta conexão?</li>**
    **<li>Considere o segmento TCP que contém o HTTP POST como o primeiro segmento na conexão TCP. Quais são os números de sequência dos seis primeiros segmentos na conexão TCP (incluindo o segmento que contém o HTTP POST)? Em que momento (hora do dia) foi enviado cada segmento? Quando foi recebido o ACK de cada segmento? Dada a diferença dos tempos nos quais cada segmento TCP foram enviados e quando a sua confirmação foi recebida, qual é o valor RTT para cada um dos seis segmentos?**</li><br />
    **Observação: o Wireshark permite traçar o RTT para cada um dos segmentos TCP enviados. Selecione um segmento TCP na listagem de pacotescapturados e selecione: Statistics->TCP Stream Graph- >Round Trip Time Graph.**
    **<li>Existem segmentos retransmitidos? Qual informação você procurou a fim de responder esta pergunta?</li>**
    </ol>

**10. É possível identificar onde começa e onde termina a fase slowstart do TCP? É possível identificar onde o “congestion avoidance” assume o controle?**

**11. Selecione um pacote UDP e responda:**
    <ol type="a">
    **<li>Ao consultar as informações exibidas no campo de conteúdo do pacote do Wireshark para o pacote selecionado, determinar:</li>**
    <ul>
    **<li>O comprimento (em bytes) de cada um dos campos de cabeçalho UDP.</li>**
    **<li>O número máximo de bytes que podem ser incluídos no payload UDP.</li>**
    **<li>O maior número possível de porta de origem.</li>**
    </ul>
    **<li>O valor no campo “Length” é o comprimento de que? Verifique a sua resposta com o valor do pacote UDP selecionado.</li>**
    </ol>
