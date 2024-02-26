from typing import Dict, List

from napalm.base import models


from .unifi import UnifiSwitchBase as _UnifiSwitchBase, correct_lldp_interface_names

class UnifiSwitchDriver(_UnifiSwitchBase):
    def get_lldp_neighbors_detail(self, interface: str = "") -> Dict[str, List[models.LLDPNeighborDetailDict]]:
        return correct_lldp_interface_names("0/", "Port ", super().get_lldp_neighbors_detail(interface))
    
    def _get_lldp_neighbors_detail(self, interface: str):
        if interface.startswith("Port"):
            interface = f"0/{interface.removeprefix('Port').strip()}"
        command = f"show lldp remote-device detail {interface}"
        return self.cli([command], use_texfsm=True)[command]

    def get_lldp_neighbors(self) -> Dict[str, List[models.LLDPNeighborDict]]:
        return correct_lldp_interface_names("0/", "Port ", super().get_lldp_neighbors())

    def _get_lldp_neighbors(self) -> Dict[str, List[models.LLDPNeighborDict]]:
        command = "show lldp remote-device all"
        return self.cli([command], use_texfsm=True)[command]
