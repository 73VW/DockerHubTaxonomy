import re
def filter(regexp, file):
    """
    Returns lines matching regexp in file
    """
    prog = re.compile(regexp)
    with open(file) as f:
        for k in [l for l in f if prog.search(l)]:
            print(k)


filter("^FROM.+", "dockerfile/alpine/gliderlabs-docker-alpine-3fbbd4c387d2934b13ea2526ce82f80e20301278-versions-library-3.2-Dockerfile")
