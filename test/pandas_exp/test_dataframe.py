
from pandas_exp.dataframe import QuantcoDataFrame
from pandas_exp.exception import QuantcoException

import pytest

from pandas_exp.series import QuantcoSeries

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
        "The elements in the series are not of same type."
    ),
    (
        {
            'Test' : ["Test", "Test1"],
            'Number': [0.1, [0.1]]
        },
        "The type of elements in the series are not allowed. The allowed types are: String, Boolean, Int and Float."
    ),
    (
        {
            'Test' : ["Test"],
            'Number': [[0.1]]
        },
        "The type of elements in the series are not allowed. The allowed types are: String, Boolean, Int and Float."
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

@pytest.mark.parametrize("data_frame, series_list, expected_dict, expected_size", [
    (
        {
            'Name' : ["Test", "Test"],
            'Number': [0.1, 0.2]
        }, 
        [True, True],
        {
            'Name' : ["Test", "Test"],
            'Number': [0.1, 0.2]
        },
        (2,2)
    ),
    (
        {
            'Name' : ["Test", "Test2"],
            'Number' : [None, None]
        }, 
        [True, False],
        {
            'Name' : ["Test"],
            'Number' : [None]
        },
        (1,2)
    ),
    (
        {
            'Name' : ["Test", None],
            'Number': [0.1, 0.2]
        }, 
        [False, False],
        {
            'Name' : [],
            'Number': []
        },
        (0,2)
    ),
    (
        {
            'Name': ["Test", "None", "QuantCo", None],
            'Number': [1.2, 3.2, 55.2, 88.90]
        }, 
        [True, None, False, True],
        {
            'Name': ["Test", None],
            'Number': [1.2, 88.90]
        },
        (2,2)
    ),
    (
        {
            'Name': [False, None, None, False],
            'Number': [1.2, 3.2, 55.2, None]
        },
        [True, None, True, True],
        {
            'Name': [False, None, False],
            'Number': [1.2, 55.2, None]
        },
        (3,2)
    ),
    (
        {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }, 
        [None, None, None, None],
        {
            'Name': [],
            'Number': []
        },
        (0,2)
    ),  
    (
        {
            'Name' : ["Test", "Test"],
            'Number': [0.1, 0.2]
        }, 
        QuantcoSeries([True, True]),
        {
            'Name' : ["Test", "Test"],
            'Number': [0.1, 0.2]
        },
        (2,2)
    ),
    (
        {
            'Name' : ["Test", "Test2"],
            'Number' : [None, None]
        }, 
        QuantcoSeries([True, False]),
        {
            'Name' : ["Test"],
            'Number' : [None]
        },
        (1,2)
    ),
    (
        {
            'Name' : ["Test", None],
            'Number': [0.1, 0.2]
        }, 
        QuantcoSeries([False, False]),
        {
            'Name' : [],
            'Number': []
        },
        (0,2)
    ),
    (
        {
            'Name': ["Test", "None", "QuantCo", None],
            'Number': [1.2, 3.2, 55.2, 88.90]
        }, 
        QuantcoSeries([True, None, False, True]),
        {
            'Name': ["Test", None],
            'Number': [1.2, 88.90]
        },
        (2,2)
    ),
    (
        {
            'Name': [False, None, None, False],
            'Number': [1.2, 3.2, 55.2, None]
        },
        QuantcoSeries([True, None, True, True]),
        {
            'Name': [False, None, False],
            'Number': [1.2, 55.2, None]
        },
        (3,2)
    ),
    (
        {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }, 
        QuantcoSeries([None, None, None, None]),
        {
            'Name': [],
            'Number': []
        },
        (0,2)
    )   
])
def test_valid_read_operator_with_list_for_quantcoframes(data_frame, series_list, expected_dict, expected_size):
    # Given
    quantoco_dataframe = QuantcoDataFrame(data_frame)

    # When
    result = quantoco_dataframe[series_list]

    # Then
    assert type(result) == QuantcoDataFrame
    assert result.size() == expected_size
    for k,v in result.frame.items():
        assert result[k].series == expected_dict[k]

@pytest.mark.parametrize("data_frame, series_list, exception, error_message",[
    (
        {
            'Name' : [],
            'Number': []
        }, 
        QuantcoSeries([None, None]),
        QuantcoException,
        "The length of the series and the filter list/series is not equal."
    ),
    (
        {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }, 
        QuantcoSeries([2,1,1,1]),
        QuantcoException,
        "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'int'>."
    ),
    (
        {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }, 
        QuantcoSeries(["2","1","1"]),
        QuantcoException,
        "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'str'>."
    ),
    (
        {
            'Name' : [],
            'Number': []
        }, 
        [None, None],
        QuantcoException,
        "The length of the series and the filter list/series is not equal."
    ),
    (
        {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }, 
        [2,1,1,1],
        QuantcoException,
        "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'int'>."
    ),
    (
        {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }, 
        ["2","1","1"],
        QuantcoException,
        "Unsupported operation. The filtering on the series works on bool type series/list. The provided type is <class 'str'>."
    ),
])
def test_invalid_read_operator_with_list_for_quantcoframes(data_frame, series_list, exception, error_message):
    # Given
    quantoco_dataframe = QuantcoDataFrame(data_frame)

    # When
    with pytest.raises(exception) as e:
        quantoco_dataframe[series_list]

    # Then
    assert e.value.args[0] == error_message