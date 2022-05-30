from re import L
from flask import Blueprint, request, render_template
import pandas as pd

views = Blueprint('views', __name__)

df_rekomendasi = pd.read_csv('./website/static/rekomendasi.csv')
df_matkul = pd.read_csv('./website/static/data_matkul.csv')
df_mahasiswa = pd.read_csv('./website/static/mahasiswa_dummy.csv')

print(13518070 in df_mahasiswa['nim'])
    
def get_matkul_info(kode_matkul):
    nama_matkul = df_matkul[df_matkul['kd_kuliah'] == kode_matkul]['nama_kuliah'].values[0]
    sks = df_matkul[df_matkul['kd_kuliah'] == kode_matkul]['sks'].values[0]
    return [nama_matkul, sks]

def get_mahasiswa_info(nim):
    isNIMExist = nim in df_mahasiswa['nim'].unique()
    if(isNIMExist):
        nama = df_mahasiswa[df_mahasiswa['nim'] == nim]['nama'].values[0]
        semester = df_mahasiswa[df_mahasiswa['nim'] == nim]['semester'].values[0]
        prodi = df_mahasiswa[df_mahasiswa['nim'] == nim]['program studi'].values[0]
        sks = df_mahasiswa[df_mahasiswa['nim'] == nim]['sks sudah diambil'].values[0]
        
        return {
            'nim': nim,
            'nama': nama,
            'semester': semester, 
            'prodi': prodi,
            'sks': sks
        }
    else:
        return {
            'nim': nim,
            'nama': 'nama_dummy',
            'semester': 'semester_dummy', 
            'prodi': 'program_studi_dummy',
            'sks': 'sks_dummy'
        }

@views.route('/')
def home():
    return render_template("page.html")

@views.route('/', methods=['POST'])
def my_form_post():
    nim = request.form["nim"]
    hasil = get_mahasiswa_info(int(nim))

    isNIMExist = int(nim) in df_rekomendasi['id_mhs'].unique()

    if(isNIMExist):
        matkul_rekomendasi = df_rekomendasi[df_rekomendasi['id_mhs'] == int(nim)]['rekomendasi matkul'].values[0].split(', ')
        
        matkul = []
        for el in matkul_rekomendasi:
            data = get_matkul_info(el)
            matkul.append({
                'kode': el,
                'nama': data[0],
                'sks': data[1]
            })
    else:
        matkul = []
    
    return render_template("page.html", profil=hasil, matkul=matkul)

