

class Matview(str):

    @property
    def schemaname(self):
        return str(self).split('.')[0]

    @property
    def matviewname(self):
        return str(self).split('.')[1]
