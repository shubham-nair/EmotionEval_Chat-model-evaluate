from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ChatLogAnalysis").getOrCreate()

# 需要真实的数仓地址和配置参数，才能实现批量处理

hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", "YOUR_AWS_ACCESS_KEY_ID")
hadoop_conf.set("fs.s3a.secret.key", "YOUR_AWS_SECRET_ACCESS_KEY")
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

df = spark.read.json("s3a://my-company-bucket/chat-logs/")

print(df.count())
print(df.printSchema())
