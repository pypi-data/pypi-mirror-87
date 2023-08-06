import consloadingbar, time

clb = consloadingbar.Bar(phases=['|', '-'])

clb.progressCircle(time_=2)
