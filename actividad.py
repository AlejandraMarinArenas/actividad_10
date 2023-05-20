from abc import ABC, abstractmethod
from errores import NoCumpleLongitudMinimaError, NoTieneLetraMayusculaError, NoTieneLetraMinusculaError, NoTieneNumeroError, NoTieneCaracterEspecialError, NoTienePalabraSecretaError

class ReglaValidacion(ABC):

    def _init_(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        if len(clave) <= self._longitud_esperada:
            raise NoCumpleLongitudMinimaError(f"La longitud de la clave debe ser mayor a {self._longitud_esperada}")

    def _contiene_mayuscula(self, clave):
        if not any(caracter.isupper() for caracter in clave):
            raise NoTieneLetraMayusculaError("La clave debe contener al menos una letra mayúscula")

    def _contiene_minuscula(self, clave):
        if not any(caracter.islower() for caracter in clave):
            raise NoTieneLetraMinusculaError("La clave debe contener al menos una letra minúscula")

    def _contiene_numero(self, clave):
        if not any(caracter.isdigit() for caracter in clave):
            raise NoTieneNumeroError("La clave debe contener al menos un número")

    @abstractmethod
    def es_valida(self, clave):
        pass


class ReglaValidacionGanimedes(ReglaValidacion):

    def _init_(self, longitud_esperada):
        super()._init_(longitud_esperada)

    def _contiene_caracter_especial(self, clave):
        if not any(caracter in '@_#$%' for caracter in clave):
            raise NoTieneCaracterEspecialError("La clave debe contener al menos un caracter especial (@, _, #, $, %)")

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self._contiene_caracter_especial(clave)
        return True


class ReglaValidacionCalisto(ReglaValidacion):

    def _init_(self, longitud_esperada):
        super()._init_(longitud_esperada)

    def _contiene_calisto(self, clave):
        if 'calisto' not in clave.lower():
            raise NoTienePalabraSecretaError("La clave debe contener la palabra 'calisto' con al menos dos letras mayúsculas, pero no todas")

        ocurrencias = [clave[i:i+7] for i in range(len(clave)-6) if clave[i:i+7].lower() == 'calisto']
        for ocurrencia in ocurrencias:
            if sum(1 for c in ocurrencia if c.isupper()) < 2 or ocurrencia.isupper():
                raise NoTienePalabraSecretaError("La clave debe contener la palabra 'calisto' con al menos dos letras mayúsculas, pero no todas")

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self._contiene_calisto(clave)
        return True


class Validador:

    def _init_(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)
