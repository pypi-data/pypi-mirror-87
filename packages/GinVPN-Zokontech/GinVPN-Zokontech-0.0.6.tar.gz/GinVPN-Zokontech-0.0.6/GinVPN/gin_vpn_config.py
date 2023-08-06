import sys, os
from pyautogui import typewrite
import secrets


def get_valid_int_selection(prompts, min, max):
    while True:
        s=input(prompts[0])
        try:
            i=int(s)
            if(i in range(min, max)):
                return i
            else:
                print(prompts[1])
        except ValueError:
            print(prompts[2])

def yes_no():
    a=input('y/n?')
    while True:
        if(a[0].lower()=='y'):
            return True
        elif(a[0].lower()=='n'):
            return False
        else:
            print("Please Enter Y or N")

def menu_choice(name, options_list):
    print(name)
    for i in range(0, len(options_list)):
        print(str(i+1)+'. '+options_list[i])
    print()
    prompts=['Enter Valid Selection: ', 'Choice Out Of Range', 'Invalid Selection']
    return get_valid_int_selection(prompts, 1, len(options_list)+1)
    

def main():
    try:
        import GinSettings
        try:
            key=GinSettings.key
        except AttributeError:
            key="Vrz19NDnmgmqvJw0fm4R3Zadi7OLLVoA"
        try:
            server_adr=GinSettings.server_adr
        except AttributeError:
            server_adr='127.0.0.1'
        try:
            server_port=GinSettings.server_port
        except AttributeError:
            server_port=5000
    except ModuleNotFoundError:
        print('Running First Time Setup')
        print("Generating Key...")
        key=secrets.token_bytes(32)
        server_adr='127.0.0.1'
        server_port=5000
        print("Enter VPN Server Address: ")
        typewrite(server_adr)
        server_adr = input()
        typewrite(str(server_port))
        prompts=['Enter VPN Port Address: ', 'Invalid Port', 'Invalid Port']
        server_port = get_valid_int_selection(prompts, 1024, 65535)
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, 'GinSettings.py'), 'w')
        f.write('key='+str(key)+'\n'+'server_adr='+'\''+server_adr+'\''+'\n'+'server_port='+str(server_port))
        f.close()
        return
        

    menu_name='Config Options'
    menu_options=['Generate New Key', 'Change VPN Server', 'Change VPN Port', 'Save Changes and Quit', 'Quit Config']

    while True:
        i=menu_choice('\n'+menu_name, menu_options)
        if i==1:
            print("Generating Key...")
            key=secrets.token_bytes(32)
        if i==2:
            print("Enter VPN Server Address: ")
            typewrite(server_adr)
            server_adr = input()
        if i==3:
            typewrite(str(server_port))
            prompts=['Enter VPN Port Address: ', 'Invalid Port', 'Invalid Port']
            server_port = get_valid_int_selection(prompts, 1024, 65535)
        if i==4:
            if yes_no():
                print("Saving Options")
                __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
                f = open(os.path.join(__location__, 'GinSettings.py'), 'w')
                f.write('key='+str(key)+'\n'+'server_adr='+'\''+server_adr+'\''+'\n'+'server_port='+str(server_port))
                f.close()
                break
        if i==5:
            if yes_no():
                break

if __name__=='__main__':
    main()
