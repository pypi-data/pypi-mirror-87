# pylint: disable=broad-except, invalid-name
import os
from utils import log
from test_framework.database import SqlConnection
from test_framework.state import NodeState
from utils.system import get_ip_address


NODE_STATE_TABLE_COLUM = [
    {"name": "index", "type": "int(11) AUTO_INCREMENT PRIMARY KEY"},
    {"name": "state", "type": "VARCHAR(45)"},
    {"name": "time", "type": "datetime DEFAULT CURRENT_TIMESTAMP"}]


class NodeSqlConnection(SqlConnection):

    def __init__(self, db_name="nodes"):
        super(NodeSqlConnection, self).__init__(db_name=db_name)
        self.node_table = "node"

    def create_node_state_table(self, node_ip):
        table_name ="{}".format(node_ip)
        self.create_table(table_name, NODE_STATE_TABLE_COLUM)
        return table_name

    def create_new_node(self, node):
        table_name = self.create_node_state_table(node["ip"])
        self.insert_to_table("node", vendor=node["vendor_name"],
            ip=node["ip"],
            name="env_{}".format(node["ip"]),
            system=node["operating_system"],
            capacity=node["capacity"],
            fw=node["fw_version"],
            state=NodeState.verdicts_map[NodeState.Idle],
            state_table=table_name)

    def update_exist_node(self, node):
        str_date = "`system`='{}',capacity='{}',fw='{}',state='{}',vendor='{}'".format(
            node["operating_system"], node["capacity"], node["fw_version"],
            NodeState.verdicts_map[NodeState.Idle], node["vendor_name"]
        )
        update_command = "UPDATE node SET {} WHERE ip='{}'".format(str_date, node["ip"])
        self.cursor.execute(update_command)
        self.conn.commit()

    def is_exist_node(self, node):
        sql_command = "SELECT * from node WHERE ip='{}'".format(node["ip"])
        self.cursor.execute(sql_command)
        gets = self.cursor.fetchone()
        result = True if gets else False
        return result

    def update_node_state(self, state):
        ip_address = get_ip_address()
        table = "`{}`".format(ip_address)
        self.insert_to_table(table, state=NodeState.verdicts_map[state])

    def update_power_cycle_node_state(self, state):
        if "TARGETIP" in os.environ.keys():
            target_ip = os.environ['TARGETIP']
            if target_ip != "0.0.0.0":
                table = "`{}`".format(target_ip)
                if self.is_exist_table(target_ip) is True:
                    self.insert_to_table(table, state=NodeState.verdicts_map[state])


def update_env_state(func):
    def func_wrapper(*args, **kwargs):
        node = func(*args, **kwargs)
        try:
            sql_connection = NodeSqlConnection()
            if sql_connection.is_exist_node(node) is True:
                sql_connection.update_exist_node(node)
            else:
                sql_connection.create_new_node(node)
        except Exception as all_exception:
            log.ERR(all_exception)
        return node
    return func_wrapper


def update_node_state(func):
    def func_wrapper(*args, **kwargs):
        is_updated, state = func(*args, **kwargs)
        if is_updated is True:
            try:
                sql_connection = NodeSqlConnection()
                sql_connection.update_node_state(state)
                sql_connection.update_power_cycle_node_state(state)
            except Exception as all_exception:
                log.ERR(all_exception)
        return is_updated, state
    return func_wrapper
