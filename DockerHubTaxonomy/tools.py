import re
def filter(regexp, text):
    """
    Returns lines matching regexp in file
    """
    lines = text.splitlines()
    prog = re.compile(regexp)
    for k in [line for line in lines if prog.search(line)]:
        return k

filter("^FROM.+", "FROM scratch\nFROM foo\nFROM bar")
