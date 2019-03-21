from neo4j import GraphDatabase, exceptions
from . import Data_Types_and_Constants

_uri = "bolt://localhost:7687"
_user = "neo4j"
_password = "user"


def init_db(uri=_uri, user=_user, password=_password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


def delete_graph(driver):
    pass
    # TODO: implement this function


def populate_traced_function(traced_func, driver):
    """
    Creates a graph to represent the traced function, containing all tracelets and relevant information
    :param traced_func: the function to parse
    :param driver: neo4j python driver object (created by init_db())
    :return: success: (BOOLEAN)
    """
    with driver.session() as session:
        with session.begin_transaction() as tx:
            # create function node
            traced_func_id = tx.run('Merge (f:TracedFunction {filename:$filename, rawfileoffset:$rawoff,'
                                    'arguments:$arg_bitarray})'
                                    'RETURN id(f) ',
                                    filename=traced_func.filename, rawoff=traced_func.raw_file_offset,
                                    arg_bitarray=traced_func.arguments.hex).single().value()
            # Create nodes for all tracelets
            for tracelet in traced_func.tracelets:
                tracelet_node = tx.run('MATCH (f) WHERE id(f) = {func_id} '
                                       'MERGE (tracelet:Tracelet {operations:$ops, operands:$operands, '
                                       'symbols:$symbols, hash:$hash })'
                                       'MERGE (f)-[:CONTAINS]->(tracelet)'
                                       'RETURN id(tracelet) ',
                                       func_id=traced_func_id, ops=tracelet.operations.hex,
                                       operands=tracelet.operands.hex,
                                       symbols=tracelet.symbols.hex, hash=tracelet.hash)

                if tracelet_node.peek():
                    tracelet_id = tracelet_node.peek()[0]
                    current_instruction_id = tracelet_id
                else:
                    continue

                for i in range(int(len(tracelet.operations.hex) / 2)):
                    current_operation = tracelet.operations.hex[i * 2: (i * 2) + 2]
                    retry = True
                    while retry:
                        try:
                            next_instruction_id = tx.run('MATCH (node) WHERE id(node) = {current_instruction_id} '
                                                         'MERGE (ni:NormalizedInstr {current_operation: $current_op}) '
                                                         'MERGE (node)-[:NextOperation {orig: $orig}]->(ni) '
                                                         'RETURN id(ni) ',
                                                         current_instruction_id=current_instruction_id,
                                                         current_op=current_operation,
                                                         orig=tracelet_id).single().value()
                            current_instruction_id = next_instruction_id
                            retry = False
                        except exceptions.TransientError:
                            continue

        if not tx.closed():
            tx.sync()
            tx.commit()
