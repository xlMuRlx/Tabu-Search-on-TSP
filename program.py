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
    prepovedani = {}
    for v in vozlisca:
        prepovedani[v] = []
    while True:
        sosedi = []
        for sosed in povezave[vozlisce]:
            if (sosed[0] not in pot) and (sosed[0] not in prepovedani[vozlisce]):
                sosedi.append(sosed[0])
        if sosedi == []:
            pot.remove(vozlisce)
            vozlisce = pot[-1]
        else:
            random.shuffle(sosedi)
            novo_vozlisce = sosedi.pop(0)
            pot.append(novo_vozlisce)
            if len(pot) == len(vozlisca):
                koncni_sosedi = []
                for sosed in povezave[vozlisce]:
                    koncni_sosedi.append(sosed[0])
                if zacetek in koncni_sosedi:
                    pot.append(zacetek)
                    return pot
                else:
                    pot.remove(vozlisce)
                    prepovedani[vozlisce].append(novo_vozlisce)
                    vozlisce = pot[-1]
            else:
                vozlisce = novo_vozlisce
                


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



# Preveri še primer, če dobiš pot brez okolice!!!
def tabu_search(vozlisca, povezave):
    najboljsa = poisci_resitev(vozlisca, povezave)
    pot = najboljsa[:]
    tabu = []
    koraki = 0
    while koraki < 10000:
        kandidati = okolica_poti(pot, povezave)
        dolzina = float('inf')
        for kandidat in kandidati:
            if kandidat not in tabu:
                if dolzina_poti(kandidat, povezave) < dolzina:
                    dolzina = dolzina_poti(kandidat, povezave)
                    nova_pot = kandidat[:]
        if nova_pot not in tabu:
            tabu.append(nova_pot)
        if len(tabu) > 100:
            tabu.pop(0)
        if dolzina_poti(nova_pot, povezave) < dolzina_poti(najboljsa, povezave):
            najboljsa = nova_pot[:]
        pot = nova_pot[:]
        koraki += 1
    return najboljsa







            
        
