
from pandas_exp.dataframe import QuantcoDataFrame

df = QuantcoDataFrame({
    'SKU' : ["X4E", "T3B", "F8D", "C7X"],
    'price' : [7.0, 3.5, 8.0, 6.0],
    'sales' : [5, 3, 1, 10],
    'taxed' : [False, False, True, False]
})

# let's find all our tax free products/SKUs where the price our $5.0 shipping fee is more than $10 and we had more than 3 sales.
print(df[(df["price"] + 5.0 > 10.0) & (df["sales"] > 3) & ~df["taxed"]]["SKU"])

df = QuantcoDataFrame({
    'Student' : ["Harry Potter", "Hermione Granger", "Ron Weasley", "Draco Malfoy", "Neville Longbottom"],
    'Course Attendance - DarkArts' : [True, False, True, None, False],
    'Grade - DarkArts' : [9, 9, 8, 8, 7],
    'Friends' : [2, 2, 2, 5, 10],
    'House': ["Gryffindor", "Gryffindor", "Gryffindor", "Slytherin", None],
    "Quiditch-Seeker": [True, None, False, True, None]
})
# let's award 1.0 grade points to Gryfinndor and see which student has greater than 8 grade points.
# Filter those students who have >=2 friends and have attended the darkarts course and is also a quiditch seeker.
result = df[(df["Grade - DarkArts"] + 1.0 > 8) & (df['House'] == "Gryffindor") & (df['Friends'] >=2) & (df["Course Attendance - DarkArts"] == True) & (df['Quiditch-Seeker'] == True)]
print(result["Student"])