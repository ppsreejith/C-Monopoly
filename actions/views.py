from game.views import ApiTemplate

class SimpleTest(ApiTemplate):
    def post(self,request):
        return self.render({"name":"Sreejith Pp"})