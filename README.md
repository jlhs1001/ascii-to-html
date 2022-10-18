![# ascii_to_html](https://github.com/jlhs1001/ascii-to-html/blob/main/data/logo.png?raw=true)

-- Made by Liam Seewald

> ## HTML-ify your ASCII with ease and elegance. _Now with optimization!_


### Getting Started


### Install!

```commandline
pip install ascii_to_html
```

### Import, Initialize!
```python
from ascii_to_html import AsciiConverter

converter = AsciiConverter(insert_nbsp=True, inline_css=False)

# Hey! Make sure to grab a copy of the css data if you
# don't plan on using inline css: 
AsciiConverter.generate_css()
```

### Execute, Enjoy!
```python
converter.to_html("\x1b[32;4mascii_to_html\x1b[0m")
```

---
## About optimization

### Yes, we optimize!

> ascii_to_html will toss unnecessary data to generate cleaner HTML,
> something other ASCII-to-HTML converters won't do.

## ❌ This is gross:
```html
<span class="asciiBold ansi30"></span>
<span class="asciiBold ansi30">-</span>
<span class="asciiBold ansi30"></span>
<span class="asciiBold ansi30">-</span>
<span class="asciiBold ansi30"></span>
<span class="asciiBold ansi30">-</span>
<span class="asciiBold ansi30"></span>
<span class="asciiBold ansi30">-</span>
...
```

## ✅ Much better optimized:

```html
<span class="asciiBold ansi30">----</span>
...
```

### This happens because sometimes programs (_cough cough mocha cough_) generate far too many escape codes.
### We provide happen to provide a quite fast solution!