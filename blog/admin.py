from django.contrib import admin

# Register your models here.
from blog.models import Article, MetaData, Tag, Category, create_slug, PageCount


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content',{
            'fields': ('title','description','category','tags','status','trashed'),

        }),
        ('Images', {
            'fields': ('card_image','main_image',),
            'classes': ('collapse', 'collapse-closed')
        }),
        ('Publication', {
            'fields': ('publish_date','creation_date','last_update','start_publish_date','end_publish_date',),
            'classes': ('collapse', 'collapse-closed')
        }),
        (None, {
            'fields': ('featured','author','slug',),

        }),
    )
    list_display = ('title', 'author', 'status', 'publish_date')

    list_filter = ('status', 'publish_date')
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    ordering = ['status', 'publish_date']
    raw_id_fields = ('author',)
    radio_fields = {'status': admin.VERTICAL}
    search_fields = ('title', 'content', 'author')


    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = create_slug(obj)
        obj.save()
        # obj.slug = create_slug(obj)
        # obj.save()

class MetaDataAdmin(admin.ModelAdmin):
    fieldsets = (
            ('hello', {
                'fields': ('keyword','description')
            }),
            ('Advanced options', {
                'classes': ('collapse',),
                'fields': ('article',)
            }),
        )


admin.site.register(Article, ArticleAdmin)
admin.site.register(MetaData, MetaDataAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PageCount)