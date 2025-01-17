# Databricks notebook source
# MAGIC %md
# MAGIC # Lab Exercise
# MAGIC ## De-Duping Data

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Instructions
# MAGIC
# MAGIC In this exercise, we're doing ETL on a file we've received from some customer. That file contains data about people, including:
# MAGIC
# MAGIC * first, middle and last names
# MAGIC * gender
# MAGIC * birth date
# MAGIC * Social Security number
# MAGIC * salary
# MAGIC
# MAGIC But, as is unfortunately common in data we get from this customer, the file contains some duplicate records. Worse:
# MAGIC
# MAGIC * In some of the records, the names are mixed case (e.g., "Carol"), while in others, they are uppercase (e.g., "CAROL"). 
# MAGIC * The Social Security numbers aren't consistent, either. Some of them are hyphenated (e.g., "992-83-4829"), while others are missing hyphens ("992834829").
# MAGIC
# MAGIC The name fields are guaranteed to match, if you disregard character case, and the birth dates will also match. (The salaries will match, as well,
# MAGIC and the Social Security Numbers *would* match, if they were somehow put in the same format).
# MAGIC
# MAGIC Your job is to remove the duplicate records. The specific requirements of your job are:
# MAGIC
# MAGIC * Remove duplicates. It doesn't matter which record you keep; it only matters that you keep one of them.
# MAGIC * Preserve the data format of the columns. For example, if you write the first name column in all lower-case, you haven't met this requirement.
# MAGIC * Write the result as a Parquet file, as designated by *destFile*.
# MAGIC * The final Parquet "file" must contain 8 part files (8 files ending in ".parquet").
# MAGIC
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** The initial dataset contains 103,000 records.<br/>
# MAGIC The de-duplicated result haves 100,000 records.

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Getting Started
# MAGIC
# MAGIC Run the following cell to configure our "classroom."

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %run "./Includes/Initialize-Labs"

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace

# Assuming spark is your SparkSession object
spark = SparkSession.builder.appName("ETL").getOrCreate()

# Step 1: Read the input file into a DataFrame
# Replace 'inputFile' with the path to your input file
df = spark.read.csv('inputFile', header=True, inferSchema=True)

# Step 2: Normalize the Data
# Create new columns for comparison
df_normalized = df.withColumn('first_name_normalized', lower(col('first_name'))) \
                  .withColumn('middle_name_normalized', lower(col('middle_name'))) \
                  .withColumn('last_name_normalized', lower(col('last_name'))) \
                  .withColumn('ssn_normalized', regexp_replace(col('ssn'), '-', ''))

# Step 3: Remove Duplicates
# Drop duplicates based on the normalized columns
df_deduplicated = df_normalized.dropDuplicates(
    ['first_name_normalized', 'middle_name_normalized', 'last_name_normalized', 'birth_date', 'ssn_normalized']
)

# Step 4: Write the result as a Parquet file
# Replace 'destFile' with the path to your output directory
df_deduplicated.drop('first_name_normalized', 'middle_name_normalized', 'last_name_normalized', 'ssn_normalized') \
               .write.parquet('destFile', mode='overwrite')

# Step 5: Ensure the output contains 8 part files
# This can be done by coalescing to 8 partitions before writing
df_deduplicated.coalesce(8) \
               .drop('first_name_normalized', 'middle_name_normalized', 'last_name_normalized', 'ssn_normalized') \
               .write.parquet('destFile', mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Hints
# MAGIC
# MAGIC * Use the <a href="http://spark.apache.org/docs/latest/api/python/index.html" target="_blank">API docs</a>. Specifically, you might find 
# MAGIC   <a href="http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame" target="_blank">DataFrame</a> and
# MAGIC   <a href="http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#module-pyspark.sql.functions" target="_blank">functions</a> to be helpful.
# MAGIC * It's helpful to look at the file first, so you can check the format. `dbutils.fs.head()` (or just `%fs head`) is a big help here.

# COMMAND ----------

# TODO

(source, sasEntity, sasToken) = getAzureDataSource()
spark.conf.set(sasEntity, sasToken)

sourceFile = source + "/dataframes/people-with-dups.txt"
destFile = userhome + "/people.parquet"

# In case it already exists
dbutils.fs.rm(destFile, True)

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://s3-us-west-2.amazonaws.com/curriculum-release/images/105/logo_spark_tiny.png) Validate Your Answer
# MAGIC
# MAGIC At the bare minimum, we can verify that you wrote the parquet file out to **destFile** and that you have the right number of records.
# MAGIC
# MAGIC Running the following cell to confirm your result:

# COMMAND ----------

finalDF = spark.read.parquet(destFile)
finalCount = finalDF.count()

clearYourResults()
validateYourAnswer("01 Expected 100000 Records", 972882115, finalCount)
summarizeYourResults()

