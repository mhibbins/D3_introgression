library(ggplot2)
library(readxl)

remove(list=ls())

D3_bigtheta_results <- read_excel("~/Box Sync/Projects/introgression_statistic/revision/Data/big_theta//D3_bigtheta_results.xlsx")

D3_bigtheta_plot <- ggplot(D3_bigtheta_results, #setup plot object
                     aes(x = as.factor(gamma), y = D3))

#Add violin
D3_bigtheta_plot <- D3_bigtheta_plot + geom_violin()

#Add points
D3_bigtheta_plot <- D3_bigtheta_plot + geom_jitter(position = position_jitter(0.2))
#Remove grid background and add borders

D3_bigtheta_plot <- D3_bigtheta_plot + theme_bw(base_size = 19) + theme(panel.border = element_blank(), 
                                                            panel.grid.major = element_blank(),
                                                            panel.grid.minor = element_blank(), 
                                                            axis.line = element_line(colour = "black"))

#Add dashed line at 0

D3_bigtheta_plot <- D3_bigtheta_plot + geom_hline(aes(yintercept = 0), 
                                      linetype = "dashed")

#Adjust axis labels

D3_bigtheta_plot <- D3_bigtheta_plot + labs(x = expression(paste(
  'Admixture proportion (', gamma, ')')),
  y = expression(italic('D')[3]))

### P value calculcation for individual sims ### 

get_pval <- function(estimate, stdev){ #gets pval from statistic value and stdev
  
  z <- estimate / stdev #z score
  p <- pnorm(estimate, mean = 0, sd = stdev, lower.tail = FALSE) #p value
  
  return(p)
}

D3_bigtheta_results$D3_bigtheta_pvals <- mapply(get_pval, #calculate D3_bigtheta p-values
                                    estimate = D3_bigtheta_results$D3,
                                    stdev = D3_bigtheta_results$D3_stdev)

### Calculate rejection rates ### 

D3_bigtheta_0_power <- sum(subset(D3_bigtheta_results, gamma == 0)$D3_bigtheta_pvals < 0.05)/100*100
D3_bigtheta_0.01_power <- sum(subset(D3_bigtheta_results, gamma == 0.01)$D3_bigtheta_pvals < 0.05)/100*100
D3_bigtheta_0.05_power <- sum(subset(D3_bigtheta_results, gamma == 0.05)$D3_bigtheta_pvals < 0.05)/100*100
D3_bigtheta_0.1_power <- sum(subset(D3_bigtheta_results, gamma == 0.1)$D3_bigtheta_pvals < 0.05)/100*100

### Add rejection rates to plots ###

D3_bigtheta_plot <- D3_bigtheta_plot + annotate('text', label = '9%', x = 1, y = 0.003, size = 6)
D3_bigtheta_plot <- D3_bigtheta_plot + annotate('text', label = '47%', x = 2, y = 0.004, size = 6)
D3_bigtheta_plot <- D3_bigtheta_plot + annotate('text', label = '100%', x = 3, y = 0.01, size = 6)
D3_bigtheta_plot <- D3_bigtheta_plot + annotate('text', label = '100%', x = 4, y = 0.012, size = 6)

D3_bigtheta_plot
