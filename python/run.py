import importlib
import utils.logger
import utils.module_scanner
import os
import services.simc
import tornado.ioloop
import tornado.web
import tornado.websocket
import ignore

def make_app(settings_file = "config.settings"):
    settings = importlib.import_module(settings_file)
    handlers = utils.module_scanner.generate_handlers(settings.CONTROLLER_MODULES)
    app = tornado.web.Application(handlers)
    app.listen(settings.SERVER_PORT)
    utils.logger.log("Server listening on port: ", settings.SERVER_PORT)
    return app

if __name__ == '__main__':
    print(ignore.Test.callit(2))
#    
#    with open(os.path. expanduser("~") + "/.simc_apikey", "w") as f: 
#        f.write(os.environ['APIKEY'])
#    
#    utils.logger.log("Debug Test")
#    utils.logger.log("Log Test")
#    utils.logger.warn("Warn Test")
#    utils.logger.err("Error Test")
#    app = make_app()
#    service = services.simc.SimcService()
#    tornado.ioloop.IOLoop.current().start()
