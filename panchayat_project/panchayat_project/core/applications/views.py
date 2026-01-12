from django.shortcuts import render, redirect
from .models import Application, Document
from users.models import Citizen
from panchayat.models import Panchayat


def apply_certificate(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        certificate_type = request.POST.get('certificate_type')
        panchayat_id = request.POST.get('panchayat')
        delivery_type = request.POST.get('delivery_type')
        document_file = request.FILES.get('document')

        # 🔹 Citizen: create or reuse (IMPORTANT)
        citizen, created = Citizen.objects.get_or_create(
            mobile=mobile,
            defaults={
                'name': name,
                'address': address
            }
        )

        panchayat = Panchayat.objects.get(id=panchayat_id)

        # 🔹 Charges logic (pilot = free)
        if delivery_type == 'courier':
            amount = 0
        elif delivery_type == 'taluka':
            amount = 0
        else:
            amount = 0

        application = Application.objects.create(
            citizen=citizen,
            panchayat=panchayat,
            certificate_type=certificate_type,
            delivery_type=delivery_type,
            amount=amount,
            is_paid=False
        )

        # 🔹 Document save
        if document_file:
            Document.objects.create(
                application=application,
                name=document_file.name,
                file=document_file
            )

        return redirect('status')

    panchayats = Panchayat.objects.all()
    return render(request, 'apply.html', {'panchayats': panchayats})


def application_status(request):
    application = None
    if request.method == "POST":
        mobile = request.POST.get('mobile')

        application = Application.objects.filter(
            citizen__mobile=mobile
        ).order_by('-created_at').first()   # 🔥 latest record

    return render(request, 'status.html', {'application': application})
