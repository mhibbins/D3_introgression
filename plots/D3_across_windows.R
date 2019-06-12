library(ggplot2)
remove(list=ls())
dAC_excess_windows <- read.delim("~/Box Sync/Projects/introgression_statistic/revision/Data/dAC_excess_windows.txt")

window_plot <- ggplot(dAC_excess_windows, aes(x = as.factor(gamma), y = prop))
window_plot <- window_plot + stat_summary(fun.y = mean, geom = 'point') + 
  stat_summary(fun.data = mean_sdl, geom = 'errorbar', width = 0.2)

window_plot <- window_plot + theme_bw(base_size = 14) + theme(panel.border = element_blank(), panel.grid.major = element_blank(),
                   panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
window_plot <- window_plot + labs(x = expression(paste('Admixture proportion (', gamma, ')')),
                                  y = expression(paste('Proportion of 5kb windows where ', italic('D')[3], ' < 0')))

window_plot

