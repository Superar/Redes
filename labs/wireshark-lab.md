# Laboratório Wireshark
#### Alunos: Marcio Lima Inácio - 587265
#### Felipe Sampaio de Souza - 619523

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
    Não existe nenhuma linha na mensagem contendo a flag _IF-MODIFIED-SINCE_.
    **<li>Inspecione o conteúdo da resposta do servidor da primeira solicitação do seu navegador (referente ao item a). O servidor retorna explicitamente o conteúdo do arquivo? Justifique sua resposta. <br \>Inspecione o conteúdo da segunda solicitação HTTP GET do seu navegador para o servidor. Você vê uma linha “IF-MODIFIED-SINCE:” na mensagem HTTP GET? Se a sua resposta é sim, quais são as informações que seguem o “IF-MODIFIED-SINCE”?</li>**
    O servidor retorna explicitamente o conteúdo da página HTML na seção de dados de texto da mensagem.
    <br />
    A mensagem retornada é:
    <p>
    ```<html>``` <br />
    ``` Congratulations!  You've downloaded the first Wireshark lab file!\n``` <br />
    ```</html>```
    </p>
    A mensagem de _GET_ não possui a flag _IF-MODIFIED-SINCE_, pois esta é a primeira vez em que a página é carregada, portanto ela não está salva no cache do navegador e precisa ser totalmente enviada na mensagem _OK_ do protocolo HTTP. <br />
    Ao se executar a requisição uma segunda vez (recarregando a página), a mensagem _GET_ possui a seguinte especificação:
    <p>```If-Modified-Since: Tue, 26 Sep 2017 05:59:01 GMT\r\n``` </p>
    **<li>Qual é o código de status de HTTP e frase retornada do servidor em resposta à segunda solicitação HTTP GET (referente ao item c)? O servidor retorna explicitamente o conteúdo do arquivo? Explicar.</li>**
    A mensagem de resposta possui o _status code_ 304, indicando que a página não foi modificada desde a data especificada na mensagem _GET_. Desta forma, a mensagem não possui a página completa, pois não é necessária.
    </ol>

**5. Perguntas sobre recuperação de documentos longos em HTTP:**
    <ol type="a">
    **<li>Quantas mensagens de solicitações HTTP GET seu navegador enviou? Qual é o número do pacote que contém a mensagem GET?</li>**
    Enviou apenas uma única requisição GET. Número 82.
    **<li>Qual é o número do pacote que contém o código de status e a frase associada com a resposta ao pedido HTTP GET?</li>**
    92
    **<li>Qual é o código de status e a frase na resposta?</li>**
    200 OK
    **<li>Quantos segmentos TCP (contendo os dados) foram necessários para transportar a resposta HTTP e o texto da Declaração dos Direitos dos Estados Unidos?</li>**
    3 segmentos TCP
    </ol>

**6. Perguntas sobre documentos HTML com objetos incorporados:**
    <ol type="a">
    **<li>Quantas mensagens de solicitação HTTP GET seu navegador enviou? A quais endereços da Internet foram enviadas estas requisições?</li>**
    Foram enviadas 3 solicitações GET: a primeira para "/wireshark-labs/HTTP-wireshark-file4.html"; a segunda para "/pearson.png"; e a terceira para "/~kurose/cover_5th_ed.jpg"
    **<li>Você pode dizer se o navegador baixou estas duas imagens serialmente ou se elas foram baixadas de dois sítios web em paralelo? Explicar.</li>**
    Levando em consideração a ordem das requisições visualizadas no wireshark, é realizada uma solicitação GET da primeira imagem e, mesmo sem ter chegado a resposta da primeira requisição, o browser já envia a requisição para a segunda imagem, dessa forma as imagem estão sendo baixadas paralelamente.
    </ol>


**7. Perguntas sobre DNS e Wireshark:**
    <ol type="a">
    **<li>Qual é a porta de destino para a mensagem de consulta DNS? Qual é a porta de origem da mensagem de resposta DNS?</li>**
    A porta de destino é 53 e a porta de origem é 35090.
    **<li>Para qual endereço IP a mensagem de consulta DNS é enviada? Use ipconfig para determinar o endereço IP do seu servidor DNS local. O endereço do IP do servidor que respondeu à consulta DNS e o mesmo do seu servidor DNS local?</li>**
    Enviado para o endereço 200.133.224.5 e 200.136.207.5. Ambos correspondem ao servidor dns local (foi utilizado o comando "nmcli device show" para visualizar os endereços de dns locais).
    **<li>Examine a mensagem de consulta DNS. Qual é o tipo (Type) da consulta DNS?</li>**
    Foram geradas várias consultas dns em cadeia, os tipos foram A e AAAA.
    **<li>Examine a mensagem de resposta DNS. Quantas respostas “answers” são fornecidas? O que cada uma dessas respostas contém?</li>**
    Houveram em torno de 5 respostas. Cada resposta tinha o domínio pesquisado, alguns atributos (type, class, cname) e um endereço (addr)
    **<li>Localize o pacote TCP SYN (enviado pelo seu computador e posterior à mensagem de resposta DNS). O endereço IP de destino, do pacote SYN, corresponde a qualquer um dos endereços IP fornecidos na mensagem de resposta DNS?</li>**
    Sim, corresponde a um deles
    **<li>A página web http://www.ietf.org contém imagens. Antes de recuperar cada imagem, o seu computador emite novas consultas DNS?</li>**
    Não, ele passa a utilizar o endereço ip adquirido na consulta dns anterior.
    </ol>

**8. Perguntas sobre nslookup e Wireshark: (estamos utilizando o servidor dns do google 8.8.8.8)**
    <ol type="a">
    **<li>Para qual endereço IP a mensagem de consulta DNS foi enviada? É este o endereço IP do seu servidor DNS local? Se não, a quem corresponde este endereço IP?</li>**
    A consulta dns foi enviada para o ip 8.8.8.8. Difere do ip do servidor de dns local, esse ip equivale ao ip do servidor dns passado como parâmetro para o comando.
    **<li>Examine a mensagem de consulta DNS. Qual é o tipo (Type) desta consulta DNS? A mensagem de consulta contém alguma resposta (answers)?</li>**
    É do tipo A e não possui nenhuma answer.
    **<li>Fornecer um screenshot (captura de tela) que justifique as suas respostas.</li>**
    ![Captura de tela: dns](https://github.com/Superar/Redes/blob/master/labs/imagens/dns.png)
    </ol>

**9. Perguntas sobre TCP:**
    <ol type="a">
    **<li>Qual é o endereço IP de gaia.cs.umass.edu? Qual é o número da porta pela qual o servidor está recebimento e enviando segmentos TCP para esta conexão?</li>**
    O endereço IP do servidor é 128.119.245.12. A porta pela qual o servidor estabelece a conexão é a de número 80.
    **<li>Considere o segmento TCP que contém o HTTP POST como o primeiro segmento na conexão TCP. Quais são os números de sequência dos seis primeiros segmentos na conexão TCP (incluindo o segmento que contém o HTTP POST)? Em que momento (hora do dia) foi enviado cada segmento? Quando foi recebido o ACK de cada segmento? Dada a diferença dos tempos nos quais cada segmento TCP foram enviados e quando a sua confirmação foi recebida, qual é o valor RTT para cada um dos seis segmentos?**</li><br />
    **Observação: o Wireshark permite traçar o RTT para cada um dos segmentos TCP enviados. Selecione um segmento TCP na listagem de pacotescapturados e selecione: Statistics->TCP Stream Graph- >Round Trip Time Graph.**<br />
    As mensagens TCP enviadas foram:<br />
    <ul>
    <li> Pacote 4, com número de sequência 1, enviado às 10:44:20.596858. ACK recebido às 10:44:20.624318, com RTT de aproximadamente 27ms. </li>
    <li> Pacote 5, com número de sequência 566, enviado às 10:44:20.612118. ACK recebido às 10:44:20.647675, com RTT de aproximadamente 63ms.</li>
    <li> Pacote 7, com número de sequência 2026, enviado às 10:44:20.624407. ACK recebido às 10:44:20.694466, com RTT de aproximadamente 70ms.</li>
    <li> Pacote 8, com número de sequência 3486, enviado às 10:44:20.625071. ACK recebido às 10:44:20.739499, com RTT de aproximadamente 114ms.</li>
    <li> Pacote 10, com número de sequência 4946, enviado às 10:44:20.647786. ACK recebido às 10:44:20.787680, com RTT de aproximadamente 140ms.</li>
    <li> Pacote 11, com número de sequência 6406, enviado às 10:44:20.648538. ACK recebido às 10:44:20.838183, com RTT de aproximadamente 190ms.</li>
    </ul>
    **<li>Existem segmentos retransmitidos? Qual informação você procurou a fim de responder esta pergunta?</li>**
    Não existem segmentos retransmitidos, pois ao se visualizar o gráfico Time/Sequence, que mostra o número da sequência enviado em cada tempo, pode-se verificar que não há o envio do mesmo número da sequência em dois momentos distintos.
    </ol>

**10. É possível identificar onde começa e onde termina a fase slowstart do TCP? É possível identificar onde o “congestion avoidance” assume o controle?**
</br>
É possível perceber a fase *slow start* nos primeiros 124ms de troca de pacotes. A partir dos 304ms, o número de pacotes enviados por vez é constante, portanto pode-se identificar o término da fase *slow start*. A partir deste momento, o *congestion avoidance* assume o controle.

**11. Selecione um pacote UDP e responda:**
    <ol type="a">
    **<li>Ao consultar as informações exibidas no campo de conteúdo do pacote do Wireshark para o pacote selecionado, determinar:</li>**
    <ul>
    **<li>O comprimento (em bytes) de cada um dos campos de cabeçalho UDP.</li>**
    Source Port: 2 bytes</br>
    Destination Port: 2 bytes</br>
    Length: 2 bytes</br>
    Checksum: 2 bytes</br>
    **<li>O número máximo de bytes que podem ser incluídos no payload UDP.</li>**
    65.527 bytes, pois o número máximo que o atributo length pode assumir é 65.535 bytes, porém 8 bytes são do próprio cabeçalho.
    **<li>O maior número possível de porta de origem.</li>**
    65,535
    </ul>
    **<li>O valor no campo “Length” é o comprimento de que? Verifique a sua resposta com o valor do pacote UDP selecionado.</li>**
    É o tamanho total do pacote UDP, contando o cabeçalho e o dado transportado.
    </ol>
