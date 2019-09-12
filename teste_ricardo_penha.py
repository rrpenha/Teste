#Teste de Ricardo de Ramos Penha 
#Setembro de 2019

from pyspark import SparkConf, SparkContext
from operator import add

conf = (SparkConf()
         .setMaster("local")
         .setAppName("SPark")
         .set("spark.executor.memory", "2g"))
sc = SparkContext(conf = conf)

julho = sc.textFile('access_log_Jul95')
julho = julho.cache()

agosto = sc.textFile('access_log_Aug95')
agosto = agosto.cache()

# Total de Hosts
julho_count = julho.flatMap(lambda line: line.split(' ')[0]).distinct().count()
agosto_count = agosto.flatMap(lambda line: line.split(' ')[0]).distinct().count()
print('Total de Hosts em julho: %s' % julho_count)
print('Total de Hosts em  agosto %s' % agosto_count)

#Total de Erros 404
def erros_404(line):
    try:
        code = line.split(' ')[-2]
        if code == '404':
            return True
    except:
        pass
    return False
    
julho_404 = julho.filter(erros_404).cache()
agosto_404 = agosto.filter(lambda line: line.split(' ')[-2] == '404').cache()

print('Total de Erros 404 em julho: %s' % julho_404.count())
print('Total de Erros 404 em agosto %s' % agosto_404.count())

# Os 5 maiores Urls que causaram erro 404
def maiores_urls(rdd):
    endpoints = rdd.map(lambda line: line.split('"')[1].split(' ')[1])
    counts = endpoints.map(lambda endpoint: (endpoint, 1)).reduceByKey(add)
    top = counts.sortBy(lambda pair: -pair[1]).take(5)
    
    print('\n5 maiores Urls que causaram o erro 404:')
    for endpoint, count in top:
        print(endpoint, count)
        
    return top

maiores_urls(julho_404)
maiores_urls(agosto_404)

# Total de Erros 404 por dia
def daily_count(rdd):
    days = rdd.map(lambda line: line.split('[')[1].split(':')[0])
    counts = days.map(lambda day: (day, 1)).reduceByKey(add).collect()
    
    print('\nTotal de erros 404 por dia:')
    for day, count in counts:
        print(day, count)
        
    return counts

daily_count(julho_404)
daily_count(agosto_404)

# Total de bytes retornados
def tot_bytes(rdd):
    def cont_byte(line):
        try:
            count = int(line.split(" ")[-1])
            if count < 0:
                raise ValueError()
            return count
        except:
            return 0
        
    count = rdd.map(cont_byte).reduce(add)
    return count

print('Total de bytes retornados em julho: %s' % tot_bytes(julho))
print('Total de bytes retornados em agosto: %s' % tot_bytes(agosto))

sc.stop()
