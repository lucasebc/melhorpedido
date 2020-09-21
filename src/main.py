import argparse

import cli

# def main_gui():
#     import gui
#     gui.gui()

def main():
    cli.cli() 


parser = argparse.ArgumentParser(description='Melhor pedido de compras')
# parser.add_argument('-gui', help='iniciar com a interface gráfica.', action='store_true')

args = parser.parse_args() 

if __name__ == "__main__":
    main()
    # main() if not args.gui else main_gui()
