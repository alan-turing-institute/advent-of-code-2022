%{
int cycles = 1;
int x = 1;
int print_if(int cycles, int x, int* total) {
  if((cycles - 20) % 40 == 0){
    *total += cycles * x;
    //printf("total: %d ", *total);
  }
  //printf("cycle: %d ", cycles);
  //printf("x: %d \n", x);
  return 0;
}
int total = 0;
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

