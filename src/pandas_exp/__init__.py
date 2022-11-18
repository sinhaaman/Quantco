
from pandas_exp.dataframe import QuantcoDataFrame
from pandas_exp.series import QuantcoSeries 

invalidFrame = {
    'Test' : ["Test", "Test"],
    'Number': [0.1, 0.2, 0.3]
}
validFrame = {
    'Test' : ["Test", "Test"],
    'Number': [0.1, 0.2]
}

df = QuantcoDataFrame({
    'SKU' : ["X4E", "T3B", "F8D", "C7X"],
    'price' : [7.0, 3.5, 8.0, 6.0],
    'sales' : [5, 3, 1, 10],
    'taxed' : [False, False, True, False]
})
result1 = df["price"]
result2  = (df["price"] + 5.0 > 10.0) & (df["sales"] > 3)
result3 = ~df["taxed"]
result  = (df["price"] + 5.0 > 10.0) & (df["sales"] > 3) & ~df["taxed"]

series = QuantcoSeries("price", [7.0, 3.5, 8.0, 6.0])
result4 = df[result]["SKU"] 
print(series)
print(result)
#df = QuantcoDataFrame(validFrame)
#df1 = QuantcoDataFrame()