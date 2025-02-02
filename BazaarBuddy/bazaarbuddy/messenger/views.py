from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from core.models import Product

from .forms import MessageForm
from .models import Chat

@login_required
def new_chat(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product.user == request.user:
        return redirect('core:product_detail', id=product.id)
    
    chats = Chat.objects.filter(product=product).filter(members__in=[request.user.id])

    if chats:
        return redirect('messenger:detail', pk=chats.first().id)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            chat = Chat.objects.create(product=product)
            chat.members.add(request.user)
            chat.members.add(product.user)
            chat.save()
            
            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user  
            chat_message.save()

        return redirect('messenger:detail', pk=product_id)
    else:
        form = MessageForm()
    
    return render(request, 'messenger/new_chat.html', {
        'form': form
    })
    
    
@login_required
def inbox(request):
    chats = Chat.objects.filter(members__in=[request.user.id])

    return render(request, 'messenger/inbox.html', {
        'chats': chats
    })
    
    
@login_required
def detail(request, pk):
    chat = Chat.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()

            chat.save()

            return redirect('messenger:detail', pk=pk)
    else:
        form = MessageForm()

    return render(request, 'messenger/detail.html', {
        'chat': chat,
        'form': form
    })
