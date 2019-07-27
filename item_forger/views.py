from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import RPItem

from .forms import ViewCollectionForm, ForgeItemForm, EditItemForm
from .queries import ItemCollectionQuerySet as ICQS

def create_item_view(request, form_class=ForgeItemForm, template="item_forger/create_item.html",
                    extra_context=None, when=None, *args, **kwargs):
        form=form_class(
            data=request.POST or None,
            files=request.FILES or None
            )
        context = extra_context or {}

        if request.POST:
            if form.is_valid():
                item = form.save()
                context = {
                    "form": form_class(
                        data=None,
                        files=None
                        ),
                    "item_saved": True,
                    "item": item
                    }
                return render(request, template, context, *args, **kwargs)

        context.update({
            "form": form,
            "item_saved": False
            })

        return render(request, template, context, *args, **kwargs)

def edit_item_view(request, id, form_class=EditItemForm, template="item_forger/edit_item.html",
                    extra_context=None, when=None, *args, **kwargs):

        item = RPItem.objects.get(id=id)
        form=form_class(item=item,
            data=request.POST or None,
            files=request.FILES or None
            )
        context = extra_context or {}

        if "save_item" in request.POST:
            #import pudb; pudb.set_trace()
            if form.is_valid():
                item = form.save()
                context.update({
                    "form": form,
                    "item_saved": True,
                    "item": item
                    })
                return render(request, template, context, *args, **kwargs)

        if "delete_item" in request.POST:
            item.delete()
            return redirect('item_forger:item_collection')

        if "back" in request.POST:
            return redirect('item_forger:item_collection')

        context.update({
            "form": form,
            "item_saved": False
            })

        return render(request, template, context, *args, **kwargs)

def view_collection(
        request, form_class=ViewCollectionForm, template="item_forger/view_collection.html",
        extra_context=None, when=None, *args, **kwargs):


        form=form_class(
            data=request.POST or None,
            files=request.FILES or None
            )

        if "filter_items" in request.POST:
            if form.is_valid():
                rarity = form.cleaned_data["rarity_filter"]
                type = form.cleaned_data["type_filter"]
                attunement = form.cleaned_data['attunement_filter']
                campaign = form.cleaned_data['campaign_filter']
                items = ICQS().filter_item_query(rarity=rarity, attunement=attunement, type=type, campaign=campaign)

        elif 'export_items' in request.POST:
            if form.is_valid():
                rarity = form.cleaned_data["rarity_filter"]
                type = form.cleaned_data["type_filter"]
                attunement = form.cleaned_data['attunement_filter']
                campaign = form.cleaned_data['campaign_filter']
                items = ICQS().filter_item_query(rarity=rarity, attunement=attunement, type=type, campaign=campaign)
                #pdf = PDFExporter()
                #response = pdf.generate(items)
                #return response


        else:
            items = RPItem.objects.all()

        context = {
            'item_list': items,
            'form': form_class,
        }
        context.update(extra_context or {})
        return render(request, template, context, *args, **kwargs)
