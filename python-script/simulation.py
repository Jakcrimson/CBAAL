from CBAA_sim import CBAA
from CBBA_sim import CBBA



if __name__ == "__main__":
    print(r"""

   ____    ____      _         _       _      
U /"___|U | __")uU  /"\  u U  /"\  u  |"|     
\| | u   \|  _ \/ \/ _ \/   \/ _ \/ U | | u   
 | |/__   | |_) | / ___ \   / ___ \  \| |/__  
  \____|  |____/ /_/   \_\ /_/   \_\  |_____| 
 _// \\  _|| \\_  \\    >>  \\    >>  //  \\  
(__)(__)(__) (__)(__)  (__)(__)  (__)(_")("_) 
          
CONSENSUS-BASED AUCTION ALGORITHMS LIBRARY
          by. Pierre LAGUE
""")
    while True:
        algo = input("[+] Choose your simulation : \n\t(1) CBAA\n\t(2) CBBA\n")
        if int(algo) == 2:
            pass
        elif int(algo) == 1:
            cbaa = CBAA().simulation(10, 10, 50, True, 2)
            break
        else:
            algo = input("[+] Choose your simulation : \n\t(1) CBAA\n\t(2) CBBA")
