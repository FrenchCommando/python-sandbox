import re
from html.parser import HTMLParser
# need to use html parser because it handle all the conversions and the ""


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start :", tag)
        for u, v in attrs:
            print("-> {} > {}".format(u, v))

    def handle_endtag(self, tag):
        print("End   :", tag)

    def handle_startendtag(self, tag, attrs):
        print("Empty :", tag)
        for u, v in attrs:
            print("-> {} > {}".format(u, v))

    def handle_comment(self, data):
        if '\n' in data:
            print(">>> Multi-line Comment")
        else:
            print(">>> Single-line Comment")
        print(data)

    def handle_data(self, data):
        if data.strip():
            print(">>> Data")
            print(data)


# instantiate the parser and fed it some HTML
parser = MyHTMLParser()


html_tag_format = r"<[^<>]*>"


def parse_html(s):
    s = re.sub(r"<!--(.|\s|\n)*?-->", "", s)
    for m in re.findall(html_tag_format, s):
        process_tag(m)


def process_tag(t):
    clean_content = t[1:-1]
    if not clean_content:
        return
    content, is_end = parse_end(clean_content)
    print("{:6}".format(is_end), end=": ")
    split_content = content.split(" ")
    content_iter = iter(split_content)
    print(next(content_iter).lower())
    for u in content_iter:
        v = u.split("=", 1)
        u0 = v[0]
        try:
            u1 = (v[1]).strip("'").strip("\"")
        except IndexError:
            u1 = None
        print("-> {} > {}".format(u0, u1))


def parse_end(c):
    if c[0] == "/":
        return c[1:].strip(), "End"
    if c[-1] == "/":
        return c[:-1].strip(), "Empty"
    return c.strip(), "Start"


if __name__ == "__main__":
    s = """2
<html><head><title>HTML Parser - I</title></head>
<!--fwefwefew-->
<body data-modal-target class='1'><h1>HackerRank</h1><br /></body></html>"""
    s = s.split("\n", 1)[1]
    # parse_html(s)

    s2 = """5
<script type="text/javascript" src="js/cufon-yui.js"></script>
<script type="text/javascript" src="js/TitilliumMaps.font.js"></script><h1>Business Solutions</h1><br />
<h2>Business Insurance</h2><script type="text/javascript">
    Cufon.replace('h1, h2', { fontFamily: "TitilliumMaps26L", hover: true });
</script>"""
    s2 = s2.split("\n", 1)[1]
    # parse_html(s2)

    s3 = """11
<!--[if !IE 6]><!-->
  <link rel="stylesheet" type="text/css" media="screen, projection" href="REGULAR-STYLESHEET.css" />
<!--<![endif]-->

<!--[if gte IE 7]>
  <link rel="stylesheet" type="text/css" media="screen, projection" href="REGULAR-STYLESHEET.css" />
<![endif]-->

<!--[if lte IE 6]>
  <link rel="stylesheet" type="text/css" media="screen, projection" href="http://universal-ie6-css.googlecode.com/files/ie6.0.3.css" />
<![endif]-->"""
    s3 = s3.split("\n", 1)[1]
    parse_html(s3)
    parser.feed(s3)
