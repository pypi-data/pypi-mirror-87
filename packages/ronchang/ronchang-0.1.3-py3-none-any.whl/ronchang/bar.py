import os


class Bar:
    """
        Bar(count, amount, info=None, desc=None)

        :info: only display the first 10 letters.
        :desc: abbreviation for description.
    """
    _RESERVED_ROOM = 0
    _BAR_FG_UNIT = '🁢'
    _BAR_BG_UNIT = '🁣'
    _BAR_LENGTH = 15

    def __init__(self, count, amount, info=None, desc=None):
        self.count = count
        self.amount = amount
        self.info = info
        self.desc = desc

        self.validate()

        self.proceed_rate = self._get_proceed_rate()

        self._run()

    def validate(self):
        if not isinstance(self.count, int):
            error = f'[{"ERROR":8}]| Invalid type of "count": {self.count} {type(self.count)}'
            raise TypeError(error)
        if not isinstance(self.amount, int):
            error = f'[{"ERROR":8}]| Invalid type of "amount": {self.amount} {type(self.amount)}'
            raise TypeError(error)
        if self.count == 0 or self.amount == 0:
            error = f'[{"ERROR":8}]| count or amount cannot be 0'
            raise ValueError(error)
        if self.count > self.amount:
            warning = f'[{"WARNING":8}]| "count" is greater than "amount": {self.count} > {self.amount}'
            print(warning)

    @staticmethod
    def _get_console_width():
        try:
            console_width = os.get_terminal_size(0)[0]
        except:
            console_width = 76
        return console_width

    def _get_desc_length(self, bar, info, rate):
        bar_info_rate_length = len(bar) + len(info) + len(rate)
        desc_length = self._get_console_width() - bar_info_rate_length - self._RESERVED_ROOM
        return 0 if desc_length < 0 else desc_length

    def _get_proceed_rate(self):
        """
            self.amount 若小於 0 rate 或 self.count 大於 self.amount
            視作 100
        """
        if self.amount <= 0 or self.count > self.amount:
            return 100
        return self.count / self.amount * 100

    def _get_progress_bar(self):
        if self.proceed_rate > 100:
            return f'|{self._BAR_FG_UNIT * self._BAR_LENGTH}| '
        fg_length = int(self._BAR_LENGTH * self.proceed_rate / 100)
        bg_length = self._BAR_LENGTH - fg_length
        return f'|{self._BAR_FG_UNIT * fg_length}{self._BAR_BG_UNIT * bg_length}| '

    def _get_formatted_info(self):

        info = self.info.upper() if self.info else 'INFO'
        return f'[{info[:10]:<10}]| '

    def _get_formatted_desc(self, desc_length):
        desc = self.desc or f' {self.count:,} of {self.amount:,}'
        return f'{desc[:desc_length]:<{desc_length}}'

    def _get_formatted_rate(self):
        return f'[{self.proceed_rate:>6,.2f}%]'

    def _run(self):
        bar = self._get_progress_bar()
        info = self._get_formatted_info()
        rate = self._get_formatted_rate()
        desc = self._get_formatted_desc(desc_length=self._get_desc_length(bar, info, rate))
        print(f'\r{info}{rate}{bar}{desc}', end='', flush=True)
        if self.proceed_rate == 100:
            print('')

