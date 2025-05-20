from .models import DPR_table1

def circle(request):
    cir=[]
    objs=DPR_table1.objects.all()
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return {"cir":cir}