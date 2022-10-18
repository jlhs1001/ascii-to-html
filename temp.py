from src.ascii_to_html import ascii_to_html
from pathlib import Path

TEST_ROOT = Path(__file__).parent / "tests"
# read the test data
with open(str(TEST_ROOT / "out.txt"), 'r') as f:
    lines = f.readlines()

# convert the lines to html
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Test</title>
    <style>
    .ansi_fore {
    color: #FFFFFF;

}

body {
    font-family: monospace;
    font-size: 12px;
    background-color: #222;
    color: #bbb;
}

.ansi_back {
    background-color: #000000;
}
r
.ansi1 {
    font-weight: bold;
}

.ansi4 {
    text-decoration: underline;
}

.ansi9 {
    text-decoration: line-through;
}

.ansi30 {
    color: #000000;
}

.ansi31 {
    color: #FF0000;
}

.ansi32 {
    color: #00FF00;
}

.ansi33 {
    color: #FFFF00;
}

.ansi34 {
    color: #0000FF;
}

.ansi35 {
    color: #FF00FF;
}

.ansi36 {
    color: #00FFFF;
}

.ansi37 {
    color: #FFFFFF;
}

.ansi40 {
    background-color: #000000;
}

.ansi41 {
    background-color: #FF0000;
}

.ansi42 {
    background-color: #00FF00;
}

.ansi43 {
    background-color: #FFFF00;
}

.ansi44 {
    background-color: #0000FF;
}

.ansi45 {
    background-color: #FF00FF;
}

.ansi46 {
    background-color: #00FFFF;
}

.ansi47 {
    background-color: #FFFFFF;
}
</style>
</head>
<body>
"""

# for line in lines:
#     html += ascii_to_html(line, insert_nbsp=True)

html += ascii_to_html("".join(lines), insert_nbsp=True)

html += """
</body>
</html>
"""

# write the html to a file
with open(str(TEST_ROOT / "out.html"), 'w') as f:
    f.write(html)
