from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from actions.utils import create_action

from .models import Image
from .forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == 'POST':
        # форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # данные в форме валидны
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # назначить текущего пользователя элементу
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarkes image', new_image)
            messages.success(request,
                             'Image added successfully')
            # перенаправить к представлению детальной
            # информации о только что созданном элементе
            return redirect(new_image.get_absolute_url())
    else:
        # скомпоновать форму с данными,
        # предоставленными букмарклетом методом GET
        form = ImageCreateForm(data=request.GET)
        return render(request,
                      'images/image/create.html',
                      {'section': 'images',
                       'form': form})

def image_detail(request, id, slug):

    image = get_object_or_404(Image, id=id, slug=slug)

    return render(
        request,
        "images/image/detail.html",
        {
            "section": "images",
            'image': image
        }
    )


# Постановка лайка-удаление из лайкнувших
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):

    images = Image.objects.all()
    paginator = Paginator(images, 6)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не целое число, грузим 1
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # Если ajacx запрос и страница вне диапозона, вернем пустую
            return HttpResponse('')

        # Если страница вне диапазона, вернуть последжнюю страницу
        images = paginator.page(paginator.num_pages)

    if images_only:

        return render(request,
                      'images/image/list_images.html',
                      {'section': 'images',
                       'images': images}
                        )
    return render(request,
                  'images/image/list.html',
                  {'section': 'images',
                   'images': images})

