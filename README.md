# [QuantCo Programming Challenge](./QuantCo_Programming_Challenge.pdf)

This programming challenge consists of creating the following custom data types/structures:
1. QuantcoDataFrame
2. QuantcoSeries

The aim of the challenge is to fail fast (using exceptions) in case of unknown values as compared to Pandas dataframe.

## Language
The language used for this repository is Python 3.9.13. The project has not been tested to be compatible with other Python versions.

## Repository Structure
The repository consist of the following folders and files:
| S.No |            Files/Folder           |                             Description                            |
|:----:|:---------------------------------:|:------------------------------------------------------------------:|
|   1  |           src/pandas_exp          |  contains the source code for the pandas experimentation project.  |
|   2  |          test/pandas_exp          |   contains the test code for the pandas experimentation project.   |
|   3  |       test/requirements-test.txt       | contains the dependencies needed to be installed to run the tests. |
|   4  |              .vscode/             |              vscode related settings for the project.              |
|   5  |                .env               |                    vscode env to run the the project.                   |
|   6  | QuantCo_Programming_Challenge.pdf |            The pdf containing the programming challenge.           |

## Running the Project:
Please use Python 3.9.13 to use this project. However, this is not tested with other python versions.
### Source code:
* Source code is written under the [src directory and pandas_exp package](./src/pandas_exp/).
### Test code:
* There are tests written under the [test directory and pandas_exp package](./test/pandas_exp/).
* The tests are written for dataframes, series, and the example provided in the [programming challenge](./QuantCo_Programming_Challenge.pdf).
* We use the [pytest framework](https://docs.pytest.org/en/7.2.x/) to test this project.
### Running via VS Code:
You can open the project using VSCode.
1. Install VScode and open the project.
1. You can create a venv or use your installed python to run it.
    1. To create your venv, go to the project directory and use the following command:
        ```bash
        python3 -m venv ./venv
        ```
1. In vscode, press cmd + Shift + P and choose Python: Select Interpreter.
1. Point it to the venv or the python interpreter that you wish to use.
1. With this project, vscode settings and launch configurations are shipped.
1. You can write any program that you want in [init file](./src/pandas_exp/__init__.py) and then run the project using the run button over the file.
1. You can see your desired result.

#### Testing the code via VS Code
In order to run the tests from vscode:
1. With this project, settings and env file are provided. This is used to configure pytest.
1. Change your present working directory to the project directory.
1. Once you haveg set-up the python environment as mentioned in the above section, you would need to be in an active python environment. If you are using venv then please use the following command to activate the python environment.
    ```
    source ./venv/bin/activate
    ```
1. Please use the following command to install pytest in your environment.
    ```
    pip3 install -r ./test/requirements-test.txt
    ```
1. Go to the testing tab and you can see a test explorer from where you can run or debug your tests.

### Running via Command Line:
1. Make sure that you are in an active python environment. If you are using venv then please use the following command to activate the python environment.
    ```
    source ./venv/bin/activate
    ```
1. Please use the following command to set-up your python path in your environment.
    ```
    export PYTHONPATH <PATH_TO_YOUR_SRC>:<PATH_TO_YOUR_TEST>
    ```
    e.g.
    ```
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src:$(pwd)/test
    ```
    For reference please see the [.env file](./.env). It assumes that you are using a virtual environment and you are in the project directory in vscode.
1. Write your script in [init.py](./src/pandas_exp/__init__.py) and simply run your custom script using the command.
    ```
    python3 ./src/pandas_exp/__init__.py
    ```
#### Testing the code via Command Line
1. Change your present working directory to the project directory.
1. Once you have set-up the python environment as mentioned in the above section, you would need to be in an active python environment. If you are using venv then please use the following command to activate the python environment.
    ```
    source ./venv/bin/activate
    ```
1. Please use the following command to install pytest in your environment.
    ```
    pip3 install -r ./test/requirements-test.txt
    ```
1. From the command line run:
    ```
    pytest ./test
    ```

# Custom Data Structures using the project:
## 1. QuantcoDataFrame

Source code is written under [dataframe.py](./src/pandas_exp/dataframe.py). Test code is written under [test_dataframe.py](./test/pandas_exp/test_dataframe.py).

### Creating the frame
---
Allowed frames:
1. Empty Dataframe = {}. 
2. Dataframes with only column name and 0 rows = {'SKU':[]}.

### Setting the frame
---
Setters of the frame are disabled. But if client want to set using the " _ " variables then, python would not restrict it, but it is highly encouraged to follow the convention of not setting the values if the variable is preceeded with " _ " sign.

### Operations on the frame
---
1. DataFrame as a table with named columns, each of these columns is called Series, and in our case explicitly only holds values of a certain type (and the None value).
    * Implemented using dict of str and QuantcoSeries. QuantcoSeries can hold the following types: [int, bool, str, float] along with None values.
1. A DataFrame only holds one Series for each string name, but
there generally can be any number of Series in a DataFrame, with the limitation, that each Series has to have the same number of elements.
    * Using the QuantcoDataframe, you can store N columns and each column is a series of same length.
1. Finally, you should build the DataFrame itself, which gets a dictionary of Series in its constructor, where it has to perform the necessary checks, and additionally provides square bracket access either when given a string returning the respective Series, or when given a boolean Series returns another DataFrame containing only the rows with True values.
    * The constructor takes in a dictionary and performs the necessary checks.
    * It provides the square bracket access. For a provided string, it returns the respective series and for a provided boolean series, it returns another DataFrame containing only the rows with True values.  
1. It could also be helpful to add print operations/a string representation to both DataFrame and Series.
    * The python function __repr__ is overloaded in both dataframe and series. e.g. For the following data frame
        ```python
        {
            'SKU' : ["X4E", "T3B", "F8D", "C7X"],
            'price' : [7.0, 3.5, 8.0, 6.0],
            'sales' : [5, 3, 1, 10],
            'taxed' : [False, False, True, False]
        }
        ```
        In case of:
        1. Dataframe - The output for a print or string representation is: 
            ```python
            QuantcoDataFrame(size=(4, 4), column_names=['SKU', 'price', 'sales', 'taxed'])
            ```
        1. Series - The output for a print or string representation is:
            ```python
            QuantcoSeries(len=4, series=['X4E', 'T3B', 'F8D', 'C7X'], type=<class 'str'>)
            ```


## 2. QuantcoSeries
Source code is written under [series.py](./src/pandas_exp/series.py). Test code is written under [test_series.py](./test/pandas_exp/test_series.py).

### Creating the series
---
QuantoSeries can be constructed using ```QuantoSeries([1, 2, 3, 4, None])```. The type checks are performed and it throws a QuantcoException if the type of elements are not same.
### Setting the series
---
Setters of the series are disabled. But if client want to set using the " _ " variables then, python would not restrict it, but it is highly encouraged to follow the convention of not setting the values if the variable is preceeded with " _ " sign.
### Operations on the series
---
1. There are different types of Series, in this case a Series containing only string elements (and None), a boolean Series (with values True, False and None) and different numeric Series, namely one for floating point values and one for integer.
    * QuantcoSeries can hold the following types: ```[int, bool, str, float]```. Each series is capable of holding None values. QuantcoSeries determines the data type of each series passed to it. In the beginning it assumes the type of the series is NoneType, but once any element of the allowed type arises it changes the type to that element and sets the type of the series to it. e.g. ```[None, None, None]```, ```[]``` is a valid quantco series with type NoneType, ```[None, None, None, 3.0]``` is a valid quantco series with type int, and ```[None, None, None, 3.0, "Harry"]``` is an invalid series.
1. In contrast to Pandas, we would rather fail hard and fast than having weird results, meaning you are supposed to raise exceptions for any kind of operations between Series of different types (unless explicitly mentioned otherwise) and if the lengths do not match.
    * Exceptions are raised as QunatcoException, for any kind of operations between Series of different types (unless explicitly mentioned otherwise) and if the lengths do not match.
1. Generally a Series is constructed by handing it a list of the elements it is supposed to contain (and it should obviously perform a type check if all values conform to the created Series type or are None)
    * QuantoSeries can be constructed using ```QuantoSeries([1, 2, 3, 4, None])```. The type checks are performed and it throws a QuantcoException if the type of elements are not same.
1.  To limit the scope we only ask you to implement read access, by overriding the square bracket access operator, which should when given an integer return the individual value at that position, and when given a boolean Series, a new Series with all rows/values where the boolean Series is True.
    * This is implemented as per the given description. On any QuantcoSeries, if the read operation contains a number 'i', we return the element at position i, given that the index i is a valid index. If a boolean list is provided, we return the elements of the series for which the boolean series value is True. Corresponding values for None and False are removed.
1.  For all Series types you should implement the equality operation, which should fail hard if the Series types or lengths are different and otherwise perform an element-wise comparison returning a boolean Series.
    * This is implemented as per the instruction. Note that ```[1.0]``` and ```[1]``` are different due to their type. In this case we fail hard and raise an exception instead of returning False. In all cases, we return a new series, without modifying the current series.
1. Additionally, the boolean Series should support element-wise and, or, xor and invert operations.
    * These element wise and, or, xor and invert operations are equivalent to &,|,^ and ~ operators, where the first three are binary operators and the invert operation is a uniary operator. Note that only boolean series is given the capability to perform the operation. In all the other cases, the overridden operator would throw an exception.
1. Both numeric Series types should support element-wise math operations (+, -, *, /), and inequalities (>,<,>=,<=,!=), returning a boolean Series. All of these operations should return new Series instead of modifying the existing one.
    * This is taken care of, and we can define the arithmetic and comparison operations between the series. The result type is a new QuantcoSeries.
1. As a form of syntactic sugar, all these operations should also work when being handed an individual value on the right side, where it would be expanded automatically to a Series of its respective type and the same length as the other Series.
    * The syntatic sugar is also implemented as per the given specification.

## 3. QuantcoException
Source code is written under [series.py](./src/pandas_exp/series.py).

# Assumptions and Improvements
The following section talks about the assumptions taken while creating the project and the features which could also be taken into account in order to extend this project. For the sake of readability and operation, some features, which are implemented, are enabled and some features are disabled.
## Assumptions:
---
While completing the task, I have made the following assumptions:
1. A special NoneType series is a special type in the series, where all the elements are None or the series is empty. e.g. ``` [None, None, None]```, ```[]``` is a valid series of type NoneType.
1. Arithmetic operation such as +,-,*,/ are allowed on empty QuantcoSeries, ```[]```. e.g. ```[]``` * 5 would give you ```[]``` as a result, however, ```[None] * 5``` would give you error.
1. String addition is supported i.e. ```["Test1, Test2"] + "1"``` would give you ```["Test11", "Test21"]```, however, multiplication division and subtraction is not supported on strings.
1. The read access operator would work with Boolean series and the NoneType series too. So, if ```a = [1.2, 3.2]``` and ```a[[None, None]]``` is passed then it would result in ```[]``` series as it satisfies the constraint "a new series with all rows/values where the boolean series is True.
1. Float and int series type can have arithmetic operations interchangably.
1. For a dataframe, if the read access operator has a None list, it is supported. The result would however be ```[]```. e.g.
    ```python
        df = {
            'Name' : ["Test", "Test1", "Test2", None],
            'Number': [23.0, 34.8, 32.78, 98.343]
        }
        filter_list = [None, None, None, None]
        result = df[filter_list]
        df['Name'] 
        # Prints QuantcoSeries(len=0, series=[], type=<class 'NoneType'>)
        df['Number'] 
        # Prints QuantcoSeries(len=0, series=[], type=<class 'NoneType'>)

    ```
## Improvements:
---
### Feature improvements
1. String "+" operator - Implemented in the project.
2. String inequalities - Implemented in the project.
3. Bitwise operators could be improved. Int datatype do support bitwise operators so we can have bitwise '&' operation with int - e.g. 
    1. ```[1, 2, 3] & [1, 2, 3]```
    2. ```[1, 2, 3] & [True, False, True]```
    3. ```[True, False, True] & [1, 2, 3]```

        For the sake of complexity and human readable result, this feature is implemented but commented out. Follow instructions in [series.py](./src/pandas_exp/series.py) *check_boolean_operator_compatibility* function and [test_series.py](./test/pandas_exp/test_series.py) *test_valid_bitwise_binary_operations_on_series* and *test_invalid_bitwise_binary_operations_on_series* functions.
4. Operators between series are implemented to work with both **list** and **QuantcoSeries** type objects when provided in the right side (right operand) of the equation. This **list** could be treated as a syntactic sugar.
5. Arithmetic operators could be enabled to work on the None list as the right operand. e.g. ```[] + 5``` could return ```[]```. This is implemented but currenty this feature is disabled, in order to enable the feature, follow the instructions in the [series.py](./src/pandas_exp/series.py) *check_arithmetic_compatibility* function and [test_series.py](./test/pandas_exp/test_series.py) *test_valid_arithmetic_operations_on_series* and *test_invalid_arithmetic_operations_on_series*.
6. Float and Int type series could perform arithmetic operation between each other. e.g. ```[1, 2, 3] + [1.0, 2.0, 3.0]``` is valid. This is implemented in the project.

### Performance improvements
1. Current dataframe takes O(mn) time to create a frame from a provided dict, where n is the size of each of series and m being the number of series. Given the nature of problem, all the series are independent of each other and O(mn) time is taken in order to check the type of each element of the series, we could do the following to improve the time complexity of the constructor of the frame:
    1. Fail fast, if the lengths of series are not equal - O(m) time, given m is the number of series.
    2. For each series, given the number of usable processors are 'p'. We would divide them in batches and pass them to each processor.
    3. If any of the series throws an exception, the constructor would throw an error.
    4. This way the performance could be reduced to O(mn/min(m,p)) from O(mn), where n is the size of each of series, m being the number of series and p is the number of usable processor.
1. Space complexity can be improved for operations on the series when using syntactic sugar for arithmetic and inequation operators. We need not need to expand the series in that case if we identified that the type of the series and the right operand is same. e.g. 
    ```python
    x = [1,2,3] + 5
    ```
    we don't need to expand 5 to create a series of [5, 5, 5] and then perform the operation as stated in the problem statement. Formally, given a series of length n, the space and time complexity could be saved by o(m) for not expanding the series. Then the operations take place with o(n) complexity and the new series is returned with o(m) complexity. So, we would save space from o(2m) to o(m) but still the Big O complexity would remain same i.e. O(m).