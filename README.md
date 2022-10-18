![# ascii_to_html](https://github.com/jlhs1001/ascii-to-html/blob/main/data/logo.png?raw=true)

-- Made by Liam Seewald

## HTML-ify your ASCII with ease and elegance.


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
converter.to_html("")
```

