from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Item  
from .serializer import ItemForm  
from django.contrib.auth.decorators import user_passes_test
from .models import Item, Purchase
from django.db.models import Exists, OuterRef

@login_required
def shop_view(request):
    purchased_items = Purchase.objects.filter(item=OuterRef('pk'))
    items = Item.objects.annotate(
        is_sold=Exists(purchased_items)
    ).filter(is_sold=False)
    return render(request, 'shop.html', {'items': items})


@login_required
def purchase_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)  
    user = request.user

    if user.money >= item.price:
        purchase = Purchase.objects.create(
         
            user=user,
            item=item,
            item_name=item.name,
            item_price=item.price,
        )

        user.money -= item.price
        user.purchases_total += item.price
        user.save()

        item.delete()

        messages.success(request, f"You successfully purchased {purchase.item.name}")
        return redirect('home')

    else:
        messages.error(request, "You don't have enough money to buy this item.")
        return redirect('shop')


@login_required
def purchase_history(request):
    purchases = request.user.purchases.all().order_by('-purchase_date')
    return render(request, 'purchase_history.html', {'purchases': purchases})

@login_required
def buy_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user

    if user.money >= item.price:
        user.money -= item.price
        user.save()
        messages.success(request, f'You bought {item.name} for ${item.price}.')
    else:
        messages.error(request, "You don't have enough money to buy this item.")

    return redirect(f'/home/?price={item.price}')



@user_passes_test(lambda u: u.is_staff)  
@login_required
def add_item_view(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully.")
            return redirect("shop")
    else:
        form = ItemForm()
    return render(request, "add_item.html", {"form": form})