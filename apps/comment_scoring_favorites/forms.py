from django import forms

class CommentForm(forms.Form):
    product_id=forms.CharField(widget= forms.HiddenInput(), required=False)                         # HiddenInput() por mishe vali dide nemishe
    comment_id=forms.CharField(widget= forms.HiddenInput(), required=False)
    comment_text=forms.CharField(label='',
                                 error_messages={"required":"This field can't leave blank"},
                                 widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description','rows':'4'})
                                 )