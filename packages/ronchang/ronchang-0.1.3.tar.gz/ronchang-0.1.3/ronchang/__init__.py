# Copyright (c) 2020 Ron Chang. All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time
from pprint import pprint

from .timer import Timer
from .parser import Parser
from .bar import Bar


class Demo:

    @classmethod
    @Timer.interval(minutes=1)
    def Timer(cls, interval):
        """
        @Timer.interval(minutes=1)
        def demo_timer(interval):
            start = time.time()
            foo = 3
            while True:
                try:
                    print('Do something here')
                    100 / foo
                except Exception as e:
                    foo = 3
                    Timer(interval=interval, start=start, is_error=True, exception=e)
                    continue
                foo -= 1
                Timer(interval=1, start=start, EXTRA='Extra information goes here')
        """
        start = time.time()
        foo = 3
        while True:
            try:
                print(cls.Timer.__doc__)
                100 / foo
            except Exception as e:
                foo = 3
                Timer(interval=interval, start=start, is_error=True, exception=e)
                continue
            foo -= 1
            Timer(interval=1, start=start, EXTRA='Extra information goes here')

    @classmethod
    def Bar(cls):
        """
        amount = 147
        demo = '[THIS IS A DEMONSTRATION]'
        for count in range(1, amount+1):
            desc = f'{demo} | {count} of {amount}'
            Bar(count=count, amount=amount, desc=desc, info='test')
            time.sleep(0.01)
        """
        print(cls.Bar.__doc__)
        amount = 147
        demo = '[THIS IS A DEMONSTRATION]'
        for count in range(1, amount+1):
            desc = f'{demo} | {count} of {amount}'
            Bar(count=count, amount=amount, desc=desc, info='test')
            time.sleep(0.01)

