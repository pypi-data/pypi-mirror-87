from importlib.metadata import version

__version__ = version(__name__)

NUM_COLS = 80

CPP_TEMPLATE = """\
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
#include <utility>
using namespace std;
typedef long long ll;

#define MAX_N 10000

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    /* code */
}
"""
