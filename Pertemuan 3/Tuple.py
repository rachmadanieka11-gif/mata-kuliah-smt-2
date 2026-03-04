import sys
#membuat struktur Tuple 
logApps  = ("user1 login",) 
print  (logApps)
print (sys.getsizeof(logApps))

#membuktikan memory Tuple lebih efisien dari list 
logAppsList = ["user1 login"]
print(logAppsList)
print("memiliki ukurna list", sys.getsizeof(logAppsList))
print("akbarganteng")

#pembuktian Tuple tidak bisa diubaT
# 1. Tambah 
# logsApps.append("user4 login")
# 2. Ubah
# logsApps[0] "user1 logout" 
#3. Hapus 
# del logApps
#pembuktian Tuple bisa diakses dengan index

print(logApps[0])

#menduplikat Tuple
logAppsBackup = logApps
print ("ini isi logsApps Backup", logApps)
print ("ini isi logsApps", logApps)