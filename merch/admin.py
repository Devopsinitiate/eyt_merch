from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from .models import Size, Order

@admin.action(description='Export selected orders to Excel')
def export_to_excel(modeladmin, request, queryset):
    """Export orders to Excel file"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"
    
    # Header styling
    header_fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    
    # Headers
    headers = ['Order ID', 'Name', 'Gamer Tag', 'Number', 'Size', 'Color', 'Phone', 'Email', 'Date']
    ws.append(headers)
    
    # Style header row
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Data rows
    for order in queryset:
        ws.append([
            order.id,
            order.full_name,
            order.gamer_tag,
            order.preferred_number,
            order.size,
            order.get_color_display(),
            order.phone,
            order.email,
            order.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    # Adjust column widths
    column_widths = [10, 25, 20, 10, 10, 20, 15, 30, 20]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=eyt_orders.xlsx'
    wb.save(response)
    return response


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'available_quantity', 'is_available']
    list_editable = ['available_quantity']
    ordering = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'gamer_tag', 'full_name', 'size', 'color', 'created_at']
    list_filter = ['size', 'color', 'created_at']
    search_fields = ['full_name', 'gamer_tag', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    actions = [export_to_excel]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'gamer_tag', 'preferred_number')
        }),
        ('Product Selection', {
            'fields': ('size', 'color')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
