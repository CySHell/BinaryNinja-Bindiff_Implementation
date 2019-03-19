"""
This module populates the neo4j with a complete binary view.
Later the DB is used to build further relationships between entities by using various normalization and
optimization methods (contained in the Matchers package)
"""

from neo4j import GraphDatabase
import xxhash

_uri = "bolt://localhost:7687"
_user = "neo4j"
_password = "user"


def init_db(uri=_uri, user=_user, password=_password):
    bolt_driver = GraphDatabase.driver(uri, auth=(user, password))
    return bolt_driver


def delete_graph(driver):
    pass
    # TODO: implement this function


def populate_binaryview(bv, driver):
    """
    Creates a graph to represent the binary view, containing all functions and relevant information.
    Everything is based off of MLIL , NOT ASSEMBLY.
    :param bv: the Binary Ninja bv to parse
    :param driver: neo4j python driver object (created by init_db())
    :return: success: (BOOLEAN)
    """
    with driver.session() as session:
        with session.begin_transaction() as tx:
            # create file object
            br = BinaryReader(bv)

            # calculate file hash
            # TODO: use external hash generators
            file_hash = xxhash.xxh32()
            # for some reason a BinaryReader won't read more then 1000 or so bytes
            temp_hash = br.read(1000)
            while temp_hash:
                file_hash.update(temp_hash)
                temp_hash = br.read(1000)

            file_id = tx.run("MERGE (file:File {name:$name, hash:$hash}) "
                             "RETURN id(file)",
                             name=bv.file.filename, hash=file_hash.intdigest()).single().value()
            # Create nodes for all functions, connect them with the file entity
            for func in bv:
                func_hash = xxhash.xxh32()
                func_id = tx.run('MATCH (file) WHERE id(file) = {file_id} '
                                 'MERGE (func:Function {hash:$func_hash })'
                                 'MERGE (file)-[:CONTAINS {orig_id:$file_id }]->(func)'
                                 'RETURN id(func) ',
                                 file_id=file_id, func_hash=0
                                 ).single().value()
                # calculate the function hash based on the assembly instructions of all blocks.
                for basic_block in func:
                    br.seek(basic_block.start)
                    bb_txt = br.read(basic_block.length)
                    func_hash.update(bb_txt)

                # update the function object with the calculated hash
                tx.run('MATCH (func) WHERE id(func) = {func_id} '
                       'SET func.hash = {func_hash}',
                       func_id=func_id, func_hash=func_hash.intdigest())
                # create nodes for all MLIL basic blocks, connect them with the function object
                # and calculate hash for whole function (hash of all bb)
                mlil_bb_hash = xxhash.xxh32()
                # current_id is a helper var in the creation of a linked list of basic blocks
                for basic_block_mlil in func.mlil:
                    for disasm_text in basic_block_mlil.disassembly_text:
                        mlil_bb_hash.update(str(disasm_text))
                    bb_id = tx.run('MATCH (node) WHERE id(node) = {func_id} '
                                   'MERGE (bb:BasicBlock { hash:$bb_hash })'
                                   'MERGE (node)-[:CONTAINS {orig_id:$func_id }]->(bb) '
                                   'RETURN id(bb) '
                                   , bb_hash=mlil_bb_hash.intdigest(), func_id=func_id,
                                   ).single().value()
                    mlil_bb_hash.reset()
                    current_instr_id = bb_id
                    # create nodes for all MLIL instructions within the basic blocks, and connect
                    # them to their parent bb according to their role in the instructions (operator, operand,symbol)
                    for instr in basic_block_mlil:
                        token_str = str(instr.tokens).strip('[').strip(']').replace("'", '')
                        instr_id = tx.run('MATCH (node) WHERE id(node) = {current_instr_id} '
                                          'MERGE (instr:Instruction {tokens:$tokens}) '
                                          'MERGE (node)-[:NEXT {orig_id: $current_instr_id }]->(instr) '
                                          'RETURN id(instr)',
                                          current_instr_id=current_instr_id, tokens=token_str).single().value()
                        current_instr_id = instr_id
            tx.sync()


driver = init_db()
populate_binaryview(bv, driver)
