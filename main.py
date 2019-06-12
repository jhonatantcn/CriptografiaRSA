"""
RSA - CRIPTOGRAFIA ASSIMÉTRICA
"""

__author__ = "Jhonatan Thallisson Cabral Néry"

from random import randint
import os
import csv
import time


def gera_pq(num_bits):

    repet_fermat = 20

    # %%%%%%% p %%%%%%%%

    num = gera_numero(num_bits)
    eprimo = primo_potencial(num, repet_fermat, num_bits)

    while eprimo is False:
        if num % 2 == 0:  # Se for par adiciono 1 para ser ímpar
            num += 1
        else:  # Se for ímpar adiciono 2 para pegar o próximo ímpar
            num += 2
        eprimo = primo_potencial(num, repet_fermat, num_bits)

    p = num

    # %%%%%%% q %%%%%%%%
    q = p
    while p == q:  # Não deixa que q 'q' seja igual a 'p' (dá erro)
        num = gera_numero(num_bits)
        eprimo = primo_potencial(num, repet_fermat, num_bits)

        while eprimo is False:
            if num % 2 == 0:  # Se for par adiciono 1 para ser ímpar
                num += 1
            else:  # Se for ímpar adiciono 2 para pegar o próximo ímpar
                num += 2
            eprimo = primo_potencial(num, repet_fermat, num_bits)

        q = num

    pq = p, q

    return pq


def gera_numero(num_bits):  # Gera número aleatório entre 3 e 2^num_bits

    numero = randint(3, pow(2, num_bits))

    return numero


def primo_potencial(num, repeticoes, numbits):  # Fermat
    if num < 1:
        return False

    while repeticoes > 0:
        a = randint(2, pow(2, numbits))

        primo = euclides_mdc(num, a)  # MÁXIMO DIVISOR COMUM

        while primo != 1:
            a = randint(2, pow(2, numbits))
            primo = euclides_mdc(num, a)

        if pow(a, num - 1, num) != 1:
            return False

        repeticoes -= 1

    return True


# Cormen. Algoritmos. 2a edição. p. 679
def euclides_mdc(a, b):

    if b == 0:  # Caso base
        return a

    mdc = euclides_mdc(b, a % b)

    return mdc


def gera_e(qe, num_bits):  # 'e' precisa ser primo relativo de (p-1)(q-1)

    e = 0

    # %%%%%%% E %%%%%%%%
    while euclides_mdc(e, qe) != 1:

        e = gera_numero(num_bits)

    # gerado o número E aleatório, precisa satisfazer a regra:
    # 1 < e < ((p - 1) * (q - 1))
    if e >= qe or e <= 1:
        gera_e(qe, num_bits)

    return e


def inverso_modular(e, qe):  # Gera d
    d = euclides_estendido(e, qe)

    if d[0] < 1:
        d[0] = d[0] + qe

    return d[0]


# Cormen. Algoritmos. 2a edição. p. 680
def euclides_estendido(a, b):

    if b == 0:
        return [1, 0, a]
    else:
        x, y, mdc = euclides_estendido(b, a % b)

        return [y, x - (a//b) * y, mdc]


def le_arquivo(arquivo):
    arq = open(arquivo, 'r')
    msg = arq.read()  # Separa cada linha como uma posição da lista

    return msg


def criptografa(mensagem, e, n):
    cript = []
    for caractere in mensagem:
        ascii2 = ord(caractere)  # ord: Transforma caractere em num ASCII
        cript.append(pow(ascii2, e, n))

    return cript


def escreve_arquivo1(arquivo, msg):

    if os.path.isfile(arquivo):  # Se já existir um arquivo de resultados de execuções anteriores
        os.remove(arquivo)  # este comando o apagará

    with open(arquivo, mode='w') as arq:
        escreva = csv.writer(arq)
        escreva.writerow(msg)
        arq.close()


def descriptografa(mensagem, d, n):
    decript = []
    aux_decript = []

    for caractere in mensagem:
        aux = chr(pow(caractere, d, n))
        aux_decript.append(aux)

    aux_decript = ''.join(aux_decript)
    decript.append(aux_decript)

    return decript


def escreve_arquivo2(arquivo, msg):
    if os.path.isfile(arquivo):  # Se já existir um arquivo de resultados de execuções anteriores
        os.remove(arquivo)  # este comando o apagará

    arq = open(arquivo, 'w')
    for x in msg:
        arq.write(x)
    arq.close()


def main():

    num_bits_pq = 16

    auxpq = gera_pq(num_bits_pq)
    p = auxpq[0]
    q = auxpq[1]
    n = p * q
    qe = (p - 1) * (q - 1)  # quociente de euler | mesma coisa que phi(n)

    num_bits_e = num_bits_pq // 2
    e = gera_e(qe, num_bits_e)

    d = inverso_modular(e, qe)  # d não pode ser negativo

    print(f'\nChave Pública: n: {n} e: {e}')
    print(f'Chave Privada: n: {n} d: {d}')

    mensagem = le_arquivo("1_textoOriginal.jtcn")
    # print(f'\n{mensagem}')

    msg_criptografada = criptografa(mensagem, e, n)
    # print(f'\n{msg_criptografada}')
    escreve_arquivo1("2_textoCriptografado.jtcn", msg_criptografada)

    # Lendo o arquivo para descriptografar
    aux_arq = open("2_textoCriptografado.jtcn", "r")
    msg_criptografada_arq = aux_arq.read().split(',')
    for y in range(len(msg_criptografada_arq)):  # Tratamento, pois é gravado como str
        msg_criptografada_arq[y] = int(msg_criptografada_arq[y])

    # Descriptografando
    msg_descriptografada = descriptografa(msg_criptografada_arq, d, n)  ####################
    # print(f'\n{msg_descriptografada}')
    escreve_arquivo2("3_textoDescriptografado.jtcn", msg_descriptografada)

    print(f'\nValores originais: \np: {p}\nq: {q}\nd: {d}')

    repet = 1
    while repet < 21: # Repito todas as quebras de chave, para deixar confiável o tempo de execução das mesmas...

        print(f'\nREPETIÇÃO {repet}\n')

        # ************************************************************************************
        # MÉTODO FORÇA BRUTA
        print('\n\n%%%%%%%%%%%% QUEBRANDO POR FORÇA BRUTA! %%%%%%%%%%%%%%%\n')
        print(f'...Quebrando p e q...')
        inicio = time.time()
        pq_quebrados = forca_bruta_pq(n)
        fim_pq = time.time()
        tempo_gasto = fim_pq - inicio
        print(f'Tempo: {tempo_gasto}')
        print(f'>> {pq_quebrados}\n')

        print(f'...Quebrando d...')
        d_quebrado = desvendando_d(pq_quebrados, e)
        fim_d = time.time()
        tempo_gasto = fim_d - fim_pq
        print(f'Tempo: {tempo_gasto}')
        print(f'>> {d_quebrado}')

        tempo_gasto = fim_d - inicio
        print(f'\nTempo Total-Força Bruta: {tempo_gasto}\n\n')

        arq_fb = open("Testes_ForcaBruta", 'a')
        arq_fb.write(f'{repet}, {tempo_gasto}\n')  # Grava testes
        arq_fb.close()

        msg_desvendada = descriptografa(msg_criptografada, d_quebrado, n)
        escreve_arquivo2("4_textoDesvendado_ForcaBruta.jtcn", msg_desvendada)
        # msg_desvendada_arq = le_arquivo("4_textoDesvendado_ForcaBruta.jtcn")

        # print('\n%%%%%%%%% MENSAGEM DESVENDADA - FORÇA BRUTA %%%%%%%%%\n')
        # print(msg_desvendada_arq)
        # print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

        # ************************************************************************************
        # MÉTODO POLLARD RHO
        print('\n\n%%%%%%%%%%%% QUEBRANDO POR POLLARD RHO! %%%%%%%%%%%%%%%\n')
        print(f'...Quebrando p e q...')
        inicio = time.time()
        pq_quebrados = pollard_rho_pq(n)
        fim_pq = time.time()
        tempo_gasto = fim_pq - inicio
        print(f'Tempo: {tempo_gasto}')
        print(f'>> {pq_quebrados}\n')

        print(f'...Quebrando d...')
        d_quebrado = desvendando_d(pq_quebrados, e)
        fim_d = time.time()
        tempo_gasto = fim_d - fim_pq
        print(f'Tempo: {tempo_gasto}')
        print(f'>> {d_quebrado}')

        tempo_gasto = fim_d - inicio
        print(f'\nTempo Total-Pollard Rho: {tempo_gasto}\n\n')

        arq_pr = open("Testes_PollardRho", 'a')
        arq_pr.write(f'{repet}, {tempo_gasto}\n')  # Grava testes
        arq_pr.close()

        msg_desvendada = descriptografa(msg_criptografada, d_quebrado, n)
        escreve_arquivo2("5_textoDesvendado_PollardRho.jtcn", msg_desvendada)
        # msg_desvendada_arq = le_arquivo("5_textoDesvendado_PollardRho.jtcn")

        # print('\n%%%%%%%%% MENSAGEM DESVENDADA - POLLARD RHO %%%%%%%%%\n')
        # print(msg_desvendada_arq)
        # print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')


        # ************************************************************************************
        # MÉTODO BRENT
        # http://connellybarnes.com/documents/factoring.pdf  P. 07
        print('\n\n%%%%%%%%%%%% QUEBRANDO POR BRENT! %%%%%%%%%%%%%%%\n')
        print(f'...Quebrando p e q...')
        inicio = time.time()
        pq_quebrados = compl_brent(brent_p(n), n)
        fim_pq = time.time()
        tempo_gasto = fim_pq - inicio
        print(f'Tempo: {tempo_gasto}')
        print(f'>> {pq_quebrados}\n')

        print(f'...Quebrando d...')
        d_quebrado = desvendando_d(pq_quebrados, e)
        fim_d = time.time()
        tempo_gasto = fim_d - fim_pq
        print(f'Tempo: {tempo_gasto}')
        print(f'>> {d_quebrado}')

        tempo_gasto = fim_d - inicio
        print(f'\nTempo Total-Brent: {tempo_gasto}\n\n')

        arq_br = open("Testes_Brent", 'a')
        arq_br.write(f'{repet}, {tempo_gasto}\n')  # Grava testes
        arq_br.close()

        msg_desvendada = descriptografa(msg_criptografada, d_quebrado, n)
        escreve_arquivo2("6_textoDesvendado_Brent.jtcn", msg_desvendada)
        # msg_desvendada_arq = le_arquivo("6_textoDesvendado_Brent.jtcn")

        # print('\n%%%%%%%%% MENSAGEM DESVENDADA - BRENT %%%%%%%%%\n')
        # print(msg_desvendada_arq)
        # print('\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

        repet += 1


def forca_bruta_pq(n):
    nbits = 1

    p = 1  # p e q são randômicos começando em 3, mas o força bruta não sabe disso

    raiz_n = (n ** (1/2))

    while p <= raiz_n:  # Testa até a raiz quadrada de n
        if primo_potencial(p, 20, nbits):
            q = n // p
            if p * q == n:
                return p, q

        if p == 1 and p == 2:
            p += 1  # Se p for 1 ou 2 acresce 1, pois 2 é o único número primo par positivo
        else:
            p += 2  # A partir de 3 testa somente os ímpares


def desvendando_d(pq, e):
    qe = (pq[0] - 1) * (pq[1] - 1)
    d = inverso_modular(e, qe)
    return d


# Cormen 2a ed
# https://asecuritysite.com/encryption/pollard
def pollard_rho_pq(n):
    i = 1
    x = randint(1, n)
    y = x
    c = randint(1, n)

    while i == 1:
        x = g(x, c) % n
        y = g(g(y, c), c) % n
        i = euclides_mdc(abs(x - y), n)

    return i, (n // i)


def g(x, c):
    return pow(x, 2) + c


# http://code.activestate.com/recipes/579049-prime-factors-of-an-integer-by-brent-algorithm/
def brent_p(N):
    # brent retorna um divisor não garantido como primo, retorna n se n primo
    if N % 2 == 0: return 2
    y, c, m = randint(1, N - 1), randint(1, N - 1), randint(1, N - 1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = ((y * y) % N + c) % N
        k = 0
        while (k < r and g == 1):
            ys = y
            for i in range(min(m, r - k)):
                y = ((y * y) % N + c) % N
                q = q * (abs(x - y)) % N
            g = euclides_mdc(q, N)
            k = k + m
        r = r * 2
    if g == N:
        while True:
            ys = ((ys * ys) % N + c) % N
            g = euclides_mdc(abs(x - ys), N)
            if g > 1: break
    return g


def compl_brent(p, n):
    q = n // p

    # if p * q == n:
    return p, q
    # else:
        # print('Erro...')


main()
