library(ggplot2)
library(readxl)
remove(list=ls())

D3_t1_results <- read_excel("~/Box Sync/Projects/introgression_statistic/revision/Data/t1_sims/D3_t1_results.xlsx")

D3_t1_plot <- ggplot(D3_t1_results, #setup plot object
                     aes(x = as.factor(t1), y = D3))

#Add violin
D3_t1_plot <- D3_t1_plot + geom_violin()

#Add points
D3_t1_plot <- D3_t1_plot + geom_jitter(position = position_jitter(0.2))
#Remove grid background and add borders

D3_t1_plot <- D3_t1_plot + theme_bw(base_size = 19) + theme(panel.border = element_blank(), 
                                                            panel.grid.major = element_blank(),
                                                            panel.grid.minor = element_blank(), 
                                                            axis.line = element_line(colour = "black"))

#Add dashed line at 0

D3_t1_plot <- D3_t1_plot + geom_hline(aes(yintercept = 0), 
                                      linetype = "dashed")

#Adjust axis labels

D3_t1_plot <- D3_t1_plot + labs(x = expression(italic('t')[1]),
  y = expression(italic('D')[3]))

### P value calculcation for individual sims ### 

get_pval <- function(estimate, stdev){ #gets pval from statistic value and stdev
  
  z <- estimate / stdev #z score
  p <- pnorm(estimate, mean = 0, sd = stdev, lower.tail = FALSE) #p value
  
  return(p)
}

D3_t1_results$D3_t1_pvals <- mapply(get_pval, #calculate D3_t1 p-values
                                    estimate = D3_t1_results$D3,
                                    stdev = D3_t1_results$D3_stdev)

### Calculate rejection rates ### 

D3_t1_0.01_power <- sum(subset(D3_t1_results, t1 == 0.01)$D3_t1_pvals < 0.05)/100*100
D3_t1_0.1_power <- sum(subset(D3_t1_results, t1 == 0.1)$D3_t1_pvals < 0.05)/100*100
D3_t1_0.2_power <- sum(subset(D3_t1_results, t1 == 0.2)$D3_t1_pvals < 0.05)/100*100
D3_t1_0.3_power <- sum(subset(D3_t1_results, t1 == 0.3)$D3_t1_pvals < 0.05)/100*100

### Add rejection rates to plots ###

D3_t1_plot <- D3_t1_plot + annotate('text', label = '56%', x = 1, y = 0.035, size = 6)
D3_t1_plot <- D3_t1_plot + annotate('text', label = '68%', x = 2, y = 0.035, size = 6)
D3_t1_plot <- D3_t1_plot + annotate('text', label = '57%', x = 3, y = 0.035, size = 6)
D3_t1_plot <- D3_t1_plot + annotate('text', label = '57%', x = 4, y = 0.035, size = 6)

D3_t1_plot
