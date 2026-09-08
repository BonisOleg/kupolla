from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import Post, Category, Tag


class BlogListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
        cat_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = _('Блог KUPOLLA')
        ctx['meta_description'] = _('Корисні статті про купольні будинки, технології, глемпінг та нерухомість.')
        ctx['categories'] = Category.objects.all()
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx


class BlogPostView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        ctx['page_title'] = post.seo_title or post.title
        ctx['meta_description'] = post.seo_description or post.excerpt[:160]
        ctx['related_posts'] = (
            Post.objects
            .filter(is_published=True, category=post.category)
            .exclude(pk=post.pk)[:3]
        )
        return ctx
