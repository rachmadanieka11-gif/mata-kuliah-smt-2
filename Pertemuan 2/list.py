#List
lst_1 = [1,2,3]
lst_2 = [4,5,6]
lst_3 = [7,8,9]
lst = [lst_1, lst_2, lst_3]
lst
print(lst)
#sifat list
#fleksibilitas Tipe Data Elemen List
listku = ["mahardika", 1, True, 4.6]
print (listku)

#mutable(manipulasi)
listku[0]
listku[1]
listku[2]
listku[3]
print(listku)

#slicing(memotong)
warna = ["merah", "hijau","biru", "kuning", "jingga", "pink"]
print(warna[1:5])

#tinggi badan
listtinggi_badan = [160,170,182,155,168]
print(listtinggi_badan[:4])
#ganti data
listtinggi_badan = [162,177,182,150,166]
print(listtinggi_badan[:4])

#data
suhu_keluarga_ucup =['ayah ucup', 19, 'ucup', 19, 'ibu ucup', 20]
#mengubah suhu
suhu_keluarga_ucup[3] = [24]
print(suhu_keluarga_ucup)

suhu_keluarga_ucup[-2:] = ['mamah ucup', 22]
print(suhu_keluarga_ucup)

#menghapus elemen list
murid = ['Ayu', 'Bagas', 'Fajar', 'Cahyo', 'Ani']
del murid[2]
print(murid[2])
murid = ['Ayu', 'Bagas', 'Fajar', 'Cahyo', 'Ani']
murid.remove('Cahyo')
print(murid)

#list comprehension
number =[1,5,10,6,7,8,12]
result = [i for i in number if i>6]
print(result)

m = [x for x in range(10,101,10)]
print(m)
n = [j*j for j in range (10)] 
print(n)
