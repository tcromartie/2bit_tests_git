int rescale(float *datav, int ndata, int nbits, float *offset, float *scale)
{

    float *datacopy;
    float median, s1lo, s1hi, qlow, qhigh;

    datacopy = (float *) malloc(ndata * sizeof(float));
    if (!datacopy) {
        /* malloc apparently failed */
        printf("Error! malloc failed?\n");
        return (-1);
    }

    memcpy(datacopy, datav, ndata * sizeof(float));
    qsort(datacopy, ndata, sizeof(datav[0]), floatcmp);

    /* Now calculate median and percentiles */
    median = datacopy[(int) (0.5 * ndata)];     // Ignore odd-even issue
    s1lo = datacopy[(int) (0.1587 * ndata)];    // since we're approximating
    s1hi = datacopy[(int) (0.8413 * ndata)];    // percentiles anyway.

    qlow = median - LSIGMA * (median - s1lo);
    qlow = (qlow < datacopy[0]) ? datacopy[0] : qlow;

    qhigh = median + USIGMA * (s1hi - median);
    qhigh = (qhigh > datacopy[ndata - 1]) ? datacopy[ndata - 1] : qhigh;

//#if(VERBOSE)
    fprintf(stderr, "# Median = %.1f, 1 sigma = %.1f  %.1f, Clip at %.1f  %.1f\n",
            median, s1lo, s1hi, qlow, qhigh);
//#endif

    // X(qlow..qhigh) -> Y(0..15);   for 4-bit
    // X = scale*Y + offset; 
    // Y = (X-offset)/scale = (X-qlow)/(qhigh-qlow) * 16.0.

    if (nbits == 4)
        *scale = (qhigh - qlow) / 16.0;
    else if (nbits == 2)
        *scale = (qhigh - qlow) / 4.0;
    else                        // nbits = 8
        *scale = (qhigh - qlow) / 256.0;
    *offset = qlow;

    free(datacopy);
    return 0;
}

