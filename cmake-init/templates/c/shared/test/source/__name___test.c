#include <string.h>
#include "%(name)s/%(name)s.h"

int main()
{
  return strcmp("%(name)s", exported_function()) == 0 ? 0 : 1;
}