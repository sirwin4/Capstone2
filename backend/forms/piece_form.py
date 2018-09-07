from django import forms
from backend.models import Piece

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('name', 'standard_number', 'min_size', 'max_size', 'active', 'user_rack', 'area_rack')
        