from pandas_exp.exception import QuantcoException

class QuantcoSeries(object):
    allowed_data_types = {str, bool, int, float, type(None)}

    def __init__(self, series_list, **kwargs) -> None:
        self._series = series_list
        self._type = self.__check_type_of_each_element_same__(series_list)
    
    @property
    def series(self):
        return self._series
    
    @property
    def type(self):
        return self._type
    
    def __len__(self):
        return len(self._series)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(len={len(self)}, series={self._series}, type={self._type})"
    
    def __getitem__(self, access):
        if type(access) == int:
            return self._series[access]
        elif type(access) == list or type(access) == QuantcoSeries:
            return self.__filter_series__(QuantcoSeries.convert_to_quantco_series(access))
        else:
            raise QuantcoException(f"Unsupported operation. Accessibility of the series could be performed only using an integer or list of boolean values.")
    
    def __filter_series__(self, filter_list):
        if filter_list.type != bool and filter_list.type != type(None):
            raise QuantcoException(f"Unsupported operation. The filtering on the series works on bool type series/list. The provided type is {filter_list.type}.")
        if len(filter_list.series) != len(self._series):
            raise QuantcoException(f"The length of the series and the filter list/series is not equal.")
        return QuantcoSeries([self._series[i] for i in range(len(filter_list.series)) if filter_list.series[i]])

    def __check_type_of_each_element_same__(self, list_to_check, **kwargs):
        list_type = type(None)
        if list_to_check is None:
            raise QuantcoException(f"The series can't be None")
        if type(list_to_check) != list:
            raise QuantcoException(f"A valid list was not provided to construct the series.")
        for i in range(0, len(list_to_check)):
            if type(list_to_check[i]) not in self.allowed_data_types:
                raise QuantcoException(f"The type of elements in the series are not allowed. The allowed types are: String, Boolean, Int and Float.")
            if list_to_check[i] != None and i-1>=0 and list_to_check[i-1] != None and type(list_to_check[i-1]) != type(list_to_check[i]):
                raise QuantcoException(f"The elements in the series are not of same type.")
            if list_type == type(None) and list_to_check[i]!= None:
                list_type = type(list_to_check[i])

        return list_type

    # Arithmetic operations overloading:
    # Should work on Series operand also
    def __check_arithmetic_compatibility__(self, operand_type, **kwargs):
        arithmetic_types = {int, float}
        if operand_type == type(None):
            raise QuantcoException(f"The operand type {operand_type} is not supported.")
        if self._type in arithmetic_types:
            if operand_type not in arithmetic_types:
                raise QuantcoException("The type of provided input is not an int or float.")
        elif self._type == bool or operand_type == bool:
            raise QuantcoException("Addition on the bool type is not supported.")
        elif self._type != type(None) and operand_type != self._type:
            raise QuantcoException(f"The operand type {operand_type} is not compatible with the series type {self._type}.")

    def __add__(self, operand, **kwargs):
        self.__check_arithmetic_compatibility__(type(operand))
        return QuantcoSeries([elem + operand for elem in self._series])
    
    def __sub__(self, operand, **kwargs):
        self.__check_arithmetic_compatibility__(type(operand))
        return QuantcoSeries([elem - operand for elem in self._series])
    
    def __mul__(self, operand, **kwargs):
        self.__check_arithmetic_compatibility__(type(operand))
        return QuantcoSeries([elem * operand for elem in self._series])
    
    def __truediv__(self, operand, **kwargs):
        return self.__div__(operand)

    def __div__(self, operand, **kwargs):
        self.__check_arithmetic_compatibility__(type(operand))
        return QuantcoSeries([elem / operand for elem in self._series])
    
    # Comparison operations overloading:
    # Should work on Series operand also
    
    def __ge__(self, operand, **kwargs):
        return QuantcoSeries([elem >= operand for elem in self._series ])
    
    def __gt__(self, operand, **kwargs):
        return QuantcoSeries([elem > operand for elem in self._series ])
    
    def __le__(self, operand, **kwargs):
        return QuantcoSeries([elem <= operand for elem in self._series ])
    
    def __lt__(self, operand, **kwargs):
        return QuantcoSeries([elem < operand for elem in self._series ])
    
    def __ne__(self, operand, **kwargs):
        return QuantcoSeries([elem != operand for elem in self._series ])
    
    # List comptabile function overloading:
    def __check_list_compatibility__(self, operand_list, **kwargs):
        operand_list_type = operand_list.type
        if operand_list_type == float or self.type == float:
            raise QuantcoException(f"The boolean operations don't work on {self.type} type series and {operand_list_type} type operand list.")
        if operand_list_type == str or self.type == str:
            raise QuantcoException(f"The boolean operations don't work on {self.type} type series and {operand_list_type} type operand list.")
        if operand_list_type == type(None):
            raise QuantcoException(f"The boolean operations don't work on {operand_list_type} type operand list. Either the operand list is empty or has all None values.")
        if len(operand_list.series) != len(self._series):
            raise QuantcoException(f"The operand series or list provided is of length {len(operand_list.series)} and is not compatible for the operation with the list of length {len(self._series)}. Both the series length should be equal.")

    def __and__(self, operand, **kwargs):
        operand = QuantcoSeries.convert_to_quantco_series(operand)
        self.__check_list_compatibility__(operand)
        return QuantcoSeries([self._series[i] & operand.series[i] for i in range(len(self._series))])
    
    def __or__(self, operand, **kwargs):
        operand = QuantcoSeries.convert_to_quantco_series(operand)
        self.__check_list_compatibility__(operand)
        return QuantcoSeries([self._series[i] | operand.series[i] for i in range(len(self._series))])
    
    def __xor__(self, operand, **kwargs):
        operand = QuantcoSeries.convert_to_quantco_series(operand)
        self.__check_list_compatibility__(operand)
        return QuantcoSeries([self._series[i] ^ operand.series[i] for i in range(len(self._series))])
    
    def __invert__(self, **kwargs):
        if self._type == bool:
            return QuantcoSeries([not self._series[i] for i in range(len(self._series))])
        elif len(self._series) == 0:
            return QuantcoSeries(self._series)
        else:
            raise QuantcoException(f"The invert operation of the series with type {self._type} is not supported.")
    
    def __eq__(self, __o: object) -> bool:
        __o = QuantcoSeries.convert_to_quantco_series(__o)
        if __o.type != self.type:
            raise QuantcoException(f"The series types are not same. The series are of types: {self._type} and {__o.type}.")
        if len(__o.series) != len(self._series):
            raise QuantcoException(f"The length of series are not equal. The series are of length {len(self._series)} and {len(__o.series)}.")
        return __o.series == self._series
    
    def convert_to_quantco_series(__o:object, **kwargs):
        operand_list_type = type(__o)
        if operand_list_type != list and operand_list_type != QuantcoSeries:
            raise QuantcoException(f"The operand list provided in not of type list or QuantcoSeries.")
        if operand_list_type == list:
            __o = QuantcoSeries(__o)
        return __o
