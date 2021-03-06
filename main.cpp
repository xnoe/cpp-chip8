#include <iostream>
#include <fstream>
#include <stack>

int main(int argc, char** argv) {
  if (argc < 2) {
    std::cout << "CHIP-8-esque... thing?\n";
    std::cout << "By bybb\n";
    std::cout << "Usage:" << argv[1] << " <bytecode file>.\n";
    return 0;
  }

  unsigned char ROM[0x1000] = {0};
  unsigned char* Vx = &ROM[0xEA0];
  unsigned short* I = (unsigned short*)ROM+0xEB0;
  unsigned short* PC = (unsigned short*)ROM+0xEB2;
  *PC = 0x200; // Correctly set PC to 0x200

  unsigned short INST;

  // Read in bytecode file
  std::ifstream romFile (argv[1]);

  int count(0);
  while (!romFile.eof() && count<0x1000)
    ROM[count++] = romFile.get();
  ROM[--count] = 0;
  romFile.close();

  std::stack<unsigned short> stack;

  bool running = true;
  while (running && *PC<0x1000) {
    INST = (ROM[*PC]<<8)|(ROM[*PC+1]);
    unsigned short NNN = INST&4095;
    unsigned char NN = (char)INST;
    unsigned char N = (char)INST&15;
    unsigned char X = ((char)(INST>>4)&240)>>4;
    unsigned char Y = (char)(INST>>4)&15;
    unsigned char OPCODE = ((char)(INST>>8)&240)>>4;
    switch (OPCODE) {
      case (0): {
        if (!NNN) running = false;
        if (NNN==0x0E0) break;
        if (NNN==0x0EE) {
          *PC = stack.top();stack.pop();
        }
      }
      case (1):
        *PC = NNN-2;
        break;
      case (2):
        stack.push(*PC);
        *PC = NNN-2;
        break;
      case (3):
        if (Vx[X]==NN)
          *PC+=2;
        break;
      case (4):
        if (Vx[X]!=NN)
          *PC+=2;
        break;
      case (5):
        if (Vx[X]==Vx[Y]) *PC+=2;
        break;
      case (6):
        Vx[X] = NN;
        break;
      case (7):
        Vx[X] += NN;
        break;
      case (8):
        if (!N) Vx[X] = Vx[Y];
        else if (N==1) Vx[X] = Vx[X]|Vx[Y];
        else if (N==2) Vx[X] = Vx[X]&Vx[Y];
        else if (N==3) Vx[X] = Vx[X]^Vx[Y];
        else if (N==4) {
          unsigned short tmp = Vx[X];
          Vx[X] += Vx[Y];
          Vx[15] = (unsigned short)tmp>Vx[X];
        } else if (N==5) {
          unsigned short tmp = Vx[X];
          Vx[X] -= Vx[Y];
          Vx[15] = (unsigned short)tmp<Vx[X];
        } else if (N==6) {
          Vx[15] = Vx[X]&1;
          *(Vx+X) >>= 1;
        } else if (N==7) {
          unsigned short tmp = Vx[X];
          Vx[X] = Vx[Y]-Vx[X];
          Vx[15] = (unsigned short)tmp<Vx[X];
        } else if (N==14) {
          Vx[15] = Vx[X]&128;
          *(Vx+X) <<= 1;
        }
        break;
      case (9):
        if (Vx[X]!=Vx[Y]) *PC+=2;
        break;
      case (10):
        *I = NNN;
        break;
      case (11):
        *PC = *Vx+NNN;
        break;
      case (12):
        // Not Implemented;
        break;
      case (13):
        // This would usually be DXYN for draw
        // But here it is used to dump memory location at I
        std::cout << (char)ROM[*I];
        break;
      case (14):
        // Not Implemented;
      case (15):
        // Partially Implemented;
        if (NN == 0x1E) *I += Vx[X];
        else if (NN == 0x55) {
          unsigned short tmp(*I);
          for (int i(0);i<=X;i++)
            ROM[tmp++]=Vx[i];
        } else if (NN == 0x65) {
          unsigned short tmp(*I);
          for (int i(0);i<=X;i++)
            Vx[i]=ROM[tmp++];
        }
    }
    *PC+=2;
  }
  std::cout << std::flush;
  return 0;
}
