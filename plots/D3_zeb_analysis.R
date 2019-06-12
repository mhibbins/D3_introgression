D3_bootstrap_values <- read.csv( #read dataset
  "~/Box Sync/Projects/introgression_statistic/revision/Data/banana_D3_zeb_bootstrap_values.txt", sep="")

### Plot histogram ###
library(ggplot2)

D3_hist <- ggplot(D3_bootstrap_values, aes(x = D3)) #setup plot object

D3_hist <- D3_hist + geom_histogram() #add histogram

D3_hist <- D3_hist + xlim(-0.02, 0.03) #adjust range of x axis

#Clean up plot
D3_hist <- D3_hist + theme_bw() + theme(panel.border = element_blank(), panel.grid.major = element_blank(),
                                        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
D3_hist

#Estimate significance 

D3_estimate <- mean(D3_bootstrap_values$D3)
D3_stdev <- sd(D3_bootstrap_values$D3)
z <- D3_estimate/D3_stdev
pval <- pnorm(D3_estimate, mean = 0, sd = D3_stdev, lower.tail = FALSE)
