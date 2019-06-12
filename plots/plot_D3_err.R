library(ggplot2)
library(readxl)

remove(list = ls())

D3_err_bootstrap_results <- read_excel(
  "~/Box Sync/Projects/introgression_statistic/revision/Data/sequence_bias/D3_errors_results.xlsx")

#D3_gamma_bootstrap_results <- read_excel(
#  "C:/Users/Marcus/Box Sync/Projects/introgression_statistic/Data/D3vsABBABABA/D3_gamma_bootstrap_results.xlsx")

### Plot for D3 ###

D3_plot <- ggplot(D3_err_bootstrap_results, #setup plot object
                  aes(x = as.factor(rate), y = D3))

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

D3_plot <- D3_plot + labs(x = 'Per-base error rate',
  y = expression(italic('D')[3]))

### P value calculcation for individual sims ### 

get_pval <- function(estimate, stdev){ #gets pval from statistic value and stdev
  
  z <- estimate / stdev #z score
  p <- pnorm(estimate, mean = 0, sd = stdev, lower.tail = FALSE) #p value
  
  return(p)
}

D3_err_bootstrap_results$D3_pvals <- mapply(get_pval, #calculate D3 p-values
                                              estimate = D3_err_bootstrap_results$D3,
                                              stdev = D3_err_bootstrap_results$D3_stdev)

### Calculate rejection rates ### 

D3_0.0001_power <- sum(subset(D3_err_bootstrap_results, rate == 1e-4)$D3_pvals < 0.05)/100*100
D3_0.001_power <- sum(subset(D3_err_bootstrap_results, rate == 1e-3)$D3_pvals < 0.05)/100*100
D3_0.01_power <- sum(subset(D3_err_bootstrap_results, rate == 1e-2)$D3_pvals < 0.05)/100*100

### Add rejection rates to plots ###

D3_plot <- D3_plot + annotate('text', label = '10%', x = 1, y = 0.03, size = 6)
D3_plot <- D3_plot + annotate('text', label = '92%', x = 2, y = 0.06, size = 6)
D3_plot <- D3_plot + annotate('text', label = '100%', x = 3, y = 0.21, size = 6)

D3_plot


