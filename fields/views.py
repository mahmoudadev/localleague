from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from fields.models import Field, Image
from .forms import FieldForm, ImageForm


def list(request):
    fields = Field.objects.all()
    return render(request, 'fields/list.html', {'fields': fields})


def create(request):
    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=3)
    field_form = FieldForm(request.POST or None)
    formset = ImageFormSet(request.POST or None , request.FILES or None , queryset=Image.objects.none())

    if field_form.is_valid() and formset.is_valid():
        field_form = field_form.save(commit=False)
        field_form.owner = request.user.landlord
        field_form.save()

        for form in formset.cleaned_data:
                print(form)
                image = form.get('image')
                photo = Image(field=field_form, image=image)
                photo.save()
        return redirect('fields:list')


    return render(request, 'fields/form.html', {'form': field_form, 'formset': formset})


def show(request, id):

    item = Field.objects.get(id=id)

    return render(request, 'fields/show.html', {'item': item })


def edit(request, id):

    instance_field = Field.objects.get(id=id)

    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=0)
    field_form = FieldForm(request.POST or None, instance=instance_field)
    formset = ImageFormSet(request.POST or None , request.FILES or None , queryset=instance_field.image_set.all())

    if field_form.is_valid() and formset.is_valid():
        field_form = field_form.save(commit=False)
        field_form.owner = request.user.landlord
        field_form.save()
        formset.save()
        return redirect('fields:show', instance_field.id)


    return render(request, 'fields/form.html', {'item': instance_field, 'form': field_form, 'formset': formset})