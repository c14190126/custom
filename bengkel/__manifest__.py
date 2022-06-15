{
    'name': 'Bengkel',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Alvin',
    'summary': 'Modul Bengkel SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team', 'hr', 'sale'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/transaksi_views.xml',
        'views/mobil_views.xml',
        'views/product_views.xml',
        'views/kategori_views.xml',
        'views/merek_views.xml',
        'views/hr_employee_views.xml',
        'views/res_partner_views.xml',
        'data/ir_sequence_data.xml',
        'wizard/wiz_transaksi_views.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}
