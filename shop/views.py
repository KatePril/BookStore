from django.db.models import Q

from django.shortcuts import render
from django.urls import reverse
from config.settings import PAGE_NAMES
from .models import Category, Book
from main.mixins import ListViewBreadCrumbMixin, DetailViewBreadcrumbsMixin
# Create your views here.

class CatalogIndexView(ListViewBreadCrumbMixin):
    template_name = 'shop/index.html'
    model = Category
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        return Category.objects.filter(parent=None)
    
    def get_breadcrumbs(self):
        self.breadcrumbs = {
            'current' : PAGE_NAMES['catalog'],

        } # вказуємо поточну сторінку ДОПИСАТИ
        return self.breadcrumbs

class BookByCategory(ListViewBreadCrumbMixin):
    template_name = 'shop/book_list.html'
    category = None
    categories = Category.objects.all()
    paginate_by = 6
    
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Book.objects.filter(category=self.category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["categories"] = self.categories
        return context    
    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog']}
        if self.category.parent:
            linkss = []
            parent = self.category.parent
            while parent is not None:
                linkss.append(
                    (
                        reverse('category', kwargs={'slug': parent.slug}),
                        parent.name
                    )
                )
                parent = parent.parent
            for url, name in linkss[::-1]:
                breadcrumbs[url] = name
                #breadcrumbs.update({url: name}) # або так
        breadcrumbs.update({'current': self.category.name})
        return breadcrumbs

class BookDetailView(DetailViewBreadcrumbsMixin):
    model = Book
    template_name = 'shop/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog']}
        category = self.object.main_category()
        if category:
            if category.parent:
                linkss = []
                parent = category.parent
                while parent is not None:
                    linkss.append(
                        (
                            reverse('category', kwargs={'slug': parent.slug}),
                            parent.name
                        )
                    )
                    parent = parent.parent
                for url, name in linkss[::-1]:
                    breadcrumbs.update({url: name})
            breadcrumbs.update({reverse('category', kwargs={'slug': category.slug}): category.name})
        breadcrumbs.update({'current': self.object.name})
        return breadcrumbs

def user_book_list(request, pk):
    books = Book.objects.filter(owner=pk)
    return render(request, 'shop/custom_list.html', {'books': books})

def search(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'shop/custom_list.html', {'books': books})