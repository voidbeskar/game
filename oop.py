class Kucingpeliharaan:
    def __init__(self, nama):
        self.nama = nama
        self.energi = 50
        self.lapar = 50

    def status(self):
        print (f"\n--- STATUS{self.nama.upper()}---")
        print (f"\n energi : {self.energi}/100")
        print (f"\n lapar : {self.lapar}/100")

    def makan(self):
        print (f"{self.nama} sedang makan...")
        self.lapar -=20
        self.energi +=20

        if self.lapar <0: self.laper = 0
        if self.energi >100: self.energi = 100

    def main(self):
        if self.energi <=20:
            print (f"{self.nama} terlalu lelah bermain butuh istirahat")
        else:
            print (f"{self.nama} sedang bermain")
            self.energi -=20
            self.lapar +=20

        if self.energi <0 : self.energi = 0 
        if self.lapar >100 : self.lapar = 100

    def tidur(self):
        print (f"{self.nama} sedang tidur...")
        self.energi +=40
        self.lapar +=10      

        if self.energi >100 : self.energi = 100
        if self.laper >100 : self.lapar = 100

def main():
    print ("======selamat datang di game simulasi memelihar kucing======")
    nama_kucing = input("masukan nama kucing anda :")

    kucingku = Kucingpeliharaan(nama_kucing)

    while True:
        kucingku.status()
        print ("apa yang ingin kamu lakukan")
        print ("1.memberi makan")
        print ("2.mengajak bermain")
        print ("3.tidurkan")
        print ("4.keluar")

        pilihan = input("masukan pilihan anda:")

        if pilihan =="1":
            kucingku.makan()
        if pilihan =="2":
            kucingku.main()
        if pilihan =="3":
            kucingku.tidur()
        if pilihan =="4":
            print (f"terima kasih sudah merawat kucing ku {nama_kucing}")
        else:
            print ("pilihan tidak valid")

if __name__=="__main__":
    main()                              