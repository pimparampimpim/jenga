from django.contrib import admin
from .models import Museum, Guide, MuseumGuide, Exhibit, Exhibition, Address, City, Country
from .forms import AddressForm

class ExhibitInline(admin.TabularInline): 
    model = Exhibit
    extra = 1

class ExhibitionInline(admin.TabularInline): 
    model = Exhibition
    extra = 1   

class MuseumGuideInline(admin.TabularInline): 
    model = MuseumGuide
    extra = 1


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ['title', 'info', 'era']
    search_fields = ['title', 'museum__title']

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['museum', 'theme', 'floor', 'info']
    inlines = (ExhibitInline,)

@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'rating']
    inlines = (ExhibitionInline, MuseumGuideInline)

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'birthday']
    inlines = (MuseumGuideInline,)

@admin.register(MuseumGuide)
class MuseumGuideAdmin(admin.ModelAdmin):
    model = MuseumGuide
#    list_display = ['museum', 'guide']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ['name']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    autocomplete_fields = ['country']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = [
        'city',
        'street',
        'house_number',
        'entrance_number',
        'floor',
        'flat_number'
    ]
    search_fields = ['city', 'street', 'house_number']
    autocomplete_fields = ['city']
    form = AddressForm

