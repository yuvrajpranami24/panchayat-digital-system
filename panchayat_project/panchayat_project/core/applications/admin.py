from django.contrib import admin
from .models import Application, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'certificate_type',
        'citizen',
        'delivery_type',
        'amount',
        'is_paid',
        'status',
        'created_at',
    )

    list_filter = ('status', 'delivery_type', 'is_paid')
    search_fields = ('citizen__name', 'citizen__mobile')
    list_editable = ('status', 'is_paid')
    inlines = [DocumentInline]

    readonly_fields = ('notification_preview',)

    def notification_preview(self, obj):
        return obj.notification_message()

    notification_preview.short_description = "Notification Message"


admin.site.register(Document)
