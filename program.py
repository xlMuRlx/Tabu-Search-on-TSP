import random



def prevedba_koordinat(datoteka):
    ''' Funkcija, ki dano datoteko prevede v matriko sosednosti za graf,
    katerega datoteka predstavlja. '''
    koordinate = []
    with open (datoteka) as file:
        for vrstica in file:
            koordinate.append(vrstica.split())
    n = len(koordinate)
    matrika_sosednosti = []
    for i in range(0, n):
        matrika_sosednosti.append(n*[float('inf')])
    for i in range(0, n):
        for j in range(i, n):
            prvi_kraj = (float(koordinate[i][1]), float(koordinate[i][2]))
            drugi_kraj = (float(koordinate[j][1]), float(koordinate[j][2]))
            razdalja = ((drugi_kraj[0] - prvi_kraj[0])**2 + (drugi_kraj[1] - prvi_kraj[1])**2)**(1/2)
            matrika_sosednosti[i][j] = razdalja
            matrika_sosednosti[j][i] = razdalja
    return matrika_sosednosti



def usmerjena_matrika_slovar(matrika):
    ''' Funkcija za prevajanje matrike sosednosti na slovar sosedov za
    usmerjene grafe. '''
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
    ''' Funkcija za prevajanje matrike sosednosti na slovar sosedov za
    neusmerjene grafe. '''
    n = len(matrika)
    slovar = {}
    vozlisca = []
    for i in range(0, n):
        slovar[i] = []
        vozlisca.append(i)
    for i in range(0, n):
        for j in range(i, n):
            dolzina = matrika[i][j]
            if (dolzina != 0) and (dolzina != float('inf')):
                slovar[i].append([j, dolzina])
                slovar[j].append([i, dolzina])
    return slovar, vozlisca



def dolzina_poti(pot, povezave):
    ''' Izračun dolžine dane poti glede na dolžino med posameznimi
    vozlišči, ki so dane s slovarjem povezave. '''
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
    ''' Funkcija, katero uporabljamo za iskanje kakršnekoli rešitve
    v našem grafu, ki je predstavljen s seznamom vozlisca in slovarjem
    povezave. V njej uporabljamo stevec za ugotavljanje načina, kako
    smo v neko vozlišče prišli; če ima števec vrednost 1, potem smo v
    vozlišče prišli s korakom nazaj, sicer pa s korakom naprej. '''
    zacetek = vozlisca[0]
    pot = [zacetek]
    vozlisce = zacetek
    naslednji_koraki = []
    stevec = 0
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



def okolica_poti(vozlisca, pot, povezave):
    ''' Funkcija za dano pot glede na slovar povezave poišče seznam
    poti v okolici, t.j. poti, ki jih iz dane dobimo tako, da dve
    vozlišči med seboj zamenjamo. '''
    n = len(pot)
    okolica = []
    sosedi = {}
    for i in vozlisca:
        sosedi[i] = []
        for sosed in povezave[i]:
            sosedi[i].append(sosed[0])
    for i in range(0, n-3):
        for j in range(i+3, n):
            if (pot[i] in sosedi[pot[j-1]]) and (pot[i+1] in sosedi[pot[j]]):
                nova_pot = pot[:]
                nova_pot[i+1:j] = nova_pot[i+1:j][::-1]
                if nova_pot != pot:
                    okolica.append(nova_pot)
    return okolica



def tabu_search(vozlisca, povezave, max_koraki = 100, max_tabu = 50, izpis = 25):
    ''' Končna funkcija, ki s pomočjo prej definiranih funkcij
    za dan graf, predstavljen s seznamov vozlisca in slovarjem
    povezave, s pomočjo metode Tabu Search poišče optimalno oz.
    najkrajšo pot v njem. S parametrom max_koraki se določa število
    opravljenih korakov, z max_tabu maksimalno dolžino tabu seznama,
    s številom izpis pa na koliko korakov nam izpiše dolžino poti. '''
    najboljsa = poisci_resitev(vozlisca, povezave)
    naj_dolzina = float('inf')
    pot = najboljsa[:]
    tabu = []
    koraki = 0
    while koraki < max_koraki:
        kandidati = []
        for kandidat in okolica_poti(vozlisca, pot, povezave):
            if kandidat not in tabu:
                kandidati.append(kandidat)
        if kandidati == []:
            pot = poisci_resitev(vozlisca, povezave)
            koraki += 1
        else:
            dolzina = float('inf')
            for kandidat in kandidati:
                nova_dolzina = dolzina_poti(kandidat, povezave)
                if nova_dolzina < dolzina:
                    dolzina = nova_dolzina
                    nova_pot = kandidat[:]
            tabu.append(nova_pot)
            if len(tabu) > max_tabu:
                tabu.pop(0)
            if dolzina < naj_dolzina:
                najboljsa = nova_pot[:]
                naj_dolzina = dolzina
            pot = nova_pot[:]
            if koraki % izpis == 0:
                print(naj_dolzina, ', Koraki =', koraki)
            koraki += 1
    return (najboljsa, naj_dolzina)



################################################################################
# Definiranje funkcij, ki poženejo eno izmed priloženih datotek.               #
################################################################################


# Primer za graf, katerega sliko si lahko ogledate v kratki predstavitvi
def osnovni_primer():
    vozlisca = [1, 2, 3, 4, 5, 6, 7, 8]
    povezave = {1:[[2,3], [3,2], [4,5]],
                2:[[1,3], [3,3], [5,3]],
                3:[[1,2], [2,3], [4,2], [5,5], [6,3], [7,7]],
                4:[[1,5], [3,2], [6,6]],
                5:[[2,3], [3,5], [7,4]],
                6:[[3,3], [4,6], [8,1]],
                7:[[3,7], [5,4], [8,2]],
                8:[[6,1], [7,2]]
                }
    print(tabu_search(vozlisca, povezave, 20, 10))


# Primer za Bavarsko velikosti 29
def bavarska():
    matrika = prevedba_koordinat('bavarska.txt')
    povezave, vozlisca = neusmerjena_matrika_slovar(matrika)
    print(tabu_search(vozlisca, povezave, 150, 50))


# Primer za Eilon velikosti 51
def eilon():
    matrika = prevedba_koordinat('eilon.txt')
    povezave, vozlisca = neusmerjena_matrika_slovar(matrika)
    print(tabu_search(vozlisca, povezave, 150, 50))

    
# Primer za Eilon velikosti 101
def eilon_101():
    matrika = prevedba_koordinat('eilon_101.txt')
    povezave, vozlisca = neusmerjena_matrika_slovar(matrika)
    print(tabu_search(vozlisca, povezave, 200, 100))



            
        
