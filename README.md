# Event Driven Data Processing
An entirely serverless event driven data pipeline built on AWS cloud for high scalability and flexibility

## Solution Architecture
<p align="left">
  <img src="https://raw.githubusercontent.com/gabriel-barata/images/master/event-driven-data-pipeline/68747470733a2f2f692e706f7374696d672e63632f624e4d306a7642642f6469616772616d2e706e67.png" alt="Texto Alternativo" width="720">
</p>




## Temp

Amazon S3 (Simple Storage Service):
O Amazon S3 é um serviço de armazenamento de objetos altamente escalável e durável. Nossa arquitetura usa o S3 como um repositório de dados, onde os arquivos são adicionados ao bucket "dl-bronze-layer".

Amazon EventBridge:
O Amazon EventBridge é um serviço de roteamento de eventos que permite capturar, processar e enviar eventos de diferentes serviços. Configuramos uma regra no EventBridge para acionar sempre que um novo arquivo for adicionado ao bucket "dl-bronze-layer".

EventBridge Rule:
A regra do EventBridge é configurada com base em um padrão de correspondência, que define quando a regra será acionada. Nesse caso, a regra é acionada quando um novo arquivo é adicionado ao bucket "dl-bronze-layer".

Amazon SNS (Simple Notification Service):
O Amazon SNS é um serviço de mensagens e notificações. Configuramos um tópico SNS para receber mensagens do EventBridge quando a regra é acionada. O SNS é responsável por encaminhar a mensagem para os assinantes registrados no tópico.

Amazon SQS (Simple Queue Service):
O Amazon SQS é um serviço de filas de mensagens. Configuramos uma fila SQS para receber as mensagens do tópico SNS. Quando uma nova mensagem é recebida, ela é colocada na fila SQS para processamento posterior.

AWS Lambda:
O AWS Lambda é um serviço de computação sem servidor. Configuramos uma função Lambda para consumir a fila SQS e processar as mensagens recebidas. A função Lambda pode executar transformações nos arquivos recém-chegados ao bucket "dl-bronze-layer".

Resumo do fluxo de dados:

Um novo arquivo é adicionado ao bucket "dl-bronze-layer" no Amazon S3.
O Amazon EventBridge detecta a adição do arquivo e aciona a regra configurada.
O EventBridge gera um evento contendo informações sobre o arquivo adicionado.
O evento é enviado para o tópico SNS configurado.
O tópico SNS encaminha a mensagem contendo o evento para a fila SQS configurada.
A função Lambda é acionada quando uma nova mensagem é recebida na fila SQS.
A função Lambda processa o arquivo, executando transformações ou outras operações definidas.
Esse é um resumo da arquitetura e do fluxo de dados da pipeline que construímos. Ela permite automatizar o processamento de arquivos adicionados ao bucket "dl-bronze-layer", acionando uma função Lambda para realizar transformações ou outras ações necessárias.

## Resources

+ The policies used on this solution was created wiht [aws policy generator](https://awspolicygen.s3.amazonaws.com/policygen.html)'s help.
+ The [policy](https://docs.aws.amazon.com/pt_br/aws-managed-policy/latest/reference/AmazonSNSFullAccess.html) used for SNS full acess.