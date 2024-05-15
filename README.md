```
   ____    ____      _         _       _      
U /"___|U | __")uU  /"\  u U  /"\  u  |"|     
\| | u   \|  _ \/ \/ _ \/   \/ _ \/ U | | u   
 | |/__   | |_) | / ___ \   / ___ \  \| |/__  
  \____|  |____/ /_/   \_\ /_/   \_\  |_____| 
 _// \\  _|| \\_  \\    >>  \\    >>  //  \\  
(__)(__)(__) (__)(__)  (__)(__)  (__)(_")("_)
  CONSENSUS-BASED AUCTION ALGORITHM LIBRARY
            by Pierre LAGUE
```

**CBAAL - Consensus Based Auction Algorithm Library**

## Overview

CBAAL is a library developed as part of my end-of-year assignment for my first-year master's degree. It focuses on implementing consensus-based auction algorithms (CBAA) and consensus-based bundle algorithm (CBBA) primarily for dynamic load balancing problems. The algorithms implemented in this library are inspired by the publication of Choi et al., which introduced these innovative approaches to solving load balancing challenges in dynamix environments. 📚💼

## Features

- Implementation of CBAA and CBBA algorithms.
- Designed for dynamic load balancing scenarios.
- Provides a framework for simulating load balancing strategies over various network topologies.
- Well-documented codebase for easy understanding and modification. 🛠️📝

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CBAAL.git
   ```

2. Navigate to the cloned directory:
   ```
   cd CBAAL
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Import the necessary modules:
   ```python
   from cbaal import CBAA, CBBA
   ```

2. Initialize the algorithms with appropriate parameters:
   ```python
   cbaa = CBAA(...)
   cbba = CBBA(...)
   ```

3. Run the algorithms with your specific data:
   ```python
   cbaa_result = cbaa.simulation(...)
   cbba_result = cbba.simulation(...)
   ```

After a simulation a gif will be saved showing you the process of the task assignement : 
![]([my_gif/mygif.gif](https://github.com/Jakcrimson/CBAAL/blob/master/my_gif/mygif.gif))

## Documentation

Detailed documentation can be found in scripts of the repository. This includes explanations of the algorithms, and relevant remarks about the code and theory behind the algorithms. 📖🔍

## Contribution

Contributions to the project are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository. 🚀👥

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details. 📜

## Acknowledgements

We would like to express our gratitude to Choi et al [https://dspace.mit.edu/bitstream/handle/1721.1/52330/Choi_Consensus-Based-Decentralized.pdf?sequence=2] . for their pioneering work in consensus-based auction algorithms, which served as the inspiration for this project. 🙏

## Contact

For any inquiries or questions regarding the library, please contact [your email address]. 📧

---

**Disclaimer**: This library is provided as-is without any warranties. Use at your own discretion. 🚨🔒
