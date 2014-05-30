import matplotlib.pyplot as plt

file = "AMI.txt"

xsec = []
with open(file) as input:
    for line in input:
        if "crossSection" in line:
            xsec.append(line.split()[-1])
            
xsec_sum = 0.0
to_plot = []
less_ten = []
more_ten = []
others = []
for number in xsec:
    to_plot.append(float(number))
    if float(number) > 10.0: more_ten.append(float(number))
    if float(number) < 0.0: less_ten.append(float(number))
    if float(number) < 10.0 and float(number) > 0.0: others.append(float(number))
    xsec_sum+=float(number)
xsec_avg = xsec_sum/len(xsec)            

print "Total average: {0}".format(xsec_avg)
print ">10.0 average: {0}".format(sum(more_ten)/float(len(more_ten)))
print "<00.0 average: {0}".format(sum(less_ten)/float(len(less_ten)))
print "Other average: {0}".format(sum(others)/float(len(others)))

to_plot.sort()
more_ten.sort()
less_ten.sort()
others.sort()
print to_plot
print more_ten
print less_ten
print others
#plt.plot(to_plot)
#plt.show()
