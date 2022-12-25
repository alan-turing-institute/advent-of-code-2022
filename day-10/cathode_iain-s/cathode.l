%{
int cycles = 0;
int x = 1;
int total = 0;

int print_if(int cycles, int x, int* total) {
  int pixel_x = (cycles-1) % 40;

  if ((x-2 < pixel_x) && (x+2 > pixel_x)){
    printf("#");
  } else {
    printf(".");
  }

  if (pixel_x == 39){
    printf("\n");
  } else if (pixel_x == 19){
    *total += cycles * x;
  }
  return 0;
}
%}

%%

[\n] { ++cycles; print_if(cycles, x, &total); }
-?[0-9]+ { ++cycles; print_if(cycles, x, &total); x+=atoi(yytext); }
[addx,noop," "] { ; }

%%

int yywrap() {
  return 1;
}

int main () {
  yylex();
  printf("cycles: %d\n", cycles);
  printf("x: %d\n", x);
  printf("total: %d\n", total);
  return 0;
}

