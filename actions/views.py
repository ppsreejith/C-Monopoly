from game.views import ApiTemplate

class SimpleTest(ApiTemplate):
    def post(self):
        return self.render({"name":"Sreejith Pp"})