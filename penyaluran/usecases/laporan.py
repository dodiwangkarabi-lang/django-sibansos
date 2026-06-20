import io
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Border, Side, Font

from django.conf import settings

# models
from penyaluran.models import (
    PenerimaBantuan
)

def format_header(col_name: str) -> str:
    return col_name.replace("_", " ").upper()

class Laporan:
    def __init__(self):
        pass
    
    def _generate_dataframe(self) -> pd.DataFrame:
        penerima_bantuan_qs = PenerimaBantuan.objects.all()
        no = 1
        penerima_bantuan_list = [
            {
                "nik": penerima_bantuan.masyarakat.nik,
                "nama": penerima_bantuan.masyarakat.nama,
                "alamat": penerima_bantuan.masyarakat.alamat,
                "no_hp": penerima_bantuan.masyarakat.no_hp,
                "jenis_bantuan": penerima_bantuan.bantuan.nama,
                "tanggal_terima": penerima_bantuan.tanggal_terima,
            }
            for penerima_bantuan in penerima_bantuan_qs
        ]
        penerima_bantuan_df = pd.DataFrame(penerima_bantuan_list)
        penerima_bantuan_df["no"] = penerima_bantuan_df.index + 1
        # pindahkan kolom no di awal
        penerima_bantuan_df = penerima_bantuan_df[["no"] + [col for col in penerima_bantuan_df.columns if col != "no"]]
        
        # rubah format tanggal menjadi tanggal-bulan-tahun
        penerima_bantuan_df["tanggal_terima"] = pd.to_datetime(penerima_bantuan_df["tanggal_terima"])
        penerima_bantuan_df["tanggal_terima"] = penerima_bantuan_df["tanggal_terima"].dt.strftime("%d-%m-%Y")
        
        return penerima_bantuan_df
    
    def _data_keterangan(self):
        keterangan = {
            "nama_program": "Bantuan Sosial Keluarga Sejahtera",
            "kategori_bantuan": "Sembako",
            "sumber_dana": "APBN",
            "tahun": "2026",
        }
        
        return keterangan
    
    
    def laporan_excel(self, nama_template=None, lokasi_simpan="laporan_final.xlsx") -> io.BytesIO:
        keterangan = self._data_keterangan()
        df = self._generate_dataframe()
        
        # =========================
        # LOAD TEMPLATE
        # =========================
        if nama_template is None:
            nama_template = settings.MEDIA_ROOT / "lainnya" / "template_excel.xlsx"
        wb = load_workbook(nama_template)
        
        ws = wb.active

        # =========================
        # ISI KETERANGAN
        # =========================
        ws["D10"] = keterangan["nama_program"]
        ws["D11"] = keterangan["kategori_bantuan"]
        ws["D12"] = keterangan["sumber_dana"]
        ws["D13"] = keterangan["tahun"]

        # =========================
        # TEMPAT TABEL START
        # =========================
        start_row = 16
        start_col = 2
        
        thin = Side(style="thin")

        border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin
        )

        # header
        for col_idx, col_name in enumerate(df.columns, start_col):
            cell = ws.cell(row=start_row, column=col_idx, value=format_header(col_name))
            cell.border = border
            cell.font = Font(bold=True, size=12, name="Times New Roman")
                
        for r_idx, row in enumerate(df.itertuples(index=False), start=start_row + 1):
            for c_idx, value in enumerate(row, start_col):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.border = border
                cell.font = Font(bold=False, size=12, name="Times New Roman")
                
        # hitung posisi akhir data
        last_row = start_row + len(df)

        # posisi tanda tangan
        ttd_row = last_row + 3
        
        path_gambar = settings.MEDIA_ROOT / "lainnya" / "ttd_laporan.png"
        img = Image(path_gambar)
        ws.add_image(img, f"F{ttd_row}")

        # ws[f"D{ttd_row}"] = "Tanda Tangan"
        # ws[f"D{ttd_row + 3}"] = "Nama Penandatangan"

        # =========================
        # SAVE FILE BARU
        # =========================
        # wb.save(lokasi_simpan)
        # print("Sukses generate laporan dari template")
        
        # output
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output
    
    def laporan_pdf(self, data):
        return