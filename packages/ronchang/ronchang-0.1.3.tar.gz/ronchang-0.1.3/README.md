# RonChang
### What is this?
This is my personal hands-on develop toolkits.
|name|popurse|
|-|-|
|Timer|colorful and expandable timer|

### How to install?
```bash
pip install ronchang
```

## 1. Timer
#### - import
```python
from ronchang import Timer
Timer(
    interval,  # unit: seconds
    start=None,
    is_error=False,
    exception=None,
    **kwargs
)
```
#### - demonstration
```python
from ronchang import Demo
Demo.Timer()
```

## 2. Slicer
#### - import
```python
from ronchang import Slicer
Slicer.list()
Slicer.dict()
Slicer.number()
```
#### - demonstration
```python
from ronchang import Demo
Demo.Slicer()
```

## 3. Bar
#### - import
```python
from ronchang import Bar
Bar(count, amount, desc=f'{count} of {amount}', info='INFO')
```
#### - demonstration
```python
from ronchang import Demo
Demo.Bar()
```
If you like my work, please consider buying me a coffee or [PayPal](https://paypal.me/RonDevStudio?locale.x=zh_TW)
Thanks for your support! Cheers! 🎉
<a href="https://www.buymeacoffee.com/ronchang" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" align="right"></a>
