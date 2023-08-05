import http.server
import io
import json
import os
import socketserver
import webbrowser

from pathlib import Path


def start_http_server(index_configuration, port, compare=False):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def do_GET(self, *args, **kwargs):
            directory_name = index_configuration.get('directory_name')
            if self.path in ['/', '/index.html']:
                if directory_name:
                    html_file_name = 'file_viewer.html'
                    metadata_file_path = str(Path(directory_name).joinpath('metadata.json'))
                    with open(metadata_file_path, 'r') as file:
                        format_configuration = json.load(file)
                        format_configuration['port'] = port

                else:
                    html_file_name = 'bigquery_viewer_compare.html' if compare else 'bigquery_viewer.html'
                    format_configuration = dict(index_configuration)

                print(os.getcwd())

                html_file_name = str(Path(__file__).parent.joinpath('assets', html_file_name))
                with open(html_file_name, 'r') as viewer_file:
                    viewer = viewer_file.read()
                viewer = viewer.format(**format_configuration)
                viewer_file = io.BytesIO(viewer.encode())

                self.send_response(200)
                self.send_header('Content-Length', len(viewer))
                self.end_headers()

                self.copyfile(viewer_file, self.wfile)

            self.path = '/{directory}{path}'.format(directory=directory_name, path=self.path)

            if not(self.path.endswith('.pbf') or self.path.endswith('.mvt')):
                return super().do_GET(*args, **kwargs)

            else:
                tile_file_path = str(Path(self.path[1:]))
                tile_exists = os.path.isfile(tile_file_path)

                if not tile_exists:
                    self.send_response(204)
                    self.end_headers()

                else:
                    with open(tile_file_path, 'rb') as tile_file:
                        tile_length = os.fstat(tile_file.fileno())[6]

                        self.send_response(200)
                        self.send_header('Content-Length', str(tile_length))
                        self.send_header('Content-Encoding', 'gzip')
                        self.end_headers()

                        self.copyfile(tile_file, self.wfile)

    httpd = socketserver.TCPServer(('', port), Handler)
    webbrowser.open('http://localhost:{port}/'.format(port=port), new=2)
    httpd.serve_forever()
