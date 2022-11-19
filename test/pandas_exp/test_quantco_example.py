from pandas_exp.dataframe import QuantcoDataFrame
from pandas_exp.series import QuantcoSeries

def test_quantco_example():
    # Given
    df_dict = {
        'SKU' : ["X4E", "T3B", "F8D", "C7X"],
        'price' : [7.0, 3.5, 8.0, 6.0],
        'sales' : [5, 3, 1, 10],
        'taxed' : [False, False, True, False]
    }
    df = QuantcoDataFrame(df_dict) 

    # When
    result1 = df["price"]
    assert type(result1) == QuantcoSeries
    assert result1.series == df_dict["price"]
    assert result1.type == float
    assert result1.series_name == "price"

    result1 = result1 + 5
    expected_result = [12.0, 8.5, 13.0, 11.0]
    for i in range(len(result1.series)):
        assert result1.series[i] == expected_result[i]
    
    result1 = result1 > 10.0
    expected_result = [True, False, True, True]
    for i in range(len(result1.series)):
        assert result1.series[i] == expected_result[i]
    
    result2 = df["sales"]
    assert type(result2) == QuantcoSeries
    assert result2.series == df_dict["sales"]
    assert result2.type == int
    assert result2.series_name == "sales"

    result2 = result2 > 3
    expected_result = [True, False, False, True]
    for i in range(len(result2.series)):
        assert result2.series[i] == expected_result[i]
    
    result3 = df["taxed"]
    assert type(result3) == QuantcoSeries
    assert result3.series == df_dict["taxed"]
    assert result3.type == bool
    assert result3.series_name == "taxed"

    result3 = ~result3
    expected_result = [True, True, False, True]
    for i in range(len(result3.series)):
        assert result3.series[i] == expected_result[i]
    
    result4 = result1 & result2 & result3
    assert type(result4) == QuantcoSeries
    assert result4.type == bool
    assert result4.series_name == result1.series_name
    expected_result = [True, False, False, True]
    for i in range(len(result4.series)):
        assert result4.series[i] == expected_result[i]
    
    result5 = df[result4]
    expected_result = {
        'SKU' : ["X4E", "C7X"],
        'price' : [7.0, 6.0],
        'sales' : [5, 10],
        'taxed' : [False, False]
    }
    assert type(result5) == QuantcoDataFrame
    assert result5.size() == (2,4)
    for k in result5.frame.keys():
        assert result5[k].series == expected_result[k]
    
    result = result5["SKU"]
    assert type(result) == QuantcoSeries
    assert result.series == expected_result["SKU"]
    assert result.type == str
    assert result.series_name == "SKU" 


    

