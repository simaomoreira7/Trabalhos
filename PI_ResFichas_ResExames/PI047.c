#include <stdio.h>
#include <string.h>

#define FALSE 0
#define TRUE  1
#define SKIP_EOL {while (getchar()!='\n') ;}

int pimpampum(int npersons, int pos, int nwords, int vencedor[100]) {


    while ((npersons > 1)) {
        pos = ((nwords) % npersons);

        if (vencedor[pos] == 0) {
            vencedor[pos] = 1;
        } else if (vencedor[pos] == 1) {
            while (vencedor[pos] != 0) {
                pos++;
            }
            vencedor[pos] = 1;
        }
        npersons--;
    }

    for (int i = 0; i < npersons; i++) {
        if (vencedor[i]==0) {
            return i;
        }
    }
}

int readAndCountWords() {
    char ch= getchar();
    int nwords = 0;
    while (ch!='\n') {
        while ((ch=getchar())!=' ' && ch!='\n') ;
        nwords++;
        while (ch!='\n' && (ch=getchar()==' '));
    }
    return nwords;
}

int main() {
    int ncases, nwords, npersons, pos = 0;
    int i, j;

    scanf("%d",&ncases);
    SKIP_EOL; // skip end_of_line

    for (int c=0; c<ncases; c++) {

        nwords = 0;
        nwords += readAndCountWords(); //le e conta as palavras
        printf("%d\n", nwords);


        scanf("%d",&npersons);
        printf("%d\n", npersons); // numero de pessoas

        char nomes[npersons][100];

        for (int d=0; d<npersons; d++) {
            scanf("%s",&nomes[d]); // le o nome da pessoa
            printf("%s\n", nomes[d]);

            getchar();

        }

        int vencedor[100] = {0};


        if (nwords > 9) {
            pos+=pimpampum(npersons, pos, nwords, vencedor);
            printf("%s\n", nomes[pos]);

        }

    }

    return 0;
}
