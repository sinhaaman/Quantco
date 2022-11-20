from typing import Any, Dict, List, Union
from pandas_exp.exception import QuantcoException
from pandas_exp.series import QuantcoSeries


class QuantcoDataFrame(object):
    allowed_data_types = {str, bool, int, float, type(None)}

    def __init__(self, frame_dict:Dict[str, List[Union[str, bool, int, float]]]={}) -> None:
        self._frame = self.initialize_frame(frame_dict)
        print(f"Dataframe initialized with the size: {self.size()}")

    @property
    def frame(self):
        return self._frame
    
    def __getitem__(self, key):
        if type(key) == list or type(key) == QuantcoSeries:
            filter_series = QuantcoSeries.convert_to_quantco_series(key)
            new_frame = dict()
            for k,v in self._frame.items():
                new_frame[k] = v[filter_series]
            return QuantcoDataFrame(new_frame)

        return self._frame[key]
    
    def __len__(self):
        return len(self._frame.keys())
    
    def __repr__(self):
        return f"{self.__class__.__name__}(size={self.size()}, column_names={list(self._frame.keys())})"

    def initialize_frame(self, frame_dict:Dict[str, List[Any]]) -> Dict[str, QuantcoSeries]:
        frame = dict()
        try :
            if frame_dict != {}:
                self.__validate_frame_not_none__(frame_dict)
                self.__validate_frame__(frame_dict)
                frame = self.__construct_frame__(frame_dict)
                self.rows = len(frame_dict.values().__iter__().__next__())
                self.columns = len(frame_dict.keys())
            else:
                self.rows = 0
                self.columns = 0
            return frame
        except Exception as e:
            raise QuantcoException(f"The frame is malformed and couldn't be converted to a dataframe. The exception is: {e}")
    
    def __construct_frame__(self, frame_dict) -> Dict[str, QuantcoSeries]:
        frame = {}
        for k,v in frame_dict.items():
            if type(v) == QuantcoSeries:
                v = v.series
            frame[k] = QuantcoSeries(v)
        return frame

    def size(self):
        return self.rows,self.columns
    
    def __validate_frame_not_none__(self, frame_dict:Dict[str, List[Any]]):
        if frame_dict is None:
            raise QuantcoException("The frame dictionary can't be None")

    def __validate_frame__(self, frame_dict:Dict[str, List[Any]]):
        item1_k,item1_v = frame_dict.items().__iter__().__next__()
        for k,v in frame_dict.items():
            self.__check_key__(k)
            self.__check_series_none__(k,v)
            self.__check_length_of_list__(v, len(item1_v))
    
    def __check_length_of_list__(self, list_to_check, length) :
        if len(list_to_check) != length:
            raise QuantcoException("The length of the series are not equal.")
    
    def __check_key__(self, key):
        if key is None:
            raise QuantcoException("The name of the series can't be None.")
    
    def __check_series_none__(self, name_of_series, list_to_check):
        if list_to_check is None:
            raise QuantcoException(f"The series with name: {name_of_series} can't be None.")
