#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>

#define ROWS 6
#define COLS 7

char board[ROWS][COLS];

bool check_win(char player) {

    for (int r = 0; r < ROWS; r++) {
        for (int c = 0; c <= COLS - 4; c++) {
            if (board[r][c] == player && board[r][c+1] == player &&
                board[r][c+2] == player && board[r][c+3] == player) {
                return true;
                }
        }
    }

    // Check vertical
    for (int r = 0; r <= ROWS - 4; r++) {
        for (int c = 0; c < COLS; c++) {
            if (board[r][c] == player && board[r+1][c] == player &&
                board[r+2][c] == player && board[r+3][c] == player) {
                return true;
                }
        }
    }


    for (int r = 0; r <= ROWS - 4; r++) {
        for (int c = 0; c <= COLS - 4; c++) {
            if (board[r][c] == player && board[r+1][c+1] == player &&
                board[r+2][c+2] == player && board[r+3][c+3] == player) {
                return true;
                }
        }
    }


    for (int r = 3; r < ROWS; r++) {
        for (int c = 0; c <= COLS - 4; c++) {
            if (board[r][c] == player && board[r-1][c+1] == player &&
                board[r-2][c+2] == player && board[r-3][c+3] == player) {
                return true;
                }
        }
    }

    return false;
}


int make_move(int col, char player) {
    for (int r = ROWS-1; r >= 0; r--) {
        if (board[r][col] == '.') {
            board[r][col] = player;
            return r;
        }
    }
    return -1;
}


void undo_move(int row, int col) {
    board[row][col] = '.';
}
