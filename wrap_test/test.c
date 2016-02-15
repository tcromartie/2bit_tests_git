void test(double* pin, double* pout, int n) {
    int i;		
	for (i=0; i<n; ++i) {
		pout[i] = pin[i]*2;
	}
}
