import http.server
import socketserver
import requests
import re

domain = "https://news.ycombinator.com/"
HOST = '127.0.0.1'
PORT = 6174


class HackerProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = domain + self.path[1:]
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        s_html = requests.get(url)
        s_html_splitted = re.split('(<[^>]*>)', s_html.text)
        s_html_list = [i for i in " ".join(s_html_splitted).split(" ")]
        result = []

        for x in s_html_list:
            if len(x) == 6 and x.isalpha():
                x = x + "&#10084;&#65039;"
            if x == 'href="favicon.ico">':
                x = 'href="https://news.ycombinator.com/favicon.ico">'
            if x == 'src="y18.gif"':
                x = 'src="https://news.ycombinator.com/y18.gif"'
            if x == 'href="news.css?9NJgprN1KEySYl9ly5Jp">':
                x = 'href="https://news.ycombinator.com/news.css?3j84cbbQsnRiQd7bc60p">'
            if x == "src='hn.js?9NJgprN1KEySYl9ly5Jp'>":
                x = 'src="https://news.ycombinator.com/hn.js?9NJgprN1KEySYl9ly5Jp">'
            result.append(x)
        self.wfile.write(bytes(re.sub('(?<=>) | (?=<)', '', " ".join(result)), 'UTF-8'))


httpd = socketserver.ThreadingTCPServer(("", PORT), HackerProxy)
print("Serving at port", PORT)
httpd.serve_forever()
