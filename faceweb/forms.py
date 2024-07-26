from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm): # to upload vehicle image into database , u can see upload_vehicle.html , we have used forms.py
    class Meta:
        model = Vehicle 
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})


# ----------------------------------------------end of forms.py faceweb -------------------------------------------------------
# views.py

# from django.shortcuts import render, redirect
# from .forms import VehicleForm

# def upload_vehicle(request):
#     if request.method == 'POST':
#         form = VehicleForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('upload_success')  # Redirect to success page or image list
#     else:
#         form = VehicleForm()
#     return render(request, 'upload_vehicle.html', {'form': form})

# def upload_success(request):
#     return render(request, 'upload_success.html')
# forms.py