from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


from pengajuan.forms import PengajuanForm, VerifikasiPermohonanForm

from accounts.services import registrasi_service
from accounts.forms import RegisterForm

from bantuan.models import Bantuan
from pengajuan.models import Pengajuan

def index(request):
    return render(request, 'pages/index.html')



def pengajuan_detail_view(request, pengajuan_id):
    pengajuan = get_object_or_404(Pengajuan, id=pengajuan_id)
    if request.method == "POST":
        form_verifikasi = VerifikasiPermohonanForm(request.POST, instance=pengajuan)
        if form_verifikasi.is_valid():
            obj = form_verifikasi.save(commit=False)
            obj.pengajuan = Pengajuan.objects.get(id=pengajuan_id)
            obj.diverifikasi_oleh = request.user
            obj.tanggal_verifikasi = timezone.now()
            
            try:
                obj.save()
                messages.success(request, "Pengajuan berhasil diverifikasi")
                return redirect("pengajuan_detail", pengajuan_id=pengajuan_id)
            except Exception as e:
                messages.error(request, "Pengajuan gagal diverifikasi")
                return redirect("pengajuan_detail", pengajuan_id=pengajuan_id)
        else:
            obj = form_verifikasi.save(commit=False)
            obj.pengajuan = Pengajuan.objects.get(id=pengajuan_id)
            obj.diverifikasi_oleh = request.user
            obj.tanggal_verifikasi = timezone.now()
            obj.save()
            messages.success(request, "Pengajuan berhasil diverifikasi")
            return redirect("pengajuan_detail", pengajuan_id=pengajuan_id)
    context = {
        "pengajuan": Pengajuan.objects.get(id=pengajuan_id),
        "form_verifikasi": VerifikasiPermohonanForm(instance=pengajuan)
    }
    return render(request, 'pages/pengajuan_detail.html', context)

def dashboard_admin(request):
    
    context = {
        "daftar_pengajuan": Pengajuan.objects.all()
    }
    return render(request, 'pages/dashboard_admin.html', context)

def dashboard_masyarakat(request):
    
    if request.method == "POST":
        form_pengajuan_bantuan = PengajuanForm(request.POST, request.FILES)
        if form_pengajuan_bantuan.is_valid():
            obj = form_pengajuan_bantuan.save(commit=False)
            obj.masyarakat = request.user.masyarakat
            obj.save()
            
            
            messages.success(request, "Pengajuan berhasil dikirim")
            return redirect("dashboard_masyarakat")
        
    else:
        form_pengajuan_bantuan = PengajuanForm()
        
    try:
        daftar_pengajuan = Pengajuan.objects.filter(masyarakat=request.user.masyarakat)
    except ObjectDoesNotExist:
        daftar_pengajuan = None
    
    context = {
        "daftar_bantuan": Bantuan.objects.all(),
        "daftar_pengajuan": daftar_pengajuan,
        "form_pengajuan_bantuan": form_pengajuan_bantuan
    }
    return render(request, 'pages/dashboard_masyarakat.html', context)

def form_pengajuan_view(request):
    context = {}
    return render(request, 'pages/form_pengajuan.html', context)
