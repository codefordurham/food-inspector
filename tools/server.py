import http.server
import socketserver
import argparse


parser = argparse.ArgumentParser(description='Simple development HTTP server')
parser.add_argument('--host', help='host to listen on', default="localhost")
parser.add_argument('--port', type=int, help='port to listen on', default=8001)


def main():
    args = parser.parse_args()
    Handler = http.server.SimpleHTTPRequestHandler
    print(args)
    httpd = socketserver.TCPServer((args.host, args.port), Handler)
    print("serving at", args.host, args.port)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
