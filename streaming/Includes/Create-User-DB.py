# Databricks notebook source
# MAGIC %scala
# MAGIC val databaseName = {
# MAGIC   val tags = com.databricks.logging.AttributionContext.current.tags
# MAGIC   val name = tags.getOrElse(com.databricks.logging.BaseTagDefinitions.TAG_USER, java.util.UUID.randomUUID.toString.replace("-", ""))
# MAGIC   val username = if (name != "unknown") name else dbutils.widgets.get("databricksUsername")
# MAGIC   val databaseName   = username.replaceAll("[^a-zA-Z0-9]", "_") + "_db"
# MAGIC   spark.conf.set("com.databricks.training.spark.databaseName", databaseName)
# MAGIC   databaseName
# MAGIC }
# MAGIC
# MAGIC displayHTML(s"Created user-specific database")

# COMMAND ----------

# MAGIC %scala
# MAGIC spark.sql("CREATE DATABASE IF NOT EXISTS `%s`".format(databaseName))
# MAGIC spark.sql("USE `%s`".format(databaseName))
# MAGIC
# MAGIC displayHTML("""Using the database <b style="color:green">%s</b>.""".format(databaseName))
