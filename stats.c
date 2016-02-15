/* STATS routine to calculate statistics of a data set; taken from S Ransom's misc_utils in PRESTO*/
/* Feb 15 2016 */

#include <ctype.h>
#include "misc_utils.h"
#include "slamac.h"
#include <math.h>

void stats(float *x, int n, double *mean, double *var, double *skew, double *kurt)
/* For a floating point vector, *x, of length n, this routine  */
/* returns the mean, variance, skewness, and kurtosis of *x.   */
{
    long i;
    double an = 0.0, an1 = 0.0, dx, t1, t2, stdevmle;

    /*  Modified (29 June 98) C version of the following:        */
    /*  ALGORITHM AS 52  APPL. STATIST. (1972) VOL.21, P.226     */
    /*  Returned values were checked with Mathematica 3.01       */

    if (n < 1) {
        printf("\vVector length must be > 0 in stats().  Exiting\n");
        exit(1);
    } else {
        *mean = (double) x[0];
        *var = 0.0;
        *skew = 0.0;
        *kurt = 0.0;
    }

    for (i = 1; i < n; i++) {
        an = (double) (i + 1);
        an1 = (double) (i);
        dx = ((double) x[i] - *mean) / an;
        t1 = an1 * dx * dx;
        t2 = an * t1;
        *kurt -=
            dx * (4.0 * *skew - dx * (6.0 * *var + t1 * (1.0 + an1 * an1 * an1)));
        *skew -= dx * (3.0 * *var - t2 * (an - 2.0));
        *var += t2;
        *mean += dx;
    }

    if (n > 1) {
        stdevmle = sqrt(*var / an);
        t1 = stdevmle * stdevmle * stdevmle;
        *skew /= t1 * an;
        *kurt = *kurt / (t1 * stdevmle * an) - 3.0;
        *var /= an1;
    }

    return;
}
