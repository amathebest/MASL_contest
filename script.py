# libraries import
from Dag import DAG




# constants declaration


definition = "a-b,a-c,c-b,b-d,a-e,e-d,c-f,b-f"
dag = DAG.create_dag(definition)

dag.build_adjacency_matrix()
