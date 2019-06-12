library(ggplot2)
library(readxl)

remove(list = ls())

D3_gamma_bootstrap_results <- read_excel(
  "~/Box Sync/Projects/introgression_statistic/revision/Data/vary_Ne/D3_vary_Ne_results.xlsx")

#D3_gamma_bootstrap_results <- read_excel(
#  "C:/Users/Marcus/Box Sync/Projects/introgression_statistic/Data/D3vsABBABABA/D3_gamma_bootstrap_results.xlsx")

### Plot for D3 ###

D3_plot <- ggplot(D3_gamma_bootstrap_results, #setup plot object
                  aes(x = as.factor(gamma), y = D3))

#Add violin
D3_plot <- D3_plot + geom_violin()

#Add points
D3_plot <- D3_plot + geom_jitter(position = position_jitter(0.2))
#Remove grid background and add borders

D3_plot <- D3_plot + theme_bw(base_size = 19) + theme(panel.border = element_blank(), 
                                                      panel.grid.major = element_blank(),
                                                      panel.grid.minor = element_blank(), 
                                                      axis.line = element_line(colour = "black"))

#Add dashed line at 0

D3_plot <- D3_plot + geom_hline(aes(yintercept = 0), 
                                linetype = "dashed")

#Adjust axis labels

D3_plot <- D3_plot + labs(x = expression(paste(
  'Admixture proportion (', gamma, ')')),
  y = expression(italic('D')[3]))

### P value calculcation for individual sims ### 

get_pval <- function(estimate, stdev){ #gets pval from statistic value and stdev
  
  z <- estimate / stdev #z score
  p <- pnorm(estimate, mean = 0, sd = stdev, lower.tail = FALSE) #p value
  
  return(p)
}

D3_gamma_bootstrap_results$D3_pvals <- mapply(get_pval, #calculate D3 p-values
                                              estimate = D3_gamma_bootstrap_results$D3,
                                              stdev = D3_gamma_bootstrap_results$D3_stdev)

### Calculate rejection rates ### 

D3_0_power <- sum(subset(D3_gamma_bootstrap_results, gamma == 0)$D3_pvals < 0.05)/100*100
D3_0.01_power <- sum(subset(D3_gamma_bootstrap_results, gamma == 0.01)$D3_pvals < 0.05)/100*100
D3_0.05_power <- sum(subset(D3_gamma_bootstrap_results, gamma == 0.05)$D3_pvals < 0.05)/100*100
D3_0.1_power <- sum(subset(D3_gamma_bootstrap_results, gamma == 0.1)$D3_pvals < 0.05)/100*100

### Add rejection rates to plots ###

D3_plot <- D3_plot + annotate('text', label = '4%', x = 1, y = 0.026, size = 6)
D3_plot <- D3_plot + annotate('text', label = '6%', x = 2, y = 0.027, size = 6)
D3_plot <- D3_plot + annotate('text', label = '48%', x = 3, y = 0.043, size = 6)
D3_plot <- D3_plot + annotate('text', label = '84%', x = 4, y = 0.055, size = 6)

### Calculate expected values of D3 ### 
pt1_conc <- 1 - exp(-0.6)
pt1_ILS <- (1/3)*exp(-0.6)
pt2_conc <- 1 - exp(-1.1)
pt2_ILS <- (1/3)*exp(-1.1
)
expected_D3 <- function(gamma){
  
  dBC = (1-gamma)*0.01*2*((pt1_conc*2.2 + 2*pt1_ILS*(2.2 + (1/3)) + pt1_ILS*(1.2 + (1/3)))) + 
    gamma*0.01*2*(((1 - exp(-1.1))*(0.1 + (1 - (1.1/(exp(1.1)-1)))) + 
                     2*(1/3)*exp(-1.1)*(2.2 + (1/3)) + (1/3)*exp(-1.1)*(1.2 + (1/3))))
  
  dAC = (1-gamma)*0.01*2*((pt1_conc*2.2 + 2*pt1_ILS*(2.2 + (1/3)) + pt1_ILS*(1.2 + (1/3)))) + 
    gamma*0.01*2*(((1 - exp(-1.1))*2.2 + 
                     2*(1/3)*exp(-1.1)*(2.2 + (1/3)) + (1/3)*exp(-1.1)*(1.2 + (1/3))))
  
  return((dAC-dBC)/(dBC+dAC))
}

D3_0_exp <- expected_D3(0)
D3_0.01_exp <- expected_D3(0.01)
D3_0.05_exp <- expected_D3(0.05)
D3_0.1_exp <- expected_D3(0.1)

### Add expected values to D3 plot 

D3_plot <- D3_plot + geom_point(aes(x = 1, y = 0), shape = 23, fill = 'red', color = 'red', size = 4)
D3_plot <- D3_plot + geom_point(aes(x = 2, y = 0.0025), shape = 23, fill = 'red', color = 'red', size = 4)
D3_plot <- D3_plot + geom_point(aes(x = 3, y = 0.0126), shape = 23, fill = 'red', color = 'red', size = 4)
D3_plot <- D3_plot + geom_point(aes(x = 4, y = 0.0256), shape = 23, fill = 'red', color = 'red', size = 4)
D3_plot
