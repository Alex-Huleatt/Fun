# require 'statistics2'

# def ci_lower_bound(pos, n, confidence)
#     if n == 0
#         return 0
#     end
#     z = Statistics2.pnormaldist(1-(1-confidence)/2)
#     phat = 1.0*pos/n
#     (phat + z*z/(2*n) - z * Math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
# end

from math import sqrt

def confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.0 #1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))
