#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int splitLine (char* line, char toks[3][36]) {
  int n = 0, i = 0, j = 0;
	
  for(i = 0; 1 ; i++) {
    if (line[i] == '\n') {
      line[i] = '\0';
    }
    if(line[i] != ' '){
      toks[n][j++] = line[i];
    } else{
      toks[n][j++]='\0'; // end of a tok
      n++;
      j=0;
    }
    if(line[i] == '\0') {
      break;
    }
  }  
  return n;
}

int parseCCS (char* input_file, double* VAL, int* ROW, int* PTR) {
  
  FILE* fp;
  char* line = NULL;
  char toks[3][36];
  size_t len = 0;
  ssize_t read;
  int cnt = 0;
  double val;

  int data_type = -1;
  int N = 0;
  int debug = 1;
  
  // open file
  if ((fp = fopen (input_file, "r")) == NULL) {
    printf ("Error: open file FAILED: %s\n", input_file);
    exit (1);
  }

  // read line by line: read (line length), line (text)
  while ((read = getline(&line, &len, fp)) != -1) {
    // comment line % ==> get data type and size
    if (line[0] == '%') {
      splitLine(line, toks);

      // based on data size, allocate memory
      N = atoi(toks[2]);      
      cnt = 0;
      
      if (strcmp(toks[1], "VAL") == 0) {
	data_type = 1;
	VAL = (double*) malloc(N * sizeof(double));
      } else if (strcmp(toks[1], "ROW") == 0) {
	data_type = 2;
	ROW = (int*)    malloc(N * sizeof(int));
      } else if (strcmp(toks[1], "PTR") == 0) {
	data_type = 3;
	PTR = (int*)    malloc(N * sizeof(int));
      } else {
	printf("Error: invalid input file: %s\n", input_file);
      }

      if (debug) {
	printf ("%s %s %d\n", toks[0], toks[1], N);
      }
      continue;
    }

    if (data_type == 1) {
      VAL[cnt] = atof(line);
      if (debug) {
	printf ("%s", line);
      }
    } else if (data_type == 2) {
      ROW[cnt] = atoi(line);
      if (debug) {
	printf ("%d\n", ROW[cnt]);
      }      
    } else if (data_type == 3) {
      PTR[cnt] = atoi(line);
      if (debug) {
	printf ("%d\n", PTR[cnt]);
      }
    }
    cnt++;
  }

  fclose(fp);
  return 0;
}

int main (int argc, char** argv) {

  double* VAL = NULL;               // this is VAL array
  int* ROW    = NULL;               // this is ROW array
  int* PTR    = NULL;               // this is PTR array
  
  // print usage
  if (argc < 2) {
    printf ("Usage: CCS <input data file>\n");
    return 0;
  }

  char* input_file = argv[1];
  printf ("Input Matrix Data File: %s\n", input_file);

  parseCCS (input_file, VAL, ROW, PTR);

  // now the data in VAL/ROW/PTR


  // after use, free memory
  if (VAL)
    free(VAL);
  if (ROW)
    free(ROW);
  if (PTR)
    free(PTR);
}

