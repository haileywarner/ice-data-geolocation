#https://stats.stackexchange.com/questions/361017/proper-way-of-estimating-the-covariance-error-ellipse-in-2d

def cov_ellipse2(points, cov, nstd):
        """
        Source: https://stackoverflow.com/a/39749274/1391441
        """
    
        vals, vecs = eigsorted(cov)
        theta = np.degrees(np.arctan2(*vecs[::-1, 0]))
    
        # Confidence level
        q = 2 * norm.cdf(nstd) - 1
        r2 = chi2.ppf(q, 2)
    
        width, height = 2 * np.sqrt(vals * r2)
    
        return width, height, theta
    
    
    if __name__ == '__main__':
        main()