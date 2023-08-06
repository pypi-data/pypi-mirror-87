import sys
from colorama import init, Fore, Style

cat = """
           _                        
           \`*-.                    
            )  _`-.                 
           .  : `. .                
           : _   '  \               
           ; *` _.   `*-._          
           `-.-'          `-.       
             ;       `       `.     
             :.       .        \    
             . \  .   :   .-'   .   
             '  `+.;  ;  '      :   
             :  '  |    ;       ;-. 
             ; '   : :`-:     _.`* ;
 [ .... ] .*' /  .*' ; .*`- +'  `*' 
          `*-*   `*-*  `*-*'
"""

signature = "Art by Blazej Kozlowski"
source_url = "https://www.asciiart.eu/animals/cats"

def meow(args=None):
  phrase = " ".join(args) if args else "Meow"  
  offset = " " * (len(phrase) - 4)
  lines = list(map(lambda x: offset + x, cat.split('\n')))
  phrase = Fore.CYAN + phrase + Style.RESET_ALL
  lines[-3] = lines[-3].replace("....", phrase)[len(offset):]
  lines.append(" " * (len(offset) + 24) + (Style.DIM + signature + Style.RESET_ALL))
  lines.append(" " * (len(offset) + 24) + (Style.DIM + source_url + Style.RESET_ALL))
  print("\n".join(lines))
  print()


def main():
  init()

  meow(sys.argv[1:])