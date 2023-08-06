
from jinja2 import Template
from dnac.exception.BadProjectFileException import InvalidOperationException

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class PAP:
    def __init__(self, name, model, floor = None):
        self.name = name
        self._parent_ = floor
        self.model = model
        self._pos_ = -1, -1, -1

    @property
    def name(self):
        return self._name_

    @name.setter
    def name(self, given_name):
        self._name_ = given_name

    @property
    def model(self):
        return self._model_

    @model.setter
    def model(self, given_model):
        self._model_ = given_model

    @property
    def parent(self):
        return self._parent_

    @parent.setter
    def parent(self, floor):
        self._parent_ = floor

    @property
    def position(self):
        return self._pos_

    @position.setter
    def position(self, new_position):
        if not self.parent:
            raise InvalidOperationException('Cannot position unassigned Access Point')
        self._pos_ = new_position

    @staticmethod
    def jsonTemplate(model):
        if model.upper() == '9130I':
            return '{"attributes":{"name":"{{ tvPAP_NAME }}","macaddress":null,"type":101,"typeString":"AP9130I"},"location":{"lattitude":0,"longtitude":0,"altitude":0},"position":{"x":{{ tvX }},"y":{{ tvY }},"z":{{ tvZ }} },"isSensor":false,"radioCount":3,"radios":[{"attributes":{"slotId":0,"ifType":1,"ifTypeString":"802.11b/g","ifTypeSubband":"B"},"antenna":{"name":"Internal-9130-2.4GHz","type":"internal","azimuthAngle":0,"elevationAngle":0,"gain":0},"isSensor":true},{"attributes":{"slotId":1,"ifType":2,"ifTypeString":"802.11a","ifTypeSubband":"A"},"antenna":{"name":"Internal-9130-5GHz","type":"internal","azimuthAngle":0,"elevationAngle":0,"gain":0},"isSensor":true},{"attributes":{"slotId":2,"ifType":3,"ifTypeString":"802.11a/b/g/n","ifTypeSubband":"ABGN"},"antenna":{"name":"Internal-Dual-Band","type":"internal","azimuthAngle":0,"elevationAngle":0,"gain":0},"isSensor":true}]}'
        else:
            return None # for now...

    @property
    def dnacJson(self):
        if self.model.upper() == '9130I':
            template = Template(PAP.jsonTemplate(self.model))
        else:
            template = None

        # Generate stringified operations list...
        return template.render(tvPAP_NAME=self.name, tvX=self.position[0], tvY=self.position[1], tvZ=self.position[2] ) if template else None
