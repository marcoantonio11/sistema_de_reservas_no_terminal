__version__ = "1.0.2"
__author__ = "Marco Silva"
__email__ = "marcoa.silva84@gmail.com"
__license__ = "MIT"
__created__ = "03/07/2025"

import os
import sys
import time
import logging
from logging import handlers

# TODO: usar funções
log_level = os.getenv("LOG_LEVEL", "WARNING").upper()

log = logging.Logger("app_reserva", log_level)

fh = handlers.RotatingFileHandler(
    "app_reserva.log",
    maxBytes=10**6,
    backupCount=10
    )
fh.setLevel(log_level)

fmt = logging.Formatter(
    '%(asctime)s  %(name)s  %(levelname)s  l:%(lineno)d' \
    '  f:%(filename)s: %(message)s'
)

fh.setFormatter(fmt)
log.addHandler(fh)

log.info("Sistema iniciado.")

PATH = os.curdir
ROOMS_FILEPATH = os.path.join(PATH, "quartos.txt")
RESERVATION_FILEPATH = os.path.join(PATH, "reservas.txt")

user = os.getenv("USER","anônimo(a)")
print("")
print("#" * 66)
print(f"{' Olá ' + user.capitalize() +', bem-vindo(a) ao TReservas! ':#^66}")
print("#" * 66)
print("")

leave_while = False
while True:
    print("O que você deseja fazer?\n")
    print("(1) Fazer uma reserva.")
    print("(2) Visualizar os dados da sua reserva.")
    print("(3) Cancelar uma reserva.")
    print("(4) Sair.\n")

    try:
        option_choosen = int(input("Digite a opção escolhida: "))
        print("")
        print("-" * 66)
        print("")
    except ValueError as e:
        print(f"[ERROR] {e}")
        log.error(e)
        sys.exit(1)

    if option_choosen == 1:
        log.debug(f"usuario escolheu a opcao {option_choosen}.")
        print("Você escolheu a opção: (1) Fazer uma reserva.\n")
        print("Nós trabalhamos com os seguintes tipos de quartos:")
        
        try:
            with open(ROOMS_FILEPATH) as rooms_file:
                for line in rooms_file:
                    file_parts = line.strip().split(",")
                    print(file_parts[1])
                print("")
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        print("Vamos exibir os quartos disponíveis no momento.")
        time.sleep(1)
        print("Buscando quartos disponíveis...\n")
        time.sleep(1)
        
        try:
            with open(ROOMS_FILEPATH) as rooms_file:
                all_rooms_code = []
                for line in rooms_file:
                    file_parts = line.strip().split(",")
                    all_rooms_code += file_parts[0]
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        try:    
            with open(RESERVATION_FILEPATH) as reservation_file:
                reserved_rooms_code = []
                for line in reservation_file:
                    line = line.strip()
                    if not line:
                        continue
                    file_parts = line.split(",")
                    reserved_rooms_code += file_parts[1]
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        busy_rooms = set(all_rooms_code) & set(list(reserved_rooms_code))
        
        print("NÚMERO - NOME DO QUARTO - DIÁRIA")

        try:
            any_room_found = False
            with open(ROOMS_FILEPATH) as rooms_file:
                for line in rooms_file:
                    room_code, room_name, room_price = line.split(",")
                    if room_code not in busy_rooms:
                        print(f"{room_code:<6} - {room_name:<14} - {room_price}")
                        any_room_found = True                
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)    
        
        while True:
            answer_confirm_reserve = input("Deseja prosseguir com a reserva para algum destes quartos (y/n)? ")
            print("")
            print("-" * 66)
            print("")
            if answer_confirm_reserve.lower() == 'y':
                print("Por favor preencha os dados abaixo:\n")
                break
            elif answer_confirm_reserve.lower() == 'n':
                print("Saindo do sistema...")
                log.info("Usuario optou por não prosseguir com a reserva.")
                time.sleep(1)
                leave_while = True
                break
            else:
                print("Opção inválida! Digite `y` ou `n`.")
                print("")
                print("-" * 66)
                print("")
                continue

        if leave_while:
            break
        leave_while = False

        if not any_room_found:
            print("Nenhum quarto disponível no momento.\n")
            log.info("Nenhum quarto disponivel no momento.")        
            continue_while = False    
            while True:
                answer_menu_1 = input("Deseja realizar outra operação (y/n)? ")
                print("")
                print("-" * 66)
                print("")
                if answer_menu_1.lower() == 'y':
                    print("Voltando ao menu inicial...\n")
                    time.sleep(2)
                    continue_while = True
                    break
                            
                elif answer_menu_1.lower() == 'n':
                    print("Saindo do sistema...")
                    time.sleep(2)
                    leave_while = True
                    break
                else:
                    print("Opção inválida! Digite `y` ou `n`.")
                    print("")
                    print("-" * 66)
                    print("")
                    continue
            
            if continue_while:
                continue
            if leave_while:
                break                             
        continue_while = False
        leave_while = False
        
        guest_name = input("Digite o nome do hóspede: ").title().strip()
        guest_full_name = " ".join(guest_name.split())
        guest_full_name_no_space = "".join(guest_name.split())

        if not guest_full_name_no_space.isalpha():
                print("[ERRO] O Nome deve conter apenas letras e espaços!")
                print(f"Você digitou `{guest_name}`")
                letter_not_allowed = []
                for letter in guest_name:
                    if not letter.isalpha() and not letter.isspace(): 
                        letter_not_allowed += letter
                print(f"Caractere(s) inválido(s): {letter_not_allowed}.")
                log.error(f"Usuario digitou o nome com caracteres invalidos. "
                          f"nome={guest_name}, caracteres_invalidos={letter_not_allowed}")
                sys.exit(1)

        try:
            code = int(input("Digite o código do quarto: "))
        except ValueError as e:
            print(f"[ERROR] {(e)}")
            log.error(e)
            sys.exit(1)

        try:
            days = int(input("Digite a quantidade de dias: "))
        except ValueError as e:
            print(f"[ERROR] {(e)}")
            log.error(e)
            sys.exit(1)

        print("")

        try:
            code_found = False
            total_value = float
            with open(ROOMS_FILEPATH) as rooms_file:
                for rooms_file_line in rooms_file:
                    room_code, room_name, room_price = rooms_file_line.strip().split(",")
                    if str(code) in room_code:
                        with open(RESERVATION_FILEPATH) as reservation_file:
                            for reservation_file_line in reservation_file:
                                reservation_file_parts = reservation_file_line.strip().split(",")
                                reservation_code = reservation_file_parts[1].strip()                 
                                if str(code) in reservation_code.strip():
                                    print(f"Você selecionou o quarto {room_code},{room_name}, {room_price}")
                                    print(f"O quarto selecionado já está ocupado.")
                                    print("Saindo do sistema...")
                                    log.warning(f"Tentativa de reservar um quarto ja ocupado: "
                                                f"usuario={user}, "
                                                f"hospede={guest_name}, "
                                                f"codigo_quarto={room_code}, "
                                                f"nome_quarto={room_name}, "
                                                f"preco_quarto={room_price}")
                                    time.sleep(1)
                                    sys.exit(1)
                        with open(RESERVATION_FILEPATH, "a") as reservation_file:
                            reservation_file.write(f"{guest_full_name},{code},{days}\n")
                            total_value = float(room_price) * int(days)
                            print("Sua reserva foi concluída com sucesso.")
                            print("Segue um resumo da sua reserva:\n")
                            print(f"Nome: {guest_name}")
                            print(f"Código do quarto: {room_code}")
                            print(f"Nome do quarto: {room_name}")
                            print(f"Quantidade de dias: {days}")
                            print(f"Valor total: {total_value}")
                            code_found = True
            log.info(f"Reserva efetuada: "
                     f"usuário={user}, "
                     f"hospede={guest_name}, "
                     f"codigo_quarto={room_code}, "
                     f"nome_quarto={room_name}, "
                     f"qtd_dias={days}, "
                     f"valor_total={total_value}")        
            if not code_found:
                print("Código do quarto não encontrado!\n")
                log.warning(f"Usuario digitou um codigo de quarto invalido.")
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)


    elif option_choosen == 2:
        log.debug(f"usuario escolheu a opcao {option_choosen}.")
        print("Você escolheu a opção: (2) Visualizar os dados da sua reserva.\n")
        guest_name = input("Digite o nome cadastrado na reserva: ").title()
        guest_full_name = " ".join(guest_name.split())
        guest_full_name_no_space = "".join(guest_name.split())

        if not guest_full_name_no_space.isalpha():
                print("[ERRO] O Nome deve conter apenas letras e espaços!")
                print(f"Você digitou `{guest_name}`")
                letter_not_allowed = []
                for letter in guest_name:
                    if not letter.isalpha() and not letter.isspace(): 
                        letter_not_allowed += letter
                print(f"Caractere(s) inválido(s): {letter_not_allowed}.")
                log.error(f"Usuario digitou o nome com caracteres invalidos. "
                          f"nome={guest_name}, caracteres_invalidos={letter_not_allowed}")
                sys.exit(1)
        try:
            with open(RESERVATION_FILEPATH) as reservation_file:
                list_reserve_guest_name = []
                for line in reservation_file:
                    file_parts = line.strip().split(",")
                    reserve_guest_name = file_parts[0]
                    list_reserve_guest_name.append(reserve_guest_name)
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        try:
            if guest_name in list_reserve_guest_name:
                with open(RESERVATION_FILEPATH) as reservation_file:
                    for line in reservation_file:
                        file_parts = line.strip().split(",")
                        if guest_name in file_parts[0]:
                            print("Seguem os dados da sua reserva:\n")
                            print(f"Nome: {guest_name}")
                            print(f"Código do quarto: {file_parts[1]}")
                            print(f"Quantidade de dias: {file_parts[2]}")
                            log.debug(f"Hospede {guest_name} consultou a sua reserva no quarto {file_parts[1]}")
            else:
                print(f"Nenhuma reserva encontrada para {guest_name}.")
                log.info(f"Nenhuma reserva encontrada para {guest_name}")
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

    elif option_choosen == 3:
        log.debug(f"usuario escolheu a opcao {option_choosen}.")
        print("Você escolheu a opção: (3) Cancelar uma reserva.\n")
        guest_name = input("Digite o nome cadastrado na reserva: ").title()
        guest_full_name = " ".join(guest_name.split())
        guest_full_name_no_space = "".join(guest_name.split())

        if not guest_full_name_no_space.isalpha():
                print("[ERRO] O Nome deve conter apenas letras e espaços!")
                print(f"Você digitou `{guest_name}`")
                letter_not_allowed = []
                for letter in guest_name:
                    if not letter.isalpha() and not letter.isspace(): 
                        letter_not_allowed += letter
                print(f"Caractere(s) inválido(s): {letter_not_allowed}.")
                log.error(f"Usuario digitou o nome com caracteres invalidos. "
                          f"nome={guest_name}, caracteres_invalidos={letter_not_allowed}")
                sys.exit(1) 

        try:
            with open(RESERVATION_FILEPATH) as reservation_file:
                list_reserve_guest_name = []
                for line_reserve in reservation_file:
                    file_parts = line_reserve.strip().split(",")
                    reserve_guest_name = file_parts[0]
                    list_reserve_guest_name.append(reserve_guest_name)
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        try:    
            with open(RESERVATION_FILEPATH) as reservation_file:
                for line in reservation_file:
                    reserve_guest_name, room_code, days = line.strip().split(",")
                    if line.startswith(guest_name + ","):
                        print("Dados da reserva:\n")
                        print(f"Nome: {reserve_guest_name}")
                        print(f"Código do quarto: {room_code}")
                        print(f"Quantidade de dias: {days}\n")
                        while True:
                            answer_cancel = input("Deseja realmente cancelar (y/n)? ")
                            print("")
                            if answer_cancel.lower() == "y":
                                print("Cancelando a reserva...")
                                time.sleep(1)
                                break
                            elif answer_cancel.lower() == "n":
                                print("Saindo do sistema...")
                                time.sleep(1)
                                log.info(f"Hospede {reserve_guest_name} desistiu de cancelar a reserva.")
                                sys.exit(1)
                            else:
                                print("Opção inválida! Por favor escolha `y` ou `n`.")
                                print("")
                                print("-" * 66)
                                print("")
                                continue
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        try:                      
            with open(RESERVATION_FILEPATH) as reservation_file:
                lines = reservation_file.readlines()
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

        try:
            if guest_name in list_reserve_guest_name:
                with open(RESERVATION_FILEPATH, 'w') as reservation_file:
                    for line in lines:  
                        if not line.startswith(guest_name + ","):
                            reservation_file.write(line)
                    print("Reserva cancelada com sucesso!")
                log.info(f"Reserva cancelada: "
                         f"usuario={user}, "
                         f"hospede={reserve_guest_name}, "
                         f"codigo_quarto={room_code}, "
                         f"qtd_dias={days}")
            else:
                print(f"Nenhuma reserva encontrada para {guest_name}.")
                log.info(f"Nenhuma reserva encontrada para {guest_name}.")
        except FileNotFoundError as e:
            print(e)
            log.error(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            log.error(e)
            sys.exit(1)

    elif option_choosen == 4:
        print("Saindo do sistema...")
        log.debug(f"Usuario selecionou a opção {option_choosen}. Sistema encerrado.")
        time.sleep(1)
        sys.exit(1)

    else:
        print("Opção inválida! Favor escolha entre 1 e 4.")
        log.debug(f"Usuario escolheu uma opção inválida. Opcao `{option_choosen}`")
        print("")
        print("-" * 66)
        print("")
        continue
    
    print("")

    while True:
        answer_menu_2 = input("Deseja realizar outra operação (y/n)? ")
        print("")
        print("-" * 66)
        print("")
        if answer_menu_2.lower() == 'y':
            print("Voltando ao menu inicial...\n")
            time.sleep(1)
            break
        elif answer_menu_2.lower() == 'n':
            print("Saindo do sistema...")
            time.sleep(1)
            leave_while = True
            break
        else:
            print("Opção inválida! Digite `y` ou `n`.")
            print("")
            print("-" * 66)
            print("")
            continue
    if leave_while:
        break
    leave_while = False