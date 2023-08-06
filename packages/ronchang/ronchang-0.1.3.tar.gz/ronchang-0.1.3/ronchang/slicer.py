from .cyn.slicer import proceed_dict, proceed_list, proceed_pages


class Slicer:
    """
    How to use:
        Slicer.split_list(input_data, slice_length=None, container_length=None, recurs=True)

        - input_data

        - recurs
          True (Default)

        - slice_length
            Each slice number

        - container_length
            As a container maximum number, approach as possible as it could be.

        Run this file directly with python to see how it goes with 3 different demonstrations!
    """

    @staticmethod
    def _proceed_pages(amount, slice_length):
        result = list()
        temp = list()
        for page in range(1, amount+1):
            temp.append(page)
            if page % slice_length == 0:
                result.append(temp.copy())
                temp.clear()
        if temp:
            result.append(temp)
        return result

    @staticmethod
    def _proceed_dict(input_data, slice_length):
        result = list()
        temp = dict()
        for index, (tier_id, info) in enumerate(input_data.items(), start=1):
            temp.update({str(tier_id): info})
            if index % slice_length == 0:
                result.append(temp.copy())
                temp.clear()
        if temp:
            result.append(temp)
        return result

    @staticmethod
    def _proceed_list(input_data, slice_length):
        result = list()
        temp = list()
        for index, data in enumerate(input_data, start=1):
            temp.append(data)
            if index % slice_length == 0:
                result.append(temp.copy())
                temp.clear()
        if temp:
            result.append(temp)
        return result

    @staticmethod
    def _get_slice_length(amount, container_length):
        if amount % container_length == 0:
            return amount // container_length
        return amount // container_length + 1

    @staticmethod
    def _validation(input_data, slice_length, container_length):
        if type(input_data) not in [list, dict, type(dict().keys()), type(dict().values())]:
            raise TypeError(f'Invalid input_data type {input_data} {type(input_data)}')
        if not (slice_length or container_length):
            raise ValueError(f'Input at least one control number!')
        if slice_length and container_length:
            raise ValueError(f'Accept only one control number!')
        if not (isinstance(slice_length, int) or slice_length is None):
            raise ValueError(f'Invalid "slice_length" value :{slice_length}')
        if not (isinstance(container_length, int) or container_length is None):
            raise ValueError(f'Invalid "container_length" value :{container_length}')
        return True

    @classmethod
    def reduce_dimension(cls, input_data):
        if not isinstance(input_data, list):
            return input_data
        result = list()
        for data in input_data:
            temp = cls.reduce_dimension(data)
            if isinstance(temp, list):
                result.extend(temp)
            else:
                result.append(temp)
        return result

    @classmethod
    def list(cls, input_data, slice_length=None, container_length=None, recurs=True):
        if not input_data:
            return list()
        cls._validation(
            input_data=input_data,
            slice_length=slice_length,
            container_length=container_length
        )
        if recurs:
            input_data = cls.reduce_dimension(input_data=input_data)
        if slice_length:
            return cls._proceed_list(input_data=input_data, slice_length=slice_length)
        if container_length:
            amount = len(input_data)
            slice_length = cls._get_slice_length(amount=amount, container_length=container_length)
            return cls._proceed_list(input_data=input_data, slice_length=slice_length)

    @classmethod
    def clist(cls, input_data, slice_length=None, container_length=None, recurs=True):
        if not input_data:
            return list()
        cls._validation(input_data=input_data, slice_length=slice_length, container_length=container_length)
        if recurs:
            input_data = cls.reduce_dimension(input_data=input_data)
        if slice_length:
            return proceed_list(input_data=input_data, slice_length=slice_length)
        if container_length:
            amount = len(input_data)
            slice_length = cls._get_slice_length(amount=amount, container_length=container_length)
            return proceed_list(input_data=input_data, slice_length=slice_length)

    @classmethod
    def dict(cls, input_data, slice_length=None, container_length=None):
        if not input_data:
            return dict()
        cls._validation(
            input_data=input_data,
            slice_length=slice_length,
            container_length=container_length
        )
        if slice_length:
            return cls._proceed_dict(input_data=input_data, slice_length=slice_length)
        if container_length:
            amount = len(input_data)
            slice_length = cls._get_slice_length(amount=amount, container_length=container_length)
            return cls._proceed_dict(input_data=input_data, slice_length=slice_length)

    @classmethod
    def cdict(cls, input_data, slice_length=None, container_length=None):
        if not input_data:
            return dict()
        cls._validation(
            input_data=input_data,
            slice_length=slice_length,
            container_length=container_length
        )
        if slice_length:
            return proceed_dict(input_data=input_data, slice_length=slice_length)
        if container_length:
            amount = len(input_data)
            slice_length = cls._get_slice_length(amount=amount, container_length=container_length)
            return proceed_dict(input_data=input_data, slice_length=slice_length)

    @classmethod
    def number(cls, number, slice_length=None, container_length=None):
        slice_page_container = list()
        temp = list()
        if isinstance(number, int) or (isinstance(number, str) and number.isdigit()):
            amount = int(number)
            if slice_length:
                return cls._proceed_pages(amount=amount, slice_length=slice_length)
            if container_length:
                slice_length = cls._get_slice_length(amount=amount, container_length=container_length)
                return cls._proceed_pages(amount=amount, slice_length=slice_length)
        raise Exception(f'Invalid input_data type {input_data} {type(input_data)}, "int" is required!')

    @classmethod
    def cnum(cls, number, slice_length=None, container_length=None):
        slice_page_container = list()
        temp = list()
        if isinstance(number, int) or (isinstance(number, str) and number.isdigit()):
            amount = int(number)
            if slice_length:
                return proceed_pages(amount=amount, slice_length=slice_length)
            if container_length:
                slice_length = cls._get_slice_length(amount=amount, container_length=container_length)
                return proceed_pages(amount=amount, slice_length=slice_length)
        raise Exception(f'Invalid input_data type {input_data} {type(input_data)}, "int" is required!')
