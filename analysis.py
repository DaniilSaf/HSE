import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
#часть 1 для приложения
def moving_average(df):
  df=df.sort_values("timestamp")
  df["movingaverage"]=df["temperature"].rolling(30).mean()
  df["movingstd"] = df["temperature"].rolling(30).std()
  return df
def StandardDeviation(df):
  stats=df.groupby(["city","season"])["temperature"].agg(["mean","std"]).reset_index()
  return stats
def Anomaly(df):
  # тут тоже возьмем отрезок 30 дней для удобства
  df["anomaly"]=(df["temperature"]>df["movingaverage"]+2 *df["movingstd"]) | (df["temperature"] < df["movingaverage"] - 2 * df["movingstd"])
  return df







#часть 2 для сравнение скорости

#ИТОГ

#   последовательная  0.04347330000018701
#   параллельная  0.04609329999948386

def helper(df):
  df=moving_average(df)
  df=Anomaly(df)
  return df
def sequentialanalysis(df):
  result = []
  for city in df["city"].unique():
    df1 = df[df["city"] == city].copy()
    result.append(helper(df1))

  return pd.concat(result)
def parallelanalysis(df):
  df1 = [df[df["city"] == city].copy() for city in df["city"].unique()]
  with ThreadPoolExecutor() as executor:
    result = list(executor.map(helper, df1))
  return pd.concat(result)
df = pd.read_csv("temperature_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
start=time.perf_counter()
timelong= sequentialanalysis(df)
end= time.perf_counter()
print("последовательная ",end - start)
start= time.perf_counter()
timefast= parallelanalysis(df)
end= time.perf_counter()
print("параллельная ",end - start)
