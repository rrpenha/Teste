# Ricardo de Ramos Penha - 11/09/2019
# Teste de proficiência Semantix

1 - Qual o objetivo do comando cache em Spark?

Na Criação de um RDD (Resilient Distributed Datasets) as aplicações de operações não acessam os dados diretamente, criam uma instrução que poderá ser aplicada em um acesso futuro. Com isso podemos usar a mesma instrução repetidamente, através do comando cache, que guarda esse resultado na memória, melhorando assim a eficiência do código, evitando o acesso direto aos discos repetidas vezes.

2 - O mesmo código implementado em Spark é normalmente mais rápido que a implementação equivalente em MapReduce. Por quê?

As aplicações desenvolvidas em MapReduce são na maioria das vezes mais lentas que aquelas desenvolvidas em Spark e a memória é um fator que explica isso. Normalmente roda-se vários processos MapReduce em sequência ao invés de se executar em uma única vez e o resultado de cada processo é gravado no disco e no próximo job essa informação precisa ser lida novamente. Um processo Spark permeia os resultados intermediários entre as operações a serem executadas através do cache desses dados em memória, e também permite que diversas operações possam ser executadas sobre um mesmo conjunto de dados, reduzindo a necessidade de i/o em disco e mesmo em situações onde ocorre a execução de apenas um processo o Spark tem um  desempenho superior ao MapReduce, pois processos Spark podem ser iniciados mais rapidamente, já que ,para cada processo MapReduce, uma nova instância da JVM é iniciada, enquanto o Spark mantém a JVM em execução em cada nó, bastando iniciar uma nova thread , o que é mais rápido.

3 - Qual é a função do SparkContext ?

O SparkContext é como se fosse um cliente no ambiente de execução do Spark. É através dele que são enviadas as configurações que serão utilizadas na alocação de recursos, como processadores e o uso de memória. Também é utilizado para a criaçãos de RDDs, criar variáveis e executar processos, um exemplo é a conexão entre o Driver Program, que controla o processamento e o Cluster Manager que controla os nós que formam o cluster.

4 - Explique com suas palavras o que é Resilient Distributed Datasets (RDD).

RDD é uma abstração na forma de processamento dos dados no Spark. São ditos Resilientes por serem tolerantes à falhas, pois podem reprocessar partes de dados perdidas nos nós e ditos distribuídos por estarem divididos em partições através de diferentes nós em um cluster. Podem ser executados em paralelo com diferentes operações sendo executadas em partições distintas em um mesmo RDD. Pode ser entendido como um sistema para coletar de forma organizada dados em vários pontos da rede quando for solicitada alguma ação sobre esses dados.

5 - GroupByKey é menos eficiente que reduceByKey em grandes dataset.
 Por quê?
 
A diferença entre ambos está na quantidade de dados trafegados na rede , o reduceByKey é mais eficiente pois promove um primeiro agrupamento de dados em cada nó do cluster para depois realizar uma única operação de união dos dados coletados em cada um dos nós, o GroupByKey realiza um agrupamento apenas ao final o que faz aumentar o número de informações trafegadas na rede.

6 - Explique o que o código Scala abaixo faz.

val textFile = sc . textFile ( "hdfs://..." ) val counts = textFile . flatMap ( line => line . split ( " " )) . map ( word => ( word , 1 ))
. reduceByKey ( _ + _ ) counts . saveAsTextFile ( "hdfs://..." )

O código lê um arquivo texto e cada linha do mesmo é dividida em uma sequência de palavras transformadas em uma única coleção ou seja, cada um dos termos separados por espaço no arquivo de entrada são reunidos em uma única lista e cada palavra é então transformada em um mapeamento de chave valor, o que reduzirá os valores iguais de chave, com chave igual à própria palavra. Esses valores são agregados a um único elemento com contador refletindo esse número de ocorrências. Ao final é salvo o RDD com a contagem de cada palavra.
