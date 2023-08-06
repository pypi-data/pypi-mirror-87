
from dnac.exception.BadProjectFileException import InvalidOperationException

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class AccessPoint:
    def __init__(self, id, name, eq_model, model, floor):
        self.id = id
        self.name = name
        self._parent_ = floor
        self.equiv_model = eq_model
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
    def equiv_model(self):
        return self._equivalent_model_

    @equiv_model.setter
    def equiv_model(self, given_model):
        self._equivalent_model_ = given_model

    @property
    def parent(self):
        return self._parent_

    @parent.setter
    def parent(self, floor):
        self._parent_ = floor

    @property
    def id(self):
        return self._id_

    @id.setter
    def id(self, id):
        self._id_ = id

    @property
    def position(self):
        return self._pos_

    @position.setter
    def position(self, new_position):
        if not self.parent:
            raise InvalidOperationException('Cannot position unassigned Access Point')
        self._pos_ = new_position

    def unposition(self):
        self.position(-1, -1, -1)
