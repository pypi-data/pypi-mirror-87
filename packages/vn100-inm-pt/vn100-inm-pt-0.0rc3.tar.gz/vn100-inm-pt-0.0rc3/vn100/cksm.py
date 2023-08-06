class CksmFletcher16:
    '''Utilidad para implementar suma de verificación a cadenas de datos'''


    @staticmethod
    def incrustarCksm(datagrama):
        """Calcula la suma de verificación del datagrama dado, y lo incrusta 
        en los primeros dos caracteres. Es un método estático."""
        _cksm = CksmFletcher16.__calcularCksmDatagrama(datagrama)
        # Meter la suma de verificación en datagrama
        for i in range(0, 2):
            datagrama[i] = _cksm[i]
        return CksmFletcher16.evaluarDatagrama(datagrama)

    @staticmethod
    def evaluarDatagrama(datagrama):
        """Verifica la suma de verificación del datagrama dado, devoviendo 1
        si está correcto, y 0 si no lo es. Es un método estático."""
        _cksm = CksmFletcher16.__calcularCksmDatagrama(datagrama)
        return 1 if _cksm[0] == datagrama[0] and _cksm[1] == datagrama[1] else 0


    @staticmethod
    def __calcularCksmDatagrama(datosEvaluados):
        """Calcula la suma de verificación. Es un método estático, y no debería usarse
        públicamente."""
        res_cksm = bytearray([0, 0])
        sum1 = 255
        sum2 = 255
        i = 2
        longiDatosEvaluados = len(datosEvaluados)
        longi = longiDatosEvaluados - i
        while (longi > 0):
            tlongi = (longiDatosEvaluados - 2) if longi > (longiDatosEvaluados - 2) else longi
            longi -= tlongi
            while True:
                sum1 += datosEvaluados[i]
                sum2 += sum1
                i += 1

                tlongi -= 1
                if tlongi == 0:
                    break
        
        # Reducción de resultado por caracteres de 8 bits:
        while (sum1 > 255 or sum2 > 255):
            sum1 = (sum1 & 255) + (sum1 >> 8)
            sum2 = (sum2 & 255) + (sum2 >> 8)

        res_cksm[0] = sum1
        res_cksm[1] = sum2
        return res_cksm
        

"""
//// Prueba y uso de suma de verificación Fletcher 16 ////

// Incrustar suma de verificación //

>>> datagrama = bytearray([0, 0, 5, 242, 25, 12])
>>> datagrama
>>> CksmFletcher16.incrustarCksm(datagrama)
>>> datagrama



// Evaluar suma de verificación //

// Responde 1 si el checksum es correcto y 0 si no

1. Datagrama malo:
>>> datagrama = bytearray([35, 16, 5, 242, 25, 12])
>>> datagrama
>>> CksmFletcher16.evaluarDatagrama(datagrama)

2. Datagrama bueno:
>>> datagrama = bytearray([29, 14, 5, 242, 25, 12])
>>> datagrama
>>> CksmFletcher16.evaluarDatagrama(datagrama)
"""