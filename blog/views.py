from django.shortcuts import render

def test(request):
    return render(request, 'blog/login.html')

def signup_view(request):
    if request.method == 'POST':
       
        pass
    return render(request, 'blog/signup.html')
