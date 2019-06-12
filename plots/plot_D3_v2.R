library(ggplot2)

remove(list=ls())

D3_v2_results <- read_excel("~/Box Sync/Projects/introgression_statistic/revision/Data/D3_v2/D3_v2_results.xlsx")

D3_v2_plot <- ggplot(D3_v2_results, #setup plot object
                  aes(x = as.factor(gamma), y = D3_v2))

#Add violin
D3_v2_plot <- D3_v2_plot + geom_violin()

#Add points
D3_v2_plot <- D3_v2_plot + geom_jitter(position = position_jitter(0.2))
#Remove grid background and add borders

D3_v2_plot <- D3_v2_plot + theme_bw(base_size = 19) + theme(panel.border = element_blank(), 
                                                      panel.grid.major = element_blank(),
                                                      panel.grid.minor = element_blank(), 
                                                      axis.line = element_line(colour = "black"))

#Add dashed line at 0

D3_v2_plot <- D3_v2_plot + geom_hline(aes(yintercept = 0), 
                                linetype = "dashed")

#Adjust axis labels

D3_v2_plot <- D3_v2_plot + labs(x = expression(paste(
  'Admixture proportion (', gamma, ')')),
  y = expression(italic('D')[3]))

### P value calculcation for individual sims ### 

get_pval <- function(estimate, stdev){ #gets pval from statistic value and stdev
  
  z <- estimate / stdev #z score
  p <- pnorm(estimate, mean = 0, sd = stdev, lower.tail = FALSE) #p value
  
  return(p)
}

D3_v2_results$D3_v2_pvals <- mapply(get_pval, #calculate D3_v2 p-values
                                              estimate = D3_v2_results$D3_v2,
                                              stdev = D3_v2_results$D3_v2_stdev)

### Calculate rejection rates ### 

D3_v2_0_power <- sum(subset(D3_v2_results, gamma == 0)$D3_v2_pvals < 0.05)/100*100
D3_v2_0.01_power <- sum(subset(D3_v2_results, gamma == 0.01)$D3_v2_pvals < 0.05)/100*100
D3_v2_0.05_power <- sum(subset(D3_v2_results, gamma == 0.05)$D3_v2_pvals < 0.05)/100*100
D3_v2_0.1_power <- sum(subset(D3_v2_results, gamma == 0.1)$D3_v2_pvals < 0.05)/100*100

### Add rejection rates to plots ###

D3_v2_plot <- D3_v2_plot + annotate('text', label = '7%', x = 1, y = 0.055, size = 6)
D3_v2_plot <- D3_v2_plot + annotate('text', label = '11%', x = 2, y = 0.07, size = 6)
D3_v2_plot <- D3_v2_plot + annotate('text', label = '52%', x = 3, y = 0.09, size = 6)
D3_v2_plot <- D3_v2_plot + annotate('text', label = '93%', x = 4, y = 0.11, size = 6)

D3_v2_plot
