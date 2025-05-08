from django import forms
from .models import DPR_file,DPR_table1,performance_at_table


class dpr_upload_form( forms.ModelForm ) :
    class Meta :
        model = DPR_file
        fields = ("dpr_file",)
###################################################### soft at ##################################################################
class  soft_at_acceptance( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_ACCEPTANCE_DATE","SOFT_AT_ACCEPTANCE_MAIL")
        widgets = {
        'SOFT_AT_ACCEPTANCE_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['SOFT_AT_ACCEPTANCE_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        self.fields['SOFT_AT_ACCEPTANCE_MAIL'].widget.attrs.update({"class":"fm-input","required":"true"})
        

class  soft_at_rejection( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_REJECTION_DATE","SOFT_AT_REJECTION_REASON")
        widgets = {
        'SOFT_AT_REJECTION_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'SOFT_AT_REJECTED_TAT_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
        self.fields['SOFT_AT_REJECTION_REASON'].widget.attrs.update({"cols":10,"rows":20,"class":"fm-input","required":"true"})
        self.fields['SOFT_AT_REJECTION_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        # self.fields['SOFT_AT_REJECTED_TAT_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        

class  soft_at_offered( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_OFFERED_DATE","SOFT_AT_OFFERED_REMARKS")
        widgets = {
        'SOFT_AT_OFFERED_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
        self.fields['SOFT_AT_OFFERED_REMARKS'].widget.attrs.update({"cols":10,"rows":10,"class":"fm-input","required":"true"})
        self.fields['SOFT_AT_OFFERED_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
       


class  soft_at_pending( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_PENDING_REASON","SOFT_AT_PENDING_REMARK","SOFT_AT_PENDING_TAT_DATE")
        widgets = {
        'SOFT_AT_PENDING_TAT_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
       
        self.fields['SOFT_AT_PENDING_REASON'].widget.attrs.update({"cols":10,"rows":10,"class":"fm-input","required":"true"})
        self.fields["SOFT_AT_PENDING_REMARK"].widget.attrs.update({"cols":10,"rows":6,"class":"fm-input","required":"true"})
        self.fields['SOFT_AT_PENDING_TAT_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
       
############################################# physical at ######################################################################33

class  physical_at_acceptance( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_ACCEPTANCE_DATE","PHYSICAL_AT_ACCEPTANCE_MAIL")
        widgets = {
        'PHYSICAL_AT_ACCEPTANCE_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['PHYSICAL_AT_ACCEPTANCE_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        self.fields['PHYSICAL_AT_ACCEPTANCE_MAIL'].widget.attrs.update({"class":"fm-input","required":"true"})
        

class  physical_at_rejection( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_REJECTION_DATE","PHYSICAL_AT_REJECTION_REASON")
        widgets = {
        'PHYSICAL_AT_REJECTION_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'PHYSICAL_AT_REJECTED_TAT_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
        self.fields['PHYSICAL_AT_REJECTION_REASON'].widget.attrs.update({"cols":10,"rows":20,"class":"fm-input","required":"true"})
        self.fields['PHYSICAL_AT_REJECTION_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        # self.fields['PHYSICAL_AT_REJECTED_TAT_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        

class  physical_at_offered( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_OFFERED_DATE","PHYSICAL_AT_OFFERED_REMARKS")
        widgets = {
        'PHYSICAL_AT_OFFERED_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
    
        self.fields['PHYSICAL_AT_OFFERED_REMARKS'].widget.attrs.update({"cols":10,"rows":10,"class":"fm-input","required":"true"})
        self.fields['PHYSICAL_AT_OFFERED_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
       


class  physical_at_pending( forms.ModelForm ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_PENDING_REASON","PHYSICAL_AT_PENDING_REMARK","PHYSICAL_AT_PENDING_TAT_DATE")
        widgets = {
        'PHYSICAL_AT_PENDING_TAT_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
       
        self.fields['PHYSICAL_AT_PENDING_REASON'].widget.attrs.update({"cols":10,"rows":10,"class":"fm-input","required":"true"})
        self.fields["PHYSICAL_AT_PENDING_REMARK"].widget.attrs.update({"cols":10,"rows":6,"class":"fm-input","required":"true"})
        self.fields['PHYSICAL_AT_PENDING_TAT_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
       

####################################################### performance at ########################################################3


class  performance_at_acceptance( forms.ModelForm ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_ACCEPTANCE_DATE","PERFORMANCE_AT_ACCEPTANCE_MAIL")
        # fields = ("PERFORMANCE_AT_ACCEPTANCE_DATE",)
        widgets = {
        'PERFORMANCE_AT_ACCEPTANCE_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['PERFORMANCE_AT_ACCEPTANCE_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        self.fields['PERFORMANCE_AT_ACCEPTANCE_MAIL'].widget.attrs.update({"class":"fm-input","required":"true"})
        

class  performance_at_rejection( forms.ModelForm ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_REJECTION_DATE","PERFORMANCE_AT_REJECTION_REASON")
        widgets = {
        'PERFORMANCE_AT_REJECTION_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'PERFORMANCE_AT_REJECTED_TAT_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
        self.fields['PERFORMANCE_AT_REJECTION_REASON'].widget.attrs.update({"cols":10,"rows":20,"class":"fm-input","required":"true"})
        self.fields['PERFORMANCE_AT_REJECTION_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
        
        

class  performance_at_offered( forms.ModelForm ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_OFFERED_DATE","PERFORMANCE_AT_OFFERED_REMARKS")
        widgets = {
        'PERFORMANCE_AT_OFFERED_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
    
        self.fields['PERFORMANCE_AT_OFFERED_REMARKS'].widget.attrs.update({"cols":10,"rows":10,"class":"fm-input","required":"true"})
        self.fields['PERFORMANCE_AT_OFFERED_DATE'].widget.attrs.update({"class":"fm-input","required":"true"})
       


class  performance_at_pending( forms.ModelForm ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_PENDING_REASON",)
        widgets = {
        'PERFORMANCE_AT_PENDING_TAT_DATE': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date',"required":"true"}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['image_name'].label="car_name" "class":"fm-input"
       
        self.fields['PERFORMANCE_AT_PENDING_REASON'].widget.attrs.update({"cols":10,"rows":10,"class":"fm-input","required":"true"})
        # self.fields["PERFORMANCE_AT_PENDING_REMARK"].widget.attrs.update({"cols":10,"rows":6,"class":"fm-input","required":"true"})
        


