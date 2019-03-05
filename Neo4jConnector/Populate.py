"""
This module populates the neo4j with values given to it by the Factory objects
"""

from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "user"


class BindjaGraph:
    """
    Neo4j graph describing the MLIL form of the binary
    """

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def delete_graph(self):
        with self.driver.session() as session:
            ##########################################
            session.begin_transaction().run()

    def populate_function(self, mlil_function):
        """
        Creates a graph to represent the function, containing all basic blocks and instructions
        :param mlil_function: (MLIL_FUNCTION) the function to parse
        :return: sucess: (BOOLEAN)
        """
        func_name = mlil_function.source_function.name

        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                # MLIL Function name
                tx.run("CREATE (func:Function {name:$name}) "
                       , name=func_name)
                # Create nodes for all basic blocks
                for basicblock in mlil_function:
                    print(tx.run('MATCH (f) WHERE f.name = {func_name} '
                           'CREATE (bb:BasicBlock {index:$index}) '
                           'CREATE (f)-[:CONTAINS]->(bb) '
                           , func_name=func_name, index=basicblock.index))
                    for instruction in basicblock:
                        tx.run('MATCH (bb) WHERE bb.index = {index} '
                               'CREATE (instr:Instruction {instr_index:$instr_index, instruction:$instr_tokens}) '
                               'CREATE (bb)-[:CONTAINS]->(instr) '
                               , instr_index=instruction.instr_index, index=basicblock.index,
                               instr_tokens=str(instruction.tokens))



bindja_driver = BindjaGraph(uri, user, password)

for f in bv.functions:
    bindja_driver.populate_function(f.mlil)
