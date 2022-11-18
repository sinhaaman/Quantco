
from pandas_exp.dataframe import QuantcoDataFrame
from pandas_exp.exception import QuantcoException

import pytest

@pytest.mark.parametrize("data_frame, size", [
    ({

    }, (0,0)),
    ({
        'Name' : ["Test", "Test"],
        'Number': [0.1, 0.2]
    }, (2,2)),
    ({
        'Name' : ["Test", "Test2"],
        'Number' : [None, None]
    }, (2,2)),
    ({
        'Name' : ["Test", None],
        'Number': [0.1, 0.2]
    }, (2,2)),
    ({
        'Name' : ["Test", None],
        'Number': [0.1, None]
    }, (2,2)),
    ({
        'Name' : [],
        'Number': []
    }, (0,2)),
    ({
        'Name': ["Test", "None", "QuantCo", None],
        'Number': [1.2, 3.2, 55.2, 88.90]
    }, (4,2))   
])
def test_valid_quantcoframes(data_frame, size):
    # Given

    # When
    frame = QuantcoDataFrame(data_frame)

    # Then
    assert frame.size() == size
    assert len(frame) >= 0
    assert repr(frame) == f"QuantcoDataFrame(size={frame.size()}, column_names={list(data_frame.keys())})"
    assert frame.__str__() == f"QuantcoDataFrame(size={frame.size()}, column_names={list(data_frame.keys())})"

@pytest.mark.parametrize("data_frame, error_message", [
    (
        {
            'Test' : ["Test", "Test"],
            'Number': [0.1, 0.2, 0.3]
        }, 
        "The length of the series are not equal."
    ),
    (
        {
            None:[None]
        },
        "The name of the series can't be None."
    ),
    (
        {
            'Test':None
        },
        "The series with name: Test can't be None."
    ),
    (   {
            'Test' : ["Test", None],
            'Number': [0.1, "Test"]
        },
        "The elements in the series 'Number' are not of same type."
    ),
    (
        {
            'Test' : ["Test", "Test1"],
            'Number': [0.1, [0.1]]
        },
        "The type of elements in the series 'Number' are not allowed. The allowed types are: String, Boolean, Int and Float."
    ),
    (
        {
            'Test' : ["Test"],
            'Number': [[0.1]]
        },
        "The type of elements in the series 'Number' are not allowed. The allowed types are: String, Boolean, Int and Float."
    ),
    (
        {
            'Name' : [],
            'Number': [],
            'Size': [0.1]
        },
        "The length of the series are not equal."
    )
])
def test_invalid_quantcoframes(data_frame, error_message):
    # Given

    # When
    with pytest.raises(QuantcoException) as e:
        QuantcoDataFrame(data_frame)

    # Then
    assert e.value.args[0] == f"The frame is malformed and couldn't be converted to a dataframe. The exception is: {error_message}"

@pytest.mark.parametrize("data_frame", [
    ({

    }),
    ({
        'Name' : ["Test", "Test"],
        'Number': [0.1, 0.2]
    }),
    ({
        'Name' : ["Test", "Test2"],
        'Number' : [None, None]
    }),
    ({
        'Name' : ["Test", None],
        'Number': [0.1, 0.2]
    }),
    ({
        'Name' : ["Test", None],
        'Number': [0.1, None]
    }),
    ({
        'Name' : [],
        'Number': []
    }),
    ({
        'Name': ["Test", "None", "QuantCo", None],
        'Number': [1.2, 3.2, 55.2, 88.90]
    })   
])
def test_setters_for_quantcoframes(data_frame):
    # Given
    frame = QuantcoDataFrame(data_frame)

     # When
    with pytest.raises(AttributeError) as e:
        frame.frame = {
        'Name' : ["Test", None],
        'Number': [0.1, None]
    }

    # Then
    assert e.value.args[0] == "can't set attribute"

@pytest.mark.parametrize("data_frame, series_name, expected_series", [
    ({
        'Name' : ["Test", "Test"],
        'Number': [0.1, 0.2]
    }, "Name", ["Test", "Test"]),
    ({
        'Name' : ["Test", "Test2"],
        'Number' : [None, None]
    }, "Number", [None, None]),
    ({
        'Name' : ["Test", None],
        'Number': [0.1, 0.2]
    }, "Name", ["Test", None]),
    ({
        'Name' : [],
        'Number': []
    }, "Name", []),
    ({
        'Name': ["Test", "None", "QuantCo", None],
        'Number': [1.2, 3.2, 55.2, 88.90]
    }, "Number", [1.2, 3.2, 55.2, 88.90])   
])
def test_valid_read_operator_for_quantcoframes(data_frame, series_name, expected_series):
    # Given
    quantoco_dataframe = QuantcoDataFrame(data_frame)

    # When
    result = quantoco_dataframe[series_name]

    # Then
    assert result.series_name == series_name
    assert len(result.series) == len(expected_series)
    for i in range(len(expected_series)):
        assert result.series[i] == expected_series[i]

@pytest.mark.parametrize("data_frame, series_name, exception, error_message", [
    ({

    }, None, KeyError, None),
    ({

    }, "None", KeyError, "None"),
    ({
        'Name' : ["Test", "Test"],
        'Number': [0.1, 0.2]
    }, "Name1", KeyError, "Name1"),
    ({
        'Name' : [],
        'Number': []
    }, "Name1", KeyError, "Name1")
])
def test_invalid_read_operator_for_quantcoframes(data_frame, series_name, exception, error_message):
    # Given
    quantoco_dataframe = QuantcoDataFrame(data_frame)

    # When
    with pytest.raises(exception) as e:
        quantoco_dataframe[series_name]

    # Then
    assert e.value.args[0] == error_message
