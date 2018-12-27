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

##povezave1 = [(1,2,3), (1,3,2), (1,4,5), (2,1,3), (2,3,3), (2,5,3), (3,1,2),
##            (3,2,3), (3,4,2), (3,5,5), (3,6,3), (3,7,7), (4,1,5), (4,3,2),
##            (4,6,6), (5,2,3), (5,3,5), (5,7,4), (6,3,3), (6,3,4), (6,8,1),
##            (7,3,7), (7,5,4), (7,8,2), (8,6,1), (8,7,2)]
##
##a = float('inf')
##povezave2 = [[0, 3, 2, 5, a, a, a, a],
##             [3, 0, 3, a, 3, a, a, a],
##             [2, 3, 0, 2, 5, 3, 7, a],
##             [5, a, 2, 0, a, 6, a, a],
##             [a, 3, 5, a, 0, a, 4, a],
##             [a, a, 3, 6, a, 0, a, 1],
##             [a, a, 7, a, 4, a, 0, 2],
##             [a, a, a, a, a, 1, 2, 0]]



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


def poisci_resitev_slabo(vozlisca, povezave):
    zacetek = vozlisca.pop(0)
    ostala = vozlisca
    korak = 0
    while True:
        pot = [zacetek] + ostala + [zacetek]
        if dolzina_poti(pot, povezave) != float('inf'):
            print(korak)
            return pot
        random.shuffle(ostala)
        korak += 1



def poisci_resitev(vozlisca, povezave):
    zacetek = vozlisca[0]
    neobiskana = vozlisca
    pot = [zacetek]
    obiskana = []
    korak = 0
    while True:
        novo_vozlisce = random.choice(povezave[zacetek])[0]
        if novo_vozlisce not in obiskana:
            pot.append(novo_vozlisce)
            obiskana.append(novo_vozlisce)
            neobiskana.remove(novo_vozlisce)
            zacetek = novo_vozlisce
            if neobiskana == []:
                if pot[0] == pot[-1]:
                    if dolzina_poti(pot, povezave) != float('inf'):
                        return pot
                poisci_resitev(vozlisca, povezave)
        korak += 1
        if korak > 10000:
            print('Napaka!')
            break
                


def okolica_poti(pot, povezave):
    n = len(pot)
    okolica = []
    nova_pot = pot
    for i in range(1, n-2):
        for j in range(2, n-2):
            a = nova_pot[i]
            nova_pot[i] = nova_pot[j]
            nova_pot[j] = a
            if dolzina_poti(nova_pot, povezave) != float('inf'):
                print(nova_pot)
                if nova_pot not in okolica:
                    okolica.append(nova_pot)
                    print(okolica)
            nova_pot = pot
    return okolica







            
        
