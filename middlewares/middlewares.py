import threading

# in class baes mishe ke betunim usere jari(request.user) ro toye model ha estefade konim
# 1. ijade middlewares dir 
# 2. ijade middlewares file 
# 3. neveshtane in class 
# 4. settings => MIDDLEWARE= ["middlewares.middlewares.RequestMiddleware",]
# 5. mitunim to model azash estefade konim. ref to apps.products.model => def get_user_score(self)
class RequestMiddleware:
    def __init__(self,get_response, thread_local=threading.local()):
        self.get_response=get_response
        self.thread_local=thread_local
        
    def __call__(self, request):
        self.thread_local.current_request = request
        response= self.get_response(request)
        return response