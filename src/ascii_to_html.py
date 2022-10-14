def ascii_to_html(source, insert_nbsp=False):
    result = "<span>"
    tags = [0, 0, False, False]
    index = 0
    while index < len(source):
        if source[index] == "\x1b":
            nums_str = source[index + 2:].split("m")[0]
            numbers = [int(num) for num in nums_str.split(";") if num.isnumeric()]
            for num in numbers:
                if num == 0:
                    tags = [0, 0, False, False]
                    break
                if 30 <= num <= 37 or 90 <= num <= 97:
                    tags[0] = num
                elif 40 <= num <= 47 or 100 <= num <= 107:
                    tags[1] = num
                elif num == 1:
                    tags[2] = True
                elif num == 4:
                    tags[3] = True
            result += f'</span><span class="{"ansi" + str(tags[0]) if tags[0] != 0 else ""}' \
                      f'{"ansi" + str(tags[1]) if tags[1] != 0 else ""}' \
                      f'{"ansiBold" if tags[2] else ""} {"ansiUnderline" if tags[3] else ""}">'
            index += len(nums_str) + 3  # 3 = len('\x1b[m'); (account for redundant chars).
        try:
            if insert_nbsp and source[index] == " ":
                result += "&nbsp;"
            else:
                result += source[index]
        except IndexError:
            pass
        index += 1
    return result + "</span>"
