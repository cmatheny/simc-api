import web
import json
import time

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        jsobj = {
            'name': name,
            'age': 543
        }
        time.sleep(8)
        content = json.dumps(jsobj, sort_keys=True, indent=2)
        web.header('Content-Type','application/json; charset=utf-8')
        web.header('Content-Length', len(content))
        return content

if __name__ == "__main__":
    app.run()