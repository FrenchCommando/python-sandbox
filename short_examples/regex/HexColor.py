import re


hex_pattern = r'[0-9a-fA-F]'
hex_color_pattern = r'#({0}{{6}}|{0}{{3}})'.format(hex_pattern)  # this version doesn't print the # in findall
hex_color_pattern = r'(#{0}{{6}}|#{0}{{3}})'.format(hex_pattern)
single_hex_color_pattern = r"^({})$".format(hex_color_pattern)
print(hex_color_pattern)
print(single_hex_color_pattern)


def filter_hexcolor(s):
    s = s.strip()
    if re.match(single_hex_color_pattern, s) or "{" in s:
        return
    i = re.findall(hex_color_pattern, s)
    for m in i:
        print(m)


if __name__ == "__main__":
    s = """11
#BED
{
    color: #FfFdF8; background-color:#aef;
    font-size: 123px;
    background: -webkit-linear-gradient(top, #f9f9f9, #fff);
}
#Cab
{
    background-color: #ABC;
    border: 2px dashed #fff;
}   """
    for line in s.split("\n"):
        filter_hexcolor(line)
