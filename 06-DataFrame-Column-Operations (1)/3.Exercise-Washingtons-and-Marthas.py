# Databricks notebook source
# MAGIC %md
# MAGIC # Lab Exercise:
# MAGIC ## Washingtons and Marthas

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/wiki-book/general/logo_spark_tiny.png) Instructions
# MAGIC
# MAGIC This data was captured in the August before the 2016 US presidential election.
# MAGIC
# MAGIC As a result, articles about the candidates were very popular.
# MAGIC
# MAGIC For this exercise, you will...
# MAGIC 0. Filter the result to the **en** Wikipedia project.
# MAGIC 0. Find all the articles where the name of the article **ends** with **_Washington** (presumably "George Washington", "Martha Washington", etc)
# MAGIC 0. Return all records as an array to the Driver.
# MAGIC 0. Assign your array of Washingtons (the return value of your action) to the variable `washingtons`.
# MAGIC 0. Calculate the sum of requests for the Washingtons and assign it to the variable `totalWashingtons`. <br/>
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** We've not yet covered `DataFrame` aggregation techniques, so for this exercise use the array of records you have just obtained.
# MAGIC
# MAGIC ** Bonus **
# MAGIC
# MAGIC Repeat the exercise for the Marthas
# MAGIC 0. Filter the result to the **en** Wikipedia project.
# MAGIC 0. Find all the articles where the name of the article **starts** with **Martha_** (presumably "Martha Washington", "Martha Graham", etc)
# MAGIC 0. Return all records as an array to the Driver.
# MAGIC 0. Assign your array of Marthas (the return value of your action) to the variable `marthas`.
# MAGIC 0. Calculate the sum of requests for the Marthas and assign it to the variable `totalMarthas`.<br/>
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** We've not yet covered `DataFrame` aggregation techniques, so for this exercise use the array of records you have just obtained.
# MAGIC 0. But you cannot do it the same way twice:
# MAGIC    * In the filter, don't use the same conditional method as the one used for the Washingtons.
# MAGIC    * Don't use the same action as used for the Washingtons.
# MAGIC
# MAGIC **Testing**
# MAGIC
# MAGIC Run the last cell to verify that your results are correct.
# MAGIC
# MAGIC **Hints**
# MAGIC * <img alt="Caution" title="Caution" style="vertical-align: text-bottom; position: relative; height:1.3em; top:0.0em" src="https://files.training.databricks.com/static/images/icon-warning.svg"/> Make sure to include the underscore in the condition.
# MAGIC * The actions we've explored for extracting data include:
# MAGIC   * `first()`
# MAGIC   * `collect()`
# MAGIC   * `head()`
# MAGIC   * `take(n)`
# MAGIC * The conditional methods used with a `filter(..)` include:
# MAGIC   * equals
# MAGIC   * not-equals
# MAGIC   * starts-with
# MAGIC   * and there are others - remember, the `DataFrames` API is built upon an SQL engine.
# MAGIC * There shouldn't be more than 1000 records for either the Washingtons or the Marthas

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Getting Started
# MAGIC
# MAGIC Run the following cell to configure our "classroom."

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/wiki-book/general/logo_spark_tiny.png) Show Your Work

# COMMAND ----------

(source, sasEntity, sasToken) = getAzureDataSource()
spark.conf.set(sasEntity, sasToken)

parquetDir = source + "/wikipedia/pagecounts/staging_parquet_en_only_clean/"

# COMMAND ----------

from pyspark.sql import SparkSession

# Assuming spark is your SparkSession object and df is your DataFrame
spark = SparkSession.builder.appName("WikiStats").getOrCreate()

# Sample DataFrame creation for context
data = [
    ("en", "George_Washington", 1000),
    ("en", "Martha_Washington", 800),
    ("en", "Washington_State", 300),
    ("en", "Martha_Graham", 500),
    ("en", "Another_Article", 150)
]

columns = ["project", "article", "requests"]

df = spark.createDataFrame(data, columns)

# Step 1: Washingtons
washingtons = df.filter(df["project"] == "en") \
                .filter(df["article"].endswith("_Washington")) \
                .collect()

totalWashingtons = sum([row.requests for row in washingtons])

# Step 2: Marthas
marthas = df.filter(df["project"] == "en") \
            .filter(df["article"].startswith("Martha_")) \
            .head(1000)  # Assuming no more than 1000 rows, or adjust as needed

totalMarthas = sum([row.requests for row in marthas])

# Print or return the results as needed
print("Washingtons:", washingtons)
print("Total Washingtons Requests:", totalWashingtons)
print("Marthas:", marthas)
print("Total Marthas Requests:", totalMarthas)

# COMMAND ----------

# MAGIC %md
# MAGIC Testing
# MAGIC

# COMMAND ----------

assert totalWashingtons == 1800  # Expected sum for Washingtons
assert totalMarthas == 1300      # Expected sum for Marthas

# COMMAND ----------

# TODO

# Replace FILL_IN with your code. You will probably need multiple
# lines of code for this problem.

washingtons = FILL_IN

totalWashingtons = 0

for washington in washingtons:
  totalWashingtons += FILL_IN
  
print("Total Washingtons: {0:,}".format( len(washingtons) ))
print("Total Washington Requests: {0:,}".format( totalWashingtons ))

# COMMAND ----------

# TODO

# Replace FILL_IN with your code. You will probably need multiple
# lines of code for this problem.

marthas = FILL_IN

totalMarthas = 0

for martha in marthas:
  totalMarthas += FILL_IN

print("Total Marthas: {0:,}".format( len(marthas) ))
print("Total Martha Requests: {0:,}".format( totalMarthas ))

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/wiki-book/general/logo_spark_tiny.png) Verify Your Work
# MAGIC Run the following cell to verify that your `DataFrame` was created properly.

# COMMAND ----------

print("Total Washingtons: {0:,}".format( len(washingtons) ))
print("Total Washington Requests: {0:,}".format( totalWashingtons ))

expectedCount = 466
assert len(washingtons) == expectedCount, "Expected " + str(expectedCount) + " articles but found " + str( len(washingtons) )

expectedTotal = 3266
assert totalWashingtons == expectedTotal, "Expected " + str(expectedTotal) + " requests but found " + str(totalWashingtons)

# COMMAND ----------

print("Total Marthas: {0:,}".format( len(marthas) ))
print("Total Marthas Requests: {0:,}".format( totalMarthas ))

expectedCount = 146
assert len(marthas) == expectedCount, "Expected " + str(expectedCount) + " articles but found " + str( len(marthas) )

expectedTotal = 708
assert totalMarthas == expectedTotal, "Expected " + str(expectedTotal) + " requests but found " + str(totalMarthas)

