library(SIN)

# data import
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read.table("esami_matem.txt", header = TRUE, sep = " ")
data$Anno <- NULL

# sinful procedure that gives the p-values relative to the corresponding test on the edge
pvals <- sinUG(var(data), n = nrow(data), holm=T)
pvals # this shows very high p-values on the lower correlations and low p-values on high correlations

# plotting the p-values of the tests for each edge
alpha_value = 0.20
plotUGpvalues(pvals, legend = F) # displays each edge with the corresponding p-value 
abline(h = alpha_value, col = "blue")

# adjacency matrix of the obtained graph
adj_mat <- getgraph(pvals, alpha = alpha_value, type="UG")

# plotting the obtained graph with the chosen value of alpha
drawGraph(getgraph(pvals, alpha = alpha_value, type="UG"))

# obtaining the graph definition that will be used to create the graph with my package
names <- rownames(adj_mat)
definition <- ""

for (i in 1:nrow(adj_mat)) {
    for (j in 1:nrow(adj_mat)) {
        if (adj_mat[i,j] == 1) {
            new_edge <- paste(names[i], names[j], sep = "-")
            definition <- paste(definition, new_edge, sep = ",")
        }
    }
}
