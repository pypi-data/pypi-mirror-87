from django.shortcuts import redirect

class NextViewMixin:
    def get_next_url(self):
        url = '/'
        if 'next' in self.request.GET:
            url = self.request.GET['next']
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        return url

    def next(self):
        url = self.get_next_url()
        return redirect(self.get_next_url())
