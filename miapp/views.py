
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import redirect, render

# Create your views here.

def home(request):
    return render(request,"layouts/home.html")

def about(request):
    return render(request,"layouts/about.html")

def proyectos(request):
    return render(request,"layouts/proyectos.html")

# views.py
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect, render

def contactos(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not (name and email and message):
            messages.error(request, "Por favor, completa todos los campos.")
            return redirect("contacto")

        subject = "Nuevo mensaje desde el sitio"
        body = f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}"

        try:
            msg = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECIPIENTS[0]],
                reply_to=[email],  # <- aquí sí es válido
            )
            msg.send(fail_silently=False)
        except BadHeaderError:
            messages.error(request, "Encabezado inválido en el correo.")
            return redirect("contacto")

        messages.success(request, "¡Gracias! Tu mensaje fue enviado.")
        return redirect("contacto")

    return render(request, "layouts/contacto.html")

def memoria(request):
    return render(request,"layouts/Memoria.html")

def snake(request):
    return render(request,"layouts/snake.html")

def nexa(request):
    return render(request,"layouts/nexa.html")

def ayudantias(request):
    return render(request, "layouts/ayudantias.html")