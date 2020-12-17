library(ggm)
library(SIN)

# Data import
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read.table("esami_matem.txt", header = TRUE, sep = " ")
data$Anno <- NULL

# Variable correlation overview
cor(data)

# SINful procedure that gives the p-values relative to the corresponding test on each edge
pvals <- sinUG(var(data), n = nrow(data), holm = T)

# Plotting the p-values of the tests for each edge
alpha_value = 0.30
plotUGpvalues(pvals, legend = F) # displays each edge with the corresponding p-value 
abline(h = alpha_value, col = "blue")

# Adjacency matrix of the obtained graph
adj_mat <- getgraph(pvals, alpha = alpha_value, type = "UG")

# Plotting the obtained graph with the chosen value of alpha
drawGraph(getgraph(pvals, alpha = alpha_value, type = "UG"))

# Analysis:
# We can assume that the first course (like Analysis 1) and the second one (like Analysis 2) are linked by
# an asymmetrical relationship, from the first to the second. For this reason we remove the edge pointing
# from the second to the first:
adj_mat["Analisi2", "Analisi1"] = 0

# The same approach is applied to the other courses:
adj_mat["Fisica2", "Fisica1"] = 0
adj_mat["Geometria2", "Geometria1"] = 0

# For the rest, in order to build a directed graph, we assume an ordering of the courses. This means that
# we decide which direction has a specific edge between two variables:
adj_mat["Geometria2", "Analisi2"] = 0

# For example, we can also assume that it's possible that Algebra gives proficiency on the exam Fisica1.
# For this reason we can direct the edge between Algebra and Fisica1 to be from Algebra and Fisica1, deleting
# the other direction. We do the same also for Geometria1:
adj_mat["Fisica1", "Algebra"] = 0
adj_mat["Geometria1", "Algebra"] = 0

# Following the same idea, we direct some more edges with an arbitrary logical order:
adj_mat["Geometria2", "Analisi2"] = 0
adj_mat["MecRaz", "Geometria2"] = 0
adj_mat["MecRaz", "Fisica1"] = 0
adj_mat["Geometria1", "Analisi1"] = 0
adj_mat["Algebra", "Analisi1"] = 0

# Obtaining the graph definition that will be used to create the graph with my package
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
definition
