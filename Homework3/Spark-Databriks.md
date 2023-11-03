# Spark Databriks

* Notebook that was used can be found in `MSAI-339_Databricks Exercise.ipynb`.
* Output for "Display top 5 rows ordered in ascending order by `age` and ascending order by `education_num`" is as follows:

```python
display(spark.sql("SELECT * FROM adult ORDER BY age asc, education_num asc LIMIT 5"))
```

| age | workclass | fnlwgt | education | education_num | marital_status | occupation      | relationship   | race  | sex  | capital_gain | capital_loss | hours_per_week | native_country | income |
| --- | --------- | ------ | --------- | ------------- | -------------- | --------------- | -------------- | ----- | ---- | ------------ | ------------ | -------------- | -------------- | ------ |
| 17  | Private   | 270942 | 5th-6th   | 3             | Never-married  | Other-service   | Other-relative | White | Male | 0            | 0            | 48             | Mexico         | <=50K  |
| 17  | Private   | 168807 | 7th-8th   | 4             | Never-married  | Craft-repair    | Not-in-family  | White | Male | 0            | 0            | 45             | United-States  | <=50K  |
| 17  | Private   | 168203 | 7th-8th   | 4             | Never-married  | Farming-fishing | Other-relative | Other | Male | 0            | 0            | 40             | Mexico         | <=50K  |
| 17  | Private   | 46402  | 7th-8th   | 4             | Never-married  | Sales           | Own-child      | White | Male | 0            | 0            | 8              | United-States  | <=50K  |
| 17  | ?         | 127003 | 9th       | 5             | Never-married  | ?               | Own-child      | Black | Male | 0            | 0            | 40             | United-States  | <=50K  |
