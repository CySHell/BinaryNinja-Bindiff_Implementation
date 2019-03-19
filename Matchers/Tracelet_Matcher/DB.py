from neo4j import GraphDatabase
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
            traced_func_id = tx.run('Merge (f:TracedFunction {filename:$filename, rawfileoffset:$rawoff})'
                                    'RETURN id(f) ',
                                    filename=traced_func.filename, rawoff=traced_func.raw_file_offset).single().value()
            # Create nodes for all tracelets
            for tracelet in traced_func.tracelets:
                tx.run('MATCH (f) WHERE id(f) = {func_id} '
                       'MERGE (tracelet:Tracelet {operations:$ops, operands:$operands, symbols:$symbols,'
                       'hash:$hash })'
                       'MERGE (f)-[:CONTAINS]->(tracelet) '
                       , func_id=traced_func_id, ops=tracelet.operations.hex, operands=tracelet.operands.hex,
                       symbols=tracelet.symbols.hex, hash=tracelet.hash)
            tx.sync()
            tx.commit()
