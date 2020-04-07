from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages


class HomeView(ListView):
    model = Item
    paginate_by = 2
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

# class ProductDetailView(View):
#     def get(self, request, slug):
#         item = get_object_or_404(Item, slug=slug)
#         context = {'item': item}
#         return render(request, 'product.html', context)

# def product(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'product.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, "order_summary.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "No active Order")
            return redirect("/")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            return render(self.request, 'checkout.html')
        except print(0):
            pass
        return render(self.request, 'checkout.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if orderITEM is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item Quatity was Updated")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was added to the Cart")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to the Cart")
        return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if orderITEM is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your Cart")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your Cart")
            return redirect("core:product", slug=slug)

    else:
        messages.info(request, "You do not have an Order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if orderITEM is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                order.items.remove(order_item)
            order_item.save()
            messages.info(request, "This item Quantity was updated")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your Cart")
            return redirect("core:order-summary")

    else:
        messages.info(request, "You do not have an Order")
        return redirect("core:order-summary")
