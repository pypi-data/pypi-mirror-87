# noqa: D205,D208,D400
"""
    formelsammlung.flask_sphinx_docs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Serve sphinx docs in your flask app.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
from pathlib import Path
from typing import Optional

from flask import Flask, Response


class SphinxDocServer:  # pylint: disable=R0903
    """Serve your sphinx docs under `/docs/` on your own flask app.

    .. highlight:: python

    You can invoke it in your app factory::

        sds = SphinxDocServer()

        def create_app():
            app = Flask(__name__)
            sds.init_app(app)
            return app

    or you can include the plugin directly without setting a ``doc_dir``::

        app = Flask(__name__)
        SphinxDocServer(app)

    or with setting a ``doc_dir``::

        app = Flask(__name__)
        SphinxDocServer(app, doc_dir="../../docs/build/html")

    .. highlight:: default
    """

    def __init__(self, app: Optional[Flask] = None, **kwargs) -> None:
        """Init SphinxDocServer."""
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(
        self, app: Flask, doc_dir: Optional[str] = None, index_file: str = "index.html"
    ) -> None:
        """Add the `/docs/` route to the `app` object.

        :param app: Flask object to add the route to.
        :param doc_dir: The base directory holding the sphinx docs to serve. If not set
            the ``doc_dir`` is guessed up to 3 directories above.
        :param index_file: The html file containing the base toctree.
            Default: "index.html"
        """

        @app.route("/docs/", defaults={"filename": index_file})
        @app.route("/docs/<path:filename>")
        def web_docs(filename: str) -> Response:  # pylint: disable=W0612
            """Route the given doc page.

            :param filename: File name from URL
            :return: Requested doc page
            """
            app.static_folder = doc_dir or self._find_build_docs(app.root_path or "")
            doc_file = app.send_static_file(filename)
            app.static_folder = "static"
            return doc_file

    @staticmethod
    def _find_build_docs(app_root: str, steps_up_the_tree: int = 3):
        """Find build sphinx html docs.

        :param app_root: Root directory of the app.
        :param steps_up_the_tree: Amount of steps to go up the file tree, defaults to 3
        :raises IOError: if no root dir path for the app is given.
        :raises IOError: if no 'doc' or 'docs' directory is found.
        :raises IOError: if no '_build' or 'build' directory is found in the
            doc/docs dir.
        :raises IOError: if no 'html' directory is found in the _build/build dir.
        :return: Path to directory holding the build sphinx docs.
        """
        if not app_root:
            raise OSError("Got no root dir for the flask app to start search.")

        check_dir = file_dir = Path(app_root).parent

        #: Search doc(s) dir up the tree
        doc_dir = None
        for i in range(0, steps_up_the_tree + 1):
            if (check_dir / "doc").is_dir():
                doc_dir = check_dir / "doc"
            if (check_dir / "docs").is_dir():
                doc_dir = check_dir / "docs"

            if doc_dir:
                break

            check_dir = file_dir.parents[i]

        if not doc_dir:
            raise OSError("No 'doc' or 'docs' directory found.")

        #: search for (_)build dir
        build_dir = None
        if (doc_dir / "_build").is_dir():
            build_dir = doc_dir / "_build"
        if (doc_dir / "build").is_dir():
            build_dir = doc_dir / "build"

        if not build_dir:
            raise OSError(
                f"No '_build' or 'build' directory found in {doc_dir}. "
                "Maybe you forgot to build the docs."
            )

        #: check for html dir
        if (build_dir / "html").is_dir():
            return build_dir / "html"
        raise OSError(
            f"No 'html' directory found in {build_dir}. "
            "Maybe you forgot to build the HTML docs."
        )
