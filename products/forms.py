from django import forms
from .models import Product,ProductImages


# CATEGORY=(
#     ('MOB','mobile'),
#     ('CL','Cloths'),
#     ('EL','Electronics'),
#     ('SP','Sports'),
#     ('HOAP','Home Applications'),

# )

class ProductCreateForm(forms.ModelForm):

    class Meta:
        model=Product
        fields= ('name','description','category','price',)
        
class ProductImageFrom(forms.ModelForm):
    class Meta:
        model=ProductImages
        fields=('image',)