import random

vozlisca = [1, 2, 3, 4, 5, 6, 7, 8]

povezave = {1:[[2,3], [3,2], [4,5]],
            2:[[1,3], [3,3], [5,3]],
            3:[[1,2], [2,3], [4,2], [5,5], [6,3], [7,7]],
            4:[[1,5], [3,2], [6,6]],
            5:[[2,3], [3,5], [7,4]],
            6:[[3,3], [4,3], [8,1]],
            7:[[3,7], [5,4], [8,2]],
            8:[[6,1], [7,2]]
            }



def prevedba_koordinat(n, datoteka):
    kordinate = []
    for i in range(n):
        vrstica = []
        for j in range(n):
            vrstica.append(0)
        kordinate.append(vrstica)
    f = open(datoteka, "r")
    for i in range(n):
        kordinate[i] = f.readline().split()
        for j in range(3):
            kordinate[i][j] = float(kordinate[i][j])
    matrika_sosednosti = []
    for i in range(n):
        vrstica = []
        for j in range(n):
            vrstica.append(0)
        matrika_sosednosti.append(vrstica)
    for i in range(n):
        for j in range(n):
            matrika_sosednosti[i][j] = (abs(kordinate[i][1]-kordinate[j][1])**2 + abs(kordinate[i][2] - kordinate[j][2])**2)**(1/2)
    return matrika_sosednosti



def usmerjena_matrika_slovar(matrika):
    slovar = {}
    stevec1 = 1
    vozlisca = []
    for vrstica in matrika:
        sosedi = []
        stevec2 = 1
        for sosed in vrstica:
            if (sosed != 0) and (sosed != float('inf')):
                sosedi.append([stevec2, sosed])
            stevec2 += 1
        slovar[stevec1] = sosedi
        vozlisca.append(stevec1)
        stevec1 += 1
    return slovar, vozlisca



def neusmerjena_matrika_slovar(matrika):
    n = len(matrika)
    slovar = {}
    vozlisca = []
    for i in range(0, n-1):
        slovar[i] = []
        vozlisca.append(i)
    for i in range(0, n-1):
        for j in range(i, n-1):
            dolzina = matrika[i][j]
            if (dolzina != 0) and (dolzina != float('inf')):
                slovar[i].append([j, dolzina])
                slovar[j].append([i, dolzina])
    return slovar, vozlisca



def dolzina_poti(pot, povezave):
    dolzina = 0
    for i in range(0, len(pot)-1):
        vozlisce = pot[i]
        sosedi = []
        for sosed in povezave[vozlisce]:
            sosedi.append(sosed[0])
            if pot[i+1] == sosed[0]:
                dolzina += sosed[1]
        if pot[i+1] not in sosedi:
            return float('inf')
    return dolzina


                
def poisci_resitev(vozlisca, povezave):
    zacetek = vozlisca[0]
    pot = [zacetek]
    vozlisce = zacetek
    naslednji_koraki = []
    stevec = 0 #gleda, kako smo do vozlišča prišli, t.j. bodisi z normalnim
            #korakom naprej (stevec = 0) bodisi s korakom nazaj (stevec = 1)
    while True:
        if stevec == 0:
            sosedi = []
            for sosed in povezave[vozlisce]:
                if sosed[0] not in pot:
                    sosedi.append(sosed[0])
            naslednji_koraki.append(sosedi)
        izbire = naslednji_koraki[-1][:]
        if izbire == []:
            pot.remove(vozlisce)
            naslednji_koraki.remove(izbire)
            naslednji_koraki[-1].remove(vozlisce)
            vozlisce = pot[-1]
            stevec = 1
        else:
            random.shuffle(izbire)
            novo_vozlisce = izbire.pop(0)
            pot.append(novo_vozlisce)
            if len(pot) == len(vozlisca):
                koncni_sosedi = []
                for sosed in povezave[novo_vozlisce]:
                    koncni_sosedi.append(sosed[0])
                if zacetek in koncni_sosedi:
                    pot.append(zacetek)
                    return pot
                else:
                    pot.remove(novo_vozlisce)
                    naslednji_koraki[-1].remove(novo_vozlisce)
                    vozlisce = pot[-1]
                    stevec = 1
            else:
                vozlisce = novo_vozlisce
                stevec = 0



def okolica_poti(pot, povezave):
    sosedje = []
    for vozlisce in pot:
        for sosed in povezave.get(vozlisce):
            if ((sosed[0] != vozlisca[0]) and (vozlisce != vozlisca[0])):
                nova_pot = pot[:]
                a, b = nova_pot.index(vozlisce), nova_pot.index(sosed[0])
                nova_pot[a], nova_pot[b] = nova_pot[b], nova_pot[a]
                if nova_pot not in sosedje:
                    if dolzina_poti(nova_pot, povezave) != float('inf'):
                        sosedje.append(nova_pot)
                nova_pot = pot
    return sosedje



def tabu_search(vozlisca, povezave):
    najboljsa = poisci_resitev(vozlisca, povezave)
    naj_dolzina = float('inf')
    pot = najboljsa[:]
    tabu = []
    koraki = 0
    while koraki < 100:
        kandidati = []
        for kandidat in okolica_poti(pot, povezave):
            kandidati.append(kandidat)
        razlika = []
        for kandidat in kandidati:
            if kandidat not in tabu:
                razlika.append(kandidat)
        if razlika == []:
            pot = poisci_resitev(vozlisca, povezave)
            koraki += 1
        else:
            dolzina = float('inf')
            for kandidat in razlika:
                if dolzina_poti(kandidat, povezave) < dolzina:
                    dolzina = dolzina_poti(kandidat, povezave)
                    nova_pot = kandidat[:]
            tabu.append(nova_pot)
            if len(tabu) > 50:
                tabu.pop(0)
            nova_dolzina = dolzina_poti(nova_pot, povezave)
            if nova_dolzina < naj_dolzina:
                najboljsa = nova_pot[:]
                naj_dolzina = nova_dolzina
            pot = nova_pot[:]
            koraki += 1
    return (najboljsa, naj_dolzina)












            
        
