library(ggplot2)
library(readxl)
remove(list=ls())

D3_tm_results <- read_excel("~/Box Sync/Projects/introgression_statistic/revision/Data/tm_sims/D3_tm_results.xlsx")

D3_tm_plot <- ggplot(D3_tm_results, #setup plot object
                     aes(x = as.factor(tm), y = D3))

#Add violin
D3_tm_plot <- D3_tm_plot + geom_violin()

#Add points
D3_tm_plot <- D3_tm_plot + geom_jitter(position = position_jitter(0.2))
#Remove grid background and add borders

D3_tm_plot <- D3_tm_plot + theme_bw(base_size = 19) + theme(panel.border = element_blank(), 
                                                            panel.grid.major = element_blank(),
                                                            panel.grid.minor = element_blank(), 
                                                            axis.line = element_line(colour = "black"))

#Add dashed line at 0

D3_tm_plot <- D3_tm_plot + geom_hline(aes(yintercept = 0), 
                                      linetype = "dashed")

#Adjust axis labels

D3_tm_plot <- D3_tm_plot + labs(x = expression(italic('t')[m]),
                                y = expression(italic('D')[3]))

### P value calculcation for individual sims ### 

get_pval <- function(estimate, stdev){ #gets pval from statistic value and stdev
  
  z <- estimate / stdev #z score
  p <- pnorm(estimate, mean = 0, sd = stdev, lower.tail = FALSE) #p value
  
  return(p)
}

D3_tm_results$D3_tm_pvals <- mapply(get_pval, #calculate D3_tm p-values
                                    estimate = D3_tm_results$D3,
                                    stdev = D3_tm_results$D3_stdev)

### Calculate rejection rates ### 

D3_tm_0.001_power <- sum(subset(D3_tm_results, tm == 0.001)$D3_tm_pvals < 0.05)/100*100
D3_tm_0.05_power <- sum(subset(D3_tm_results, tm == 0.05)$D3_tm_pvals < 0.05)/100*100
D3_tm_0.15_power <- sum(subset(D3_tm_results, tm == 0.15)$D3_tm_pvals < 0.05)/100*100
D3_tm_0.25_power <- sum(subset(D3_tm_results, tm == 0.25)$D3_tm_pvals < 0.05)/100*100

### Add rejection rates to plots ###

D3_tm_plot <- D3_tm_plot + annotate('text', label = '61%', x = 1, y = 0.035, size = 6)
D3_tm_plot <- D3_tm_plot + annotate('text', label = '63%', x = 2, y = 0.035, size = 6)
D3_tm_plot <- D3_tm_plot + annotate('text', label = '45%', x = 3, y = 0.035, size = 6)
D3_tm_plot <- D3_tm_plot + annotate('text', label = '25%', x = 4, y = 0.035, size = 6)

D3_tm_plot
