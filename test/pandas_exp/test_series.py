from operator import add, and_, eq, ge, gt, invert, le, lt, mul, ne, or_, sub, truediv, xor
from typing import Any, List
import pytest
from pandas_exp.series import QuantcoSeries
from pandas_exp.exception import QuantcoException

opreator_map = {
    add : "+",
    sub : "-",
    mul : "*",
    truediv : "/",
    ge: ">=",
    gt: ">",
    le: "<=",
    lt: "<",
    eq: "==",
    ne: "!=",
    and_: "&",
    or_: "|",
    xor: "^",
    invert: "~" 
}

@pytest.mark.parametrize("series_name, series, series_type",[
    ("Empty Series", [], type(None)),
    ("Int Series", [1,2,3], int),
    ("None Series", [None, None], type(None)),
    ("Float Series", [1.0,2.0,3.0], float),
    ("String Series", ["Test", "Test"], str),
    ("String series with None", [None, "Test", None, "Test", "None"], str)
])
def test_valid_series(series_name, series, series_type):
    # Given

    # When
    quantco_series = QuantcoSeries(series_list=series)
    
    # Then
    assert quantco_series.series == series
    assert quantco_series._type == series_type
    assert len(quantco_series) == len(series)
    assert repr(quantco_series) == f"QuantcoSeries(len={len(series)}, series={series}, type={series_type})"
    assert quantco_series.__str__() == f"QuantcoSeries(len={len(series)}, series={series}, type={series_type})"

@pytest.mark.parametrize("series_name, series, error_message",[
    ("None Series", None, "The series can't be None"),
    ("List of List", [[]], "The type of elements in the series are not allowed. The allowed types are: String, Boolean, Int and Float."),
    ("Mixed Series of type", [False, "Test", 1.2], "The elements in the series are not of same type."),
    ("Mixed Series with List", [1.0,[],3.0], "The type of elements in the series are not allowed. The allowed types are: String, Boolean, Int and Float."),
    ("Mixed Series with Int and Float", [1,2,3,4.0,5.0], "The elements in the series are not of same type.")
])
def test_invalid_series(series_name, series, error_message):
    # Given

    # When
    with pytest.raises(QuantcoException) as e:
        QuantcoSeries(series)
    
    # Then
    assert e.value.args[0] == error_message

@pytest.mark.parametrize("series_name, series, setter_attr, setter_value",[
    ("Test_Series", [False, True, None, True], "series", ["Test"]),
    ("Test_Series", ["Test, Test1"], "type", float)
])
def test_setter_for_series(series_name, series, setter_attr, setter_value):
    # Given
    quantco_series = QuantcoSeries(series)

    # When
    with pytest.raises(AttributeError) as e:
        setattr(quantco_series, setter_attr, setter_value)
    
    # Then
    assert e.value.args[0] == f"can't set attribute"

def valid_operations_on_series(series_name, series, operand, operators):
    # Given
    quantco_series = QuantcoSeries(series)

    for operator in operators:
        # When
        calculated_quantco_series = operator(quantco_series, operand)
        # Then
        assert len(calculated_quantco_series.series) == len(series)
        for i in range(len(series)):
            if type(operand) == list:
                assert calculated_quantco_series.series[i] == operator(series[i], operand[i])
            else:
                assert calculated_quantco_series.series[i] == operator(series[i], operand)

def invalid_operations_on_series(series_name:str, series:List[Any], operand:Any, operators:List[Any], exception_type:Exception, error_message:str):
    # Given
    quantco_series = QuantcoSeries(series)

    for operator in operators:
        # When
        with pytest.raises(exception_type) as e:
            operator(quantco_series, operand)
    
        # Then
        assert e.value.args[0] == error_message.format(operator_symbol=opreator_map.get(operator, None))


arithmetic_operation_list = [add, sub, mul, truediv]
@pytest.mark.parametrize("series_name, series, operand, operators",[
    ("Float series int operation", [1.0, 2.0, 3.0], 5, arithmetic_operation_list),
    ("Float series float operation", [1.0, 2.0, 3.0], 5.0, arithmetic_operation_list),
    ("Int series float operation", [1, 2, 3], 5.0, arithmetic_operation_list),
    ("Int series int operation  ", [1, 2, 3], 5, arithmetic_operation_list),
    ("Float series negative operation", [1.0, 2.0, 3.0], -5.0, arithmetic_operation_list),
    ("String series with String operation", ["Test, Test2"], "1", [add]),
    ("Empty list with int operation", [], 5, arithmetic_operation_list)
])
def test_valid_arithmetic_operations_on_series(series_name, series, operand, operators):
    valid_operations_on_series(series_name, series, operand, operators)

@pytest.mark.parametrize("series_name, series, operand, operators, exception_type, error_message",[
    ("Float series boolean operation", [1.0, 2.0, 3.0], True, arithmetic_operation_list, QuantcoException, "The type of provided input is not an int or float."),
    ("Float series string operation", [1.0, 2.0, 3.0], "Test", arithmetic_operation_list, QuantcoException, "The type of provided input is not an int or float."),
    ("String series float operation", ["Test", "Test1"], 2.0, arithmetic_operation_list, QuantcoException, "The operand type <class 'float'> is not compatible with the series type <class 'str'>."),
    ("String series None operation", ["Test", "Test1"], None, arithmetic_operation_list, QuantcoException, "The operand type <class 'NoneType'> is not supported."),
    ("Boolean series Boolean operation", [True, False, None], False, arithmetic_operation_list, QuantcoException, "Addition on the bool type is not supported."),
    ("Boolean series None operation", [True, False, None], None, arithmetic_operation_list, QuantcoException, "The operand type <class 'NoneType'> is not supported."),
    ("Empty list with None operation", [], None, arithmetic_operation_list, QuantcoException, "The operand type <class 'NoneType'> is not supported."),
    ("Float series with none int operation", [1.0, 2.0, 3.0, None], 2, arithmetic_operation_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'int'"),
    ("Float series with none float operation", [1.0, 2.0, 3.0, None], 2.0, arithmetic_operation_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'float'"),
    ("Int series with none int operation", [None, 1, 3, None], 2, arithmetic_operation_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'int'"),
    ("Int series with none float operation", [None, 1, 3, None], 2.0, arithmetic_operation_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'float'"),
    ("String series with String operation", ["Test", "Test2"], "1", [sub, truediv], TypeError, "unsupported operand type(s) for {operator_symbol}: 'str' and 'str'"),
    ("None series with String operation", [None, None], "1", [sub, truediv], TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'str'"),
    ("String series with String multiplication", ["Test", "Test2"], "1", [mul], TypeError, "can't multiply sequence by non-int of type 'str'"),
    ("None series with String multiplication", [None, None], "1", [mul], TypeError, "can't multiply sequence by non-int of type 'NoneType'"),
    ("None series with int operation", [None, None], 1, arithmetic_operation_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'int'")
])
def test_invalid_arithmetic_operations_on_series(series_name:str, series:List[Any], operand:Any, operators:List[Any], exception_type:Exception, error_message:str):
    invalid_operations_on_series(series_name, series, operand, operators, exception_type, error_message)

comparison_operator_list = [ge, gt, le, lt]
equality_comparison_operator_list = [ne]
@pytest.mark.parametrize("series_name, series, operand, operators",[
    ("Float series, comparison with int operation", [1.0, 2.0, 3.0], 5, comparison_operator_list + equality_comparison_operator_list),
    ("Float series, comparison with float operation", [1.0, 2.0, 3.0], 5.0, comparison_operator_list + equality_comparison_operator_list),
    ("Int series, commparison with float operation", [1, 2, 3], 5.0, comparison_operator_list + equality_comparison_operator_list),
    ("Int series, comparison with int operation", [1, 2, 3], 5, comparison_operator_list + equality_comparison_operator_list),
    ("Float series, comparison with negative operation", [1.0, 2.0, 3.0], -5.0, comparison_operator_list + equality_comparison_operator_list),
    ("String series, comparison with string operation", ["Test, Test2"], "1", comparison_operator_list + equality_comparison_operator_list),
    ("Empty list, comparison with int operation", [], 5, comparison_operator_list + equality_comparison_operator_list),
    ("Empty list, comparison with None operation", [], None, comparison_operator_list + equality_comparison_operator_list),
    ("Float series, comparison with boolean operation", [1.0, 2.0, 3.0], True, comparison_operator_list + equality_comparison_operator_list)
])
def test_valid_comparison_operations_on_series(series_name, series, operand, operators):
    valid_operations_on_series(series_name, series, operand, operators)

@pytest.mark.parametrize("series_name, series, other_series, expectation",[
    ("Float series with None, comparison with float list", [1.0, 2.0, 3.0, None], [1.0, 2.0, 3.0, None], True),
    ("Int series", [1, 2, 3, 4, None], [1, 2, 3, 4, None], True),
    ("None series comparison with None series", [None], [None], True),
    ("None series comparison with None series", [1.0, 2.0, 3.0, None], [1.0, 2.0, 4.0, None], False),
    ("None series comparison with None series", [1, 2, 3, None], [1, 2, 4, None], False),
    ("None series comparison with None series", [True, True], [True, None], False)
])
def test_valid_equality_on_series(series_name, series, other_series, expectation):
    # Given
    quantco_series = QuantcoSeries(series)
    other_quantco_series = QuantcoSeries(other_series)

    # When
    list_result = quantco_series == other_series
    series_result = quantco_series == other_quantco_series

    # Then
    assert list_result == expectation
    assert series_result == expectation

@pytest.mark.parametrize("series_name, series, other_series, exception, error_message",[
    ("String series with None, comparison with None operation", ["Test", "Test1", "Test", None], None, QuantcoException, "The operand list provided in not of type list or QuantcoSeries."),
    ("String series with None, comparison with Boolean operation", ["Test", "Test1", "Test", None], True, QuantcoException, "The operand list provided in not of type list or QuantcoSeries."),
    ("Series with None, comparison with None operation", [None, None, None, None], None, QuantcoException, "The operand list provided in not of type list or QuantcoSeries."),
    ("Float series with None, comparison with float list of different size", [1.0, 2.0, 3.0, None], [1.0, 2.0, 3.0, None, None], QuantcoException, "The length of series are not equal. The series are of length 4 and 5."),
    ("Float series with None, comparison with int list", [1.0, 2.0, 3.0, None], [1, 2, 3, None], QuantcoException, "The series types are not same. The series are of types: <class 'float'> and <class 'int'>."),
    ("Float series with None, comparison with String list", [1.0, 2.0, 3.0, None], ["1", None], QuantcoException, "The series types are not same. The series are of types: <class 'float'> and <class 'str'>."),
    ("Boolean series with None, comparison with string operation", [True, False, None], ["True", "False"], QuantcoException, "The series types are not same. The series are of types: <class 'bool'> and <class 'str'>."),
    ("String series with None, comparison with boolean series", ["True", "False", "True", "False", None], [True, True, True, True, True], QuantcoException, "The series types are not same. The series are of types: <class 'str'> and <class 'bool'>."),
    ("String series filtered with None", ["True", "False", "True", "False", None], [None, None, None, None, None], QuantcoException, "The series types are not same. The series are of types: <class 'str'> and <class 'NoneType'>."),
    ("None series", [None, None, None, None], [True, False, False, False], QuantcoException, "The series types are not same. The series are of types: <class 'NoneType'> and <class 'bool'>.")
])
def test_invalid_equality_on_series(series_name, series, other_series, exception, error_message):
    # Given
    quantco_series = QuantcoSeries(series)

    # When
    with pytest.raises(exception) as list_exception:
        quantco_series == other_series
    
    # Then
    assert list_exception.value.args[0] == error_message

@pytest.mark.parametrize("series_name, series, operand, operators, exception_type, error_message",[
    ("Float series, comparison with string operation", [1.0, 2.0, 3.0], "Test", comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'float' and 'str'"),
    ("String series, comparison with float operation", ["Test", "Test1"], 2.0, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'str' and 'float'"),
    ("String series, comparison with None operation", ["Test", "Test1"], None, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'str' and 'NoneType'"),
    ("Boolean series, comparison with Boolean operation", [True, False, None], False, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'bool'"),
    ("Boolean series, comparison with None operation", [True, False, None], None, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'bool' and 'NoneType'"),
    ("Float series with None, comparison with int operation", [1.0, 2.0, 3.0, None], 2, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'int'"),
    ("Float series with None, comparison with float operation", [1.0, 2.0, 3.0, None], 2.0, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'float'"),
    ("Int series with None, comparison with int operation", [None, 1, 3, None], 2, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'int'"),
    ("Int series with None, comparison with float operation", [None, 1, 3, None], 2.0, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'float'"),
    ("None series, comparison with String operation", [None, None], "1", comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'str'"),
    ("None series, comparison with int operation", [None, None], 1, comparison_operator_list, TypeError, "'{operator_symbol}' not supported between instances of 'NoneType' and 'int'")
])
def test_invalid_comparison_operations_on_series(series_name:str, series:List[Any], operand:Any, operators:List[Any], exception_type:Exception, error_message:str):
    invalid_operations_on_series(series_name, series, operand, operators, exception_type, error_message)

# Checking for boolean operation on the series
bitwise_binary_operator_list = [and_, or_, xor]

@pytest.mark.parametrize("series_name, series, operand, operators",[
    # Test cases for bitwise operators between integers. Follow the instructions in series.py to turn on this feature and uncomment the following lines for test cases.
    # ("Int series, bitwise binary operation with int", [1, 2, 3], [1, 2, 3], bitwise_binary_operator_list),
    # ("Int series, bitwise binary operation with boolean", [1, 2, 3], [True, False, True], bitwise_binary_operator_list),
    # ("Boolean series, bitwise binary operation with int", [True, False, True], [1, 2, 3], bitwise_binary_operator_list),
    ("Boolean series, bitwise binary operation with boolean", [True, False, True], [True, False, True], bitwise_binary_operator_list)
])
def test_valid_bitwise_binary_operations_on_series(series_name, series, operand, operators):
    valid_operations_on_series(series_name, series, operand, operators)

@pytest.mark.parametrize("series_name, series, operand, operators, exception_type, error_message",[
    # Comment out the following test cases if you have turned on bitwise operation on int.
    ("Int series, bitwise binary operation with int", [1, 2, 3], [1, 2, 3], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'int'> type series and <class 'int'> type operand list. The boolean operation work on only bool type series."),
    ("Int series, bitwise binary operation with boolean", [1, 2, 3], [True, False, True], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'int'> type series and <class 'bool'> type operand list. The boolean operation work on only bool type series."),
    ("Boolean series, bitwise binary operation with int", [True, False, True], [1, 2, 3], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'bool'> type series and <class 'int'> type operand list. The boolean operation work on only bool type series."),
    ("Float series, bitwise binary operation with int", [1.0, 2.0, 3.0], [1, 2, 3], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'int'> type operand list. The boolean operation work on only bool type series."),
    ("Float series, bitwise binary operation with float", [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'float'> type operand list. The boolean operation work on only bool type series."),
    ("Int series, bitwise binary operation with float", [1, 2, 3], [1.0, 2.0, 3.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'int'> type series and <class 'float'> type operand list. The boolean operation work on only bool type series."),
    ("Float series, bitwise binary operation with negative", [1.0, 2.0, 3.0], [-5.0,-3.0,-2.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'float'> type operand list. The boolean operation work on only bool type series."),
    ("String series, bitwise binary operation with string", ["Test, Test2"], ["1","-1"], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'str'> type series and <class 'str'> type operand list. The boolean operation work on only bool type series."),
    ("Float series, bitwise binary operation with boolean", [1.0, 2.0, 3.0], [True, False, True], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'bool'> type operand list. The boolean operation work on only bool type series."),
    ("String series, bitwise binary operation with boolean", ["1.0", "2.0", "3.0"], [True, False, True], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'str'> type series and <class 'bool'> type operand list. The boolean operation work on only bool type series."),
    ("String series, bitwise binary operation with float", ["1.0", "2.0", "3.0"], [1.0, 2.0, 3.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'str'> type series and <class 'float'> type operand list. The boolean operation work on only bool type series."),
    ("Boolean series, bitwise binary operation with boolean with different length", [True, False, True], [True, False, True, False], bitwise_binary_operator_list, QuantcoException, "The operand series or list provided is of length 4 and is not compatible for the operation with the list of length 3. Both the series length should be equal."),
    ("Boolean series, bitwise binary operation with boolean with different length", [True, False, True], [None, None, None, None], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'bool'> type series and <class 'NoneType'> type operand list. The boolean operation work on only bool type series."),
    ("Empty list, bitwise binary operation with int", [], [5], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'NoneType'> type series and <class 'int'> type operand list. The boolean operation work on only bool type series."),
    ("Empty list, bitwise binary operation with None", [], None, bitwise_binary_operator_list, QuantcoException, "The operand list provided in not of type list or QuantcoSeries."),
    ("Empty list, bitwise binary operation with empty list", [], [], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'NoneType'> type series and <class 'NoneType'> type operand list. The boolean operation work on only bool type series."),
    ("Empty list, bitwise binary operation with None", [None], [True], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'NoneType'> type series and <class 'bool'> type operand list. The boolean operation work on only bool type series."),
    ("Int series, bitwise binary operation with int", [1, 2, 3, None], [1, 2, 3, 4], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'int'> type series and <class 'int'> type operand list. The boolean operation work on only bool type series."),
    ("Int series, bitwise binary operation with boolean", [1, 2, 3, None], [True, False, True, False], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'int'> type series and <class 'bool'> type operand list. The boolean operation work on only bool type series."),
    ("Boolean series, bitwise binary operation with int", [True, False, True, None], [1, 2, 3, 4], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'bool'> type series and <class 'int'> type operand list. The boolean operation work on only bool type series."),
    ("Boolean series, bitwise binary operation with boolean", [True, False, True, None], [True, False, True, False], bitwise_binary_operator_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'bool'")
    # Uncomment the following test cases if you have turned on bitwise operation on int.
    # ("Float series, bitwise binary operation with int", [1.0, 2.0, 3.0], [1, 2, 3], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'int'> type operand list."),
    # ("Float series, bitwise binary operation with float", [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'float'> type operand list."),
    # ("Int series, bitwise binary operation with float", [1, 2, 3], [1.0, 2.0, 3.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'int'> type series and <class 'float'> type operand list."),
    # ("Float series, bitwise binary operation with negative", [1.0, 2.0, 3.0], [-5.0,-3.0,-2.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'float'> type operand list."),
    # ("String series, bitwise binary operation with string", ["Test, Test2"], ["1","-1"], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'str'> type series and <class 'str'> type operand list."),
    # ("Float series, bitwise binary operation with boolean", [1.0, 2.0, 3.0], [True, False, True], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'float'> type series and <class 'bool'> type operand list."),
    # ("String series, bitwise binary operation with boolean", ["1.0", "2.0", "3.0"], [True, False, True], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'str'> type series and <class 'bool'> type operand list."),
    # ("String series, bitwise binary operation with float", ["1.0", "2.0", "3.0"], [1.0, 2.0, 3.0], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'str'> type series and <class 'float'> type operand list."),
    # ("Boolean series, bitwise binary operation with boolean with different length", [True, False, True], [True, False, True, False], bitwise_binary_operator_list, QuantcoException, "The operand series or list provided is of length 4 and is not compatible for the operation with the list of length 3. Both the series length should be equal."),
    # ("Boolean series, bitwise binary operation with boolean with different length", [True, False, True], [None, None, None, None], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'NoneType'> type operand list. Either the operand list is empty or has all None values."),
    # ("Empty list, bitwise binary operation with int", [], [5], bitwise_binary_operator_list, QuantcoException, "The operand series or list provided is of length 1 and is not compatible for the operation with the list of length 0. Both the series length should be equal."),
    # ("Empty list, bitwise binary operation with None", [], None, bitwise_binary_operator_list, QuantcoException, "The operand list provided in not of type list or QuantcoSeries."),
    # ("Empty list, bitwise binary operation with empty list", [], [], bitwise_binary_operator_list, QuantcoException, "The boolean operations don't work on <class 'NoneType'> type operand list. Either the operand list is empty or has all None values."),
    # ("Empty list, bitwise binary operation with None", [None], [True], bitwise_binary_operator_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'bool'"),
    # ("Int series, bitwise binary operation with int", [1, 2, 3, None], [1, 2, 3, 4], bitwise_binary_operator_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'int'"),
    # ("Int series, bitwise binary operation with boolean", [1, 2, 3, None], [True, False, True, False], bitwise_binary_operator_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'bool'"),
    # ("Boolean series, bitwise binary operation with int", [True, False, True, None], [1, 2, 3, 4], bitwise_binary_operator_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'int'"),
    # ("Boolean series, bitwise binary operation with boolean", [True, False, True, None], [True, False, True, False], bitwise_binary_operator_list, TypeError, "unsupported operand type(s) for {operator_symbol}: 'NoneType' and 'bool'")
])
def test_invalid_bitwise_binary_operations_on_series(series_name, series, operand, operators, exception_type, error_message):
    invalid_operations_on_series(series_name, series, operand, operators, exception_type, error_message)

bitwise_uniary_operator_list = [invert]
@pytest.mark.parametrize("series_name, series, operators",[
    ("Boolean series, boolean uniary operation", [True, False, True], bitwise_uniary_operator_list),
    ("Empty list doesn't throw exception", [], bitwise_uniary_operator_list)
])
def test_valid_bitwise_uniary_operations_on_series(series_name, series, operators):
    # Given
    quantco_series = QuantcoSeries(series)

    for operator in operators:
        # When
        calculated_quantco_series = operator(quantco_series)

        # Then
        assert len(calculated_quantco_series.series) == len(series)
        for i in range(len(series)):
                assert calculated_quantco_series.series[i] == (not series[i])

@pytest.mark.parametrize("series_name, series, operators, exception_type, error_message",[
    ("Float series, boolean uniary operation", [1.0, 2.0, 3.0], bitwise_uniary_operator_list, QuantcoException, "The invert operation of the series with type <class 'float'> is not supported."),
    ("String series, boolean uniary operation", ["Test"], bitwise_uniary_operator_list, QuantcoException, "The invert operation of the series with type <class 'str'> is not supported."),
    ("None series, boolean uniary operation", [None, None, None], bitwise_uniary_operator_list, QuantcoException, "The invert operation of the series with type <class 'NoneType'> is not supported."),
    ("Int series, boolean uniary operation", [1, 2, 3], bitwise_uniary_operator_list, QuantcoException, "The invert operation of the series with type <class 'int'> is not supported."),
])
def test_invalid_bitwise_uniary_operations_on_series(series_name, series, operators, exception_type, error_message):
    # Given
    quantco_series = QuantcoSeries(series)

    for operator in operators:
        # When
        with pytest.raises(exception_type) as e:
            operator(quantco_series)
    
        # Then
        assert e.value.args[0] == error_message.format(operator_symbol=opreator_map.get(operator, None))

@pytest.mark.parametrize("series_name, series, filter, expectation",[
    ("Int series", [1, 2, 3, 4, None], [True, False, True, False, True], [1, 3, None] ),
    ("Float series", [1.0, 2.0, 3.0, 4.0, None], [True, True, True, True, False], [1.0, 2.0, 3.0, 4.0]),
    ("Boolean series", [True, False, True, False, None], [True, True, True, True, True], [True, False, True, False, None]),
    ("String series", ["True", "False", "True", "False", None], [True, True, True, True, True], ["True", "False", "True", "False", None]),
    ("String series filtered with None", ["True", "False", "True", "False", None], [None, None, None, None, True], [None]),
    ("None series", [None, None, None, None], [True, False, False, False], [None]),
    ("Int series", [1, 2, 3, 4, None, None], [True, False, True, False, True, None], [1, 3, None]),
    ("None series with None", [None, None, None, None], [None, None, None, None], []),
    ("Accessing through an int", [1, 2, 3, 4, None], 4, None)
])
def test_get_item_valid_series(series_name, series, filter, expectation):
    # Given
    quantco_series = QuantcoSeries(series)

    # When
    result = quantco_series[filter]

    # Then
    if type(result) == QuantcoSeries:
        assert result.series == expectation
    else:
        assert result == expectation

@pytest.mark.parametrize("series_name, series, filter, exception, error_message",[
    ("Int series filter with float", [True, False, True, False, None], [1.0, 2.0, 3.0, 4.0], QuantcoException, "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'float'>." ),
    ("Int series filter with int", [True, False, True, False, None], [1, 2, 3, 4, 5], QuantcoException, "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'int'>."),
    ("Boolean series filter with String", [True, False, True, False, None], ["True", "False", "True", "False", None], QuantcoException, "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'str'>."),
    ("Empty series", [], [True], QuantcoException, "The length of the series and the filter list/series is not equal."),
    ("Accessing through a map/set", [1, 2, 3, 4], {True, True, True, True}, QuantcoException, "Unsupported operation. Accessibility of the series could be performed only using an integer or list of boolean values."),
    ("Accessing through a float", [1, 2, 3, 4], 2.0, QuantcoException, "Unsupported operation. Accessibility of the series could be performed only using an integer or list of boolean values."),
    ("Accessing through array out of bound", [1, 2, 3, 4], 5, IndexError, "list index out of range")
])
def test_get_item_invalid_series(series_name, series, filter, exception, error_message):
    # Given
    quantco_series = QuantcoSeries(series)

    # When
    with pytest.raises(exception) as e:
        quantco_series[filter]

    # Then
    assert e.value.args[0] == error_message
