
__author__ = "Alexander Wallar <aw204@st-andrews.ac.uk>"


def run(host, port):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """

    import config
    import pageserver

    config.app.run(host=host, port=int(port), debug=True)


