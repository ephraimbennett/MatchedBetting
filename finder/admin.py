from django.contrib import admin
from .models import Settings, BonusBet, SecondBet, State, ProfitBet, BookMaker, Promo, Event, Line

# Inline admin to show Line objects in the Event admin
class LineInline(admin.TabularInline):  # or admin.StackedInline for a different look
    model = Line
    extra = 0
    show_change_link = True  # Optional: lets you click through to each Line
    readonly_fields = ['bookmaker', 'side', 'odds']  # Optional: make fields read-only

# Customize Event admin to include the LineInline
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'time')  # Add more fields as needed
    inlines = [LineInline]

# Register everything
admin.site.register(BonusBet)
admin.site.register(Settings)
admin.site.register(SecondBet)
admin.site.register(State)
admin.site.register(ProfitBet)
admin.site.register(BookMaker)
admin.site.register(Promo)
admin.site.register(Line)  # Keep Line registered separately for searching/filtering

# Register Event with custom admin
admin.site.register(Event, EventAdmin)
