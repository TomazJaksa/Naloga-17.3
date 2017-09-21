#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        besedilo = "Uporabnik je zapisal: "
        rezultat = self.request.get("vnos")
        skupaj = besedilo + rezultat
        return self.write(skupaj)


class GuessHandler(BaseHandler):
    def post(self):
        hiddenNumber=9
        
        number = int(self.request.get("vnos"))
        result = ""

        if number==hiddenNumber:
            result = "You've guessed the hidden number!"
        elif number < hiddenNumber:
            result = "The value is too low."
        elif number > hiddenNumber:
            result = "The value is too high."

        params = {"result": result}

        return self.render_template("result.html", params) # odpri rezultat na tej strani

class ConvertHandler(BaseHandler):
    def post(self):
        number = float(self.request.get("value"))
        conType = self.request.get("conversion")
        result = 0
        km = 0
        miles = 0

        if conType == "fromKmToMiles":
            km = number
            result = float(number*0.621371192)

        elif conType == "fromMilesToKm":
            miles = number
            result = float(number/0.621371192)


        params = {"result":result, "miles":miles, "km":km, "number":number}

        return self.render_template("convertResult.html",params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/guess',GuessHandler),
    webapp2.Route('/convert',ConvertHandler)
], debug=True)

