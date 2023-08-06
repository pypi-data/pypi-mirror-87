import logging

from netmiko import ConnectHandler
from dataclasses import dataclass
from fn_ont_expunge.exceptions import ServicePortError, ExpungeCmdError, DBExpungeError
from sqlalchemy.orm import Session
from fibrenest_db_models.old import Service


@dataclass(eq=False)
class ONTExpunge:
    """"
    Performs expunge of an ONT from OLT and the DB
    :param ont_sn: ONT Serial number
    :param ontid: ONT ID as its on the OLT
    :param portid: The OLT port where this ONT is connected to
    :param slotid: The OLT slot where this ONT is connected to
    :param frameid: The OLT frame where this ONT is connected to
    :param olt_device_details: OLT Device details used for SSH connection. These are passed directly to
    netmiko's Connecthandler
    :param logger: logging.Logger object
    :param old_db_session: sqlalchemy Session object for session to the DB
    """
    ont_sn: str
    ontid: int
    portid: int
    slotid: int
    frameid: int
    olt_device_details: dict
    logger: logging.Logger
    old_db_session: Session

    def __enter__(self):
        self.logger.info(f'Establishing SSH connection to: {self.olt_device_details["host"]}')
        self.conn = ConnectHandler(**self.olt_device_details)
        self.logger.info(f'Successfully established SSH connection to: {self.olt_device_details["host"]}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(f'Disconnecting SSH connection from: {self.olt_device_details["host"]}')
        self.conn.disconnect()
        self.logger.info(f'Successfully disconnected SSH connection from: {self.olt_device_details["host"]}')

    def _expunge_olt(self):
        """
        Expunges ONT from OLT
        :return: None
        :raise ServicePortError: If failed to get service ports associated with ONT
        :raise ExpungeCmdError: If a command failed
        """

        self.logger.info(f'Expunging ONT: {self.ont_sn} from OLT: {self.olt_device_details["host"]}')

        self.logger.info(f'Entering enable mode')
        self.conn.enable()

        self.logger.info(f'Entering config mode')
        self.conn.config_mode()

        self.logger.info(f'Deleting service ports')
        self.conn.send_command_timing(
            f'undo service-port port {self.frameid}/{self.slotid}/{self.portid} ont {self.ontid}'
        )
        svc_port_delete_output = self.conn.send_command_timing('y')
        if 'Failure' in svc_port_delete_output \
                or 'The number of total service virtual port which have been deleted: 2' not in svc_port_delete_output:
            error_msg = f'Failed to delete service ports for ONT: {self.ont_sn} on OLT: {self.olt_device_details["host"]}. ' \
                        f'OLT command output: {svc_port_delete_output}'
            self.logger.error(error_msg)
            raise ServicePortError(error_msg)
        self.logger.info(f'Successfully deleted service ports')

        self.logger.info(f'Deleting ONT')
        intf_cmd_output = self.conn.send_command(f'interface gpon {self.frameid}/{self.slotid}', expect_string='#')
        if 'Failure' in intf_cmd_output:
            error_msg = f'Failed command while expunging ONT: {self.ont_sn} from OLT: {self.olt_device_details["host"]}. ' \
                        f'cmd: interface gpon {self.frameid}/{self.slotid}. cmd_output: {intf_cmd_output}'
            self.logger.error(error_msg)
            raise ExpungeCmdError(error_msg)
        ont_delete_output = self.conn.send_command(f'ont delete {self.portid} {self.ontid}', expect_string='#')
        if 'Failure' in ont_delete_output \
                or 'Number of ONTs that can be deleted: 1, success: 1' not in ont_delete_output:
            error_msg = f'Failed command while expunging ONT: {self.ont_sn} from OLT: {self.olt_device_details["host"]}. ' \
                        f'cmd: ont delete {self.portid} {self.ontid}. cmd_output: {intf_cmd_output}'
            self.logger.error(error_msg)
            raise ExpungeCmdError(error_msg)
        self.logger.info(f'Successfully expunged ONT: {self.ont_sn} from OLT: {self.olt_device_details["host"]}')

        self.logger.info('Exiting config mode')
        self.conn.exit_config_mode()

        self.logger.info('Saving config')
        self.conn.save_config()

        return

    def _expunge_db(self):
        """
        Expunges ONT from Database
        :return: None
        :raise DBExpungeError - If any DB expunge error
        """

        self.logger.info(f'Expunging ONT: {self.ont_sn} from Database')
        old_ont_data = self.old_db_session.query(Service).filter(
            Service.pon == self.ont_sn
        ).with_for_update().one()
        self.logger.info(f'PPP state is: {old_ont_data.ppp_prov_state}')

        if old_ont_data.ppp_prov_state != 'NOT_STARTED':
            self.logger.info(f'Setting subs status to deleted to delete radius records')
            old_ont_data.subs_status = 'DELETED'
            self.old_db_session.commit()
            # The ppp prov state should change to NOT_STARTED. If that does not happen, raise error
            if old_ont_data.ppp_prov_state != 'NOT_STARTED':
                error_msg = f'Failed to change ppp prov state to NOT_STARTED while expunging ONT: {self.ont_sn} from DB. ' \
                            f'PPP prov state is: {old_ont_data.ppp_prov_state}'
                self.logger.error(error_msg)
                raise DBExpungeError(error_msg)

        self.logger.info('Deleting DB record')
        self.old_db_session.delete(old_ont_data)
        self.old_db_session.commit()
        self.logger.info(f'Successfully expunged ONT: {self.ont_sn} from database')
        return

    def expunge_ont(self):
        """
        Expunges ONT from OLT and Database
        :return: None
        :raise DBExpungeError - If any DB expunge error
        :raise ServicePortError: If failed to get service ports associated with ONT
        :raise ExpungeCmdError: If a command failed while expunging from OLT
        """

        self.logger.info(f'Expunging ONT: {self.ont_sn} from OLT')
        self._expunge_olt()

        self.logger.info(f'Expunging ONT: {self.ont_sn} from Database')
        self._expunge_db()
