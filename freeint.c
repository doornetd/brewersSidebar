#include <stdio.h>
#include <stdlib.h>

void freeint(void** p);

int main()
{
	double *p;
	p = malloc(100);
	freeint(&p);
	
	if(p==NULL){
		printf("it is null");
	} else {
		printf("it is not null");
	}

	return 0;
}

void freeint(void** p){
	free(*p);
	*p = NULL;
}
