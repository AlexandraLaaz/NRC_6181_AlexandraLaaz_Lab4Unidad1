import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class HolidayEcuador(HolidayBase):
    """
    Una clase para representar un feriado en Ecuador por provincia (HolidayEcuador)
     Su objetivo es determinar si un
     fecha especifica es unas vacaciones lo mas rapido y flexible posible.
     https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
     ...
     Atributos (Hereda la clase HolidayBase)
     ----------
     prueba: calle
         codigo de provincia segun ISO3166-2
     Metodos
     -------
     __init__(self, plate, date, time, online=False):
         Construye todos los atributos necesarios para el objeto HolidayEcuador.
     _poblar(uno mismo, año):
         Devoluciones si una fecha es feriado o no
    """     
    # ISO 3166-2 codes for the principal subdivisions, 
    # called provinces
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCIA = ["EC-P"]  # TODO add more provinces

    def __init__(self, **kwargs):
        """
       Contructor con metodos necesario para los dias festivos de Ecuador.
        """         
        self.pais = "ECUADOR"
        self.prov = kwargs.pop("provincia", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, año):
        """
        Comprueba si una fecha es feriado o no
        
         Par�metros
         ----------
         a�o: calle
             a�o de una fecha
         Devoluciones
         -------
         Devuelve verdadero si una fecha es un d�a festivo, de lo contrario, se muestra como verdadero.
        """                    
        # Año Nuevo 
        self[datetime.date(año, JAN, 1)] = "A�o Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(año, DEC, 25)] = "Navidad [Christmas]"
        
        # Semana Sata
        self[easter(año) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(año)] = "D�a de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(año) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(año) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Dia del trabajador
        nombre = "D�a Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en s�bado o martes
        # el descanso obligatorio ir� al viernes o lunes inmediato anterior
        # respectivamente
        if año > 2015 and datetime.date(año, MAY, 1).weekday() in (5,1):
            self[datetime.date(año, MAY, 1) - datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif año > 2015 and datetime.date(año, MAY, 1).weekday() == 6:
            self[datetime.date(año, MAY, 1) + datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en mi�rcoles o jueves
        # se mover� al viernes de esa semana
        elif año > 2015 and  datetime.date(año, MAY, 1).weekday() in (2,3):
            self[datetime.date(año, MAY, 1) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, MAY, 1)] = nombre
        
        # Batalla de Pichincha, son las mismas raglas del dia del trabajador
        nombre = "Batalla del Pichincha [Pichincha Battle]"
        if año > 2015 and datetime.date(año, MAY, 24).weekday() in (5,1):
            self[datetime.date(año, MAY, 24).weekday() - datetime.timedelta(days=1)] = nombre
        elif año > 2015 and datetime.date(año, MAY, 24).weekday() == 6:
            self[datetime.date(año, MAY, 24) + datetime.timedelta(days=1)] = nombre
        elif año > 2015 and  datetime.date(año, MAY, 24).weekday() in (2,3):
            self[datetime.date(año, MAY, 24) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, MAY, 24)] = nombre
        
        # Primer grito de Independencia, son las mismas raglas del dia del trabajador
        nombre = "Primer Grito de la Independencia [First Cry of Independence]"
        if año > 2015 and datetime.date(año, AUG, 10).weekday() in (5,1):
            self[datetime.date(año, AUG, 10)- datetime.timedelta(days=1)] = nombre
        elif año > 2015 and datetime.date(año, AUG, 10).weekday() == 6:
            self[datetime.date(año, AUG, 10) + datetime.timedelta(days=1)] = nombre
        elif año > 2015 and  datetime.date(año, AUG, 10).weekday() in (2,3):
            self[datetime.date(año, AUG, 10) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, AUG, 10)] = nombre       
        
        # Independencia de Guayaquil, son las mismas raglas del dia del trabajador
        nombre = "Independencia de Guayaquil [Guayaquil's Independence]"
        if año > 2015 and datetime.date(año, OCT, 9).weekday() in (5,1):
            self[datetime.date(año, OCT, 9) - datetime.timedelta(days=1)] = nombre
        elif año > 2015 and datetime.date(año, OCT, 9).weekday() == 6:
            self[datetime.date(año, OCT, 9) + datetime.timedelta(days=1)] = nombre
        elif año > 2015 and  datetime.date(año, MAY, 1).weekday() in (2,3):
            self[datetime.date(año, OCT, 9) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, OCT, 9)] = nombre        
        
        # Dia de Difuntos
        nombredd = "D�a de los difuntos [Day of the Dead]" 
        # Independencia de Cuenca
        nombreic = "Independencia de Cuenca [Independence of Cuenca]"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906))
        #Para festivos nacionales y/o locales que coincidan en d�as corridos,
        #se aplicar�n las siguientes reglas:
        if (datetime.date(año, NOV, 2).weekday() == 5 and  datetime.date(año, NOV, 3).weekday() == 6):
            self[datetime.date(año, NOV, 2) - datetime.timedelta(days=1)] = nombredd
            self[datetime.date(año, NOV, 3) + datetime.timedelta(days=1)] = nombreic     
        elif (datetime.date(año, NOV, 3).weekday() == 2):
            self[datetime.date(año, NOV, 2)] = nombredd
            self[datetime.date(año, NOV, 3) - datetime.timedelta(days=2)] = nombreic
        elif (datetime.date(año, NOV, 3).weekday() == 3):
            self[datetime.date(año, NOV, 3)] = nombreic
            self[datetime.date(año, NOV, 2) + datetime.timedelta(days=2)] = nombredd
        elif (datetime.date(año, NOV, 3).weekday() == 5):
            self[datetime.date(año, NOV, 2)] =  nombredd
            self[datetime.date(año, NOV, 3) - datetime.timedelta(days=2)] = nombreic
        elif (datetime.date(año, NOV, 3).weekday() == 0):
            self[datetime.date(año, NOV, 3)] = nombreic
            self[datetime.date(año, NOV, 2) + datetime.timedelta(days=2)] = nombredd
        else:
            self[datetime.date(año, NOV, 2)] = nombredd
            self[datetime.date(año, NOV, 3)] = nombreic  
            
        # Fundaci�n de Quito, aplica solo para la provincia de Pichincha,
        # las reglas son las mismas que el d�a del trabajo
        nombre = "Fundaci�n de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if año > 2015 and datetime.date(año, DEC, 6).weekday() in (5,1):
                self[datetime.date(año, DEC, 6) - datetime.timedelta(days=1)] = nombre
            elif año > 2015 and datetime.date(año, DEC, 6).weekday() == 6:
                self[(datetime.date(año, DEC, 6).weekday()) + datetime.timedelta(days=1)] =nombre
            elif año > 2015 and  datetime.date(año, DEC, 6).weekday() in (2,3):
                self[datetime.date(año, DEC, 6) + rd(weekday=FR)] = nombre
            else:
                self[datetime.date(año, DEC, 6)] = nombre

class PicoPlaca:
    """
    Una clase para representar un vehiculo.
    medida de restriccion (Pico y Placa)
    - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Atributos
    ----------
    placa : calle
        El registro o patente de un veh�culo es una combinaci�n de caracteres alfab�ticos o num�ricos
        caracteres que identifican e individualizan el veh�culo respecto de los dem�s;
        
        El formato utilizado es
        XX-YYYY o XXX-YYYY,
        donde X es una letra may�scula e Y es un d�gito.
    fecha: calle
        Fecha en la que el veh�culo pretende transitar
        esta siguiendo el
        Formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
    tiempo: calle
        tiempo en que el veh�culo pretende transitar
        esta siguiendo el formato
        HH:MM: por ejemplo, 08:35, 19:30
    en l�nea: booleano, opcional
        si en l�nea == Verdadero, se utilizar� la API de d�as festivos abstractos
    M�todos
    -------
    __init__(self, plate, date, time, online=False):
        Construye todos los atributos necesarios.
        para el objeto PicoPlaca.
    plato (uno mismo):
        Obtiene el valor del atributo de placa
    placa (auto, valor):
        Establece el valor del atributo de la placa
    fecha (uno mismo):
        Obtiene el valor del atributo de fecha
    fecha (auto, valor):
        Establece el valor del atributo de fecha
    tiempo (uno mismo):
        Obtiene el valor del atributo de tiempo
    tiempo (uno mismo, valor):
        Establece el valor del atributo de tiempo
    __encontar_dia(yo, fecha):
        Devuelve el d�a a partir de la fecha: por ejemplo, mi�rcoles
    __is_forbidden_time(self, check_time):
        Devuelve True si el tiempo proporcionado est� dentro de las horas pico prohibidas, de lo contrario, False
    __es_vacaciones:
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un d�a festivo en Ecuador, de lo contrario, False
    predecir (auto):
        Devuelve True si el veh�culo con la placa especificada puede estar en la carretera en la fecha y hora especificadas, de lo contrario, False
    """
    #Days of the week
    __dias = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"]

    # Dictionary that holds the restrictions inf the form {day: forbidden last digit}
    __restricciones = {
            "Monday": [1, 2],
            "Tuesday": [3, 4],
            "Wednesday": [5, 6],
            "Thursday": [7, 8],
            "Friday": [9, 0],
            "Saturday": [],
            "Sunday": []}

    def __init__(self, placa, fecha, hora, enlinea=False):
        """
        Construye todos los atributos necesarios para el objeto PicoPlaca.
        
         Par�metros
         ----------
             placa : calle
                 El registro o patente de un veh�culo es una combinaci�n de caracteres alfab�ticos o num�ricos
                 caracteres que identifican e individualizan el veh�culo respecto de los dem�s;
                 El formato utilizado es AA-YYYY o XXX-YYYY, donde X es una letra may�scula e Y es un d�gito.
             fecha: calle
                 Fecha en la que el veh�culo pretende transitar
                 Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
             tiempo: calle
                 tiempo en que el veh�culo pretende transitar
                 Sigue el formato HH:MM: por ejemplo, 08:35, 19:30
             en l�nea: booleano, opcional
                 si en l�nea == Verdadero, se usar� la API de d�as festivos abstractos (el valor predeterminado es Falso)               
        """                
        self.placa = placa
        self.fecha = fecha
        self.hora = hora
        self.enlinea = enlinea

    @property
    def placa(self):
        """Gets (Obtiene) el valor del atributo placa"""
        return self._placa

    @placa.setter
    def placa(self, valor):
        """
        Sets(Establece) eval�a el atributo placa
         Par�metros
         ----------
         valor: cadena
        
         aumenta
         ------
         ValorError
             Si la cadena de valor no tiene el formato
             XX-YYYY o XXX-YYYY,
             donde X es una letra may�scula e Y es un d�gito
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', valor):
            raise ValueError(
                'La placa debe tener el siguiente formato: XX-YYYY o XXX-YYYY, donde X es una letra may�scula e Y es un d�gito')
        self._placa = valor

    @property
    def fecha(self):
        """Gets(Obtiene) el valor del atributo de fecha"""
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        """
        Sets(Establece) el valor del atributo de fecha
         Par�metros
         ----------
         valor: cadena
        
         aumenta
         ------
         ValorError
             Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(valor) != 10:
                raise ValueError
            datetime.datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._fecha = valor
        

    @property
    def hora(self):
        """Gets (Obtiene) el valor del atributo de tiempo"""
        return self._hora

    @hora.setter
    def hora(self, valor):
        """
        Sets(Establece) el valor del atributo de tiempo
         Par�metros
         ----------
         valor: cadena
        
         aumenta
         ------
         ValorError
             Si la cadena de valor no tiene el formato HH:MM (por ejemplo, 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', valor):
            raise ValueError(
                'La hora debe tener el siguiente formato: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._hora = valor

    def __encontrar_dia(self, fecha):
        """
        Encuentra el d�a a partir de la fecha: por ejemplo, mi�rcoles
         Par�metros
         ----------
         fecha: calle
             Est� siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
         Devoluciones
         -------
         Devuelve el d�a a partir de la fecha como una cadena
        """        
        d = datetime.datetime.strptime(fecha, '%Y-%m-%d').weekday()
        return self.__dias[d]

    def __es_tiempo_prohibido(self, check_fecha):
        """
        Comprueba si el tiempo proporcionado est� dentro de las horas pico prohibidas,
         donde las horas pico son: 07:00 - 09:30 y 16:00 - 19:30
         Par�metros
         ----------
         check_time : str
             Tiempo que se comprobar�. Est� en formato HH:MM: por ejemplo, 08:35, 19:15
         Devoluciones
         -------
         Devuelve True si el tiempo proporcionado est� dentro de las horas pico prohibidas, de lo contrario, False
        """           
        t = datetime.datetime.strptime(check_fecha, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))

    def __es_vacaciones(self, fecha, enlinea):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un d�a festivo en Ecuador
         si en l�nea == Verdadero, utilizar� una API REST, de lo contrario, generar� los d�as festivos del a�o examinado
        
         Par�metros
         ----------
         fecha: calle
             Est� siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
         en l�nea: booleano, opcional
             si en l�nea == Verdadero, se utilizar� la API de d�as festivos abstractos
         Devoluciones
         -------
         Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un d�a festivo en Ecuador, de lo contrario, False
        """            
        y, m, d = fecha.split('-')

        if enlinea:
            # API de vacaciones abstractapi, versi�n gratuita: 1000 solicitudes por mes
             # 1 solicitud por segundo
             # recuperar la clave API de la variable de entorno
            key = os.environ.get('VACACIONES_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave API
                raise requests.HTTPError(
                    'Falta la clave API. Guarde su clave en la variable de entorno HOLIDAYS API_KEY')
            if response.content == b'[]':  # si no hay vacaciones obtenemos una matriz vac�a
                return False
            # Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['nombre'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = HolidayEcuador(prov='EC-P')
            return fecha in ecu_holidays

    def predecir(self):
        """
        Comprueba si el veh�culo con la placa especificada puede estar en la carretera en la fecha y hora proporcionada seg�n las reglas de Pico y Placa:
         http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
         Devoluciones
         -------
         Devoluciones
         Verdadero si el veh�culo con
         la placa especificada puede estar en el camino
         en la fecha y hora especificadas, de lo contrario Falso
        """
        # Comprobar si la fecha es un d�a festivo
        if self.__es_vacaciones(self.fecha, self.enlinea):
            return True

        # Consultar veh�culos excluidos de la restricci�n seg�n la segunda letra de la placa o si se utilizan s�lo dos letras
         #https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.placa[1] in 'AUZEXM' or len(self.placa.split('-')[0]) == 2:
            return True

       # Compruebe si el tiempo proporcionado no est� en las horas pico prohibidas
        if not self.__es_tiempo_prohibido(self.hora):
            return True

        dia = self.__encontrar_dia(self.fecha) # Encuentra el d�a de la semana a partir de la fecha
         # Verifique si el �ltimo d�gito de la placa no est� restringido en este d�a en particular
        if int(self.placa[-1]) not in self.__restricciones[dia]:
            return True

        return False

if __name__ == '__main__':
    enlinea=False
    #Ingreso de datos lo que es la placa, fecha y hora... respectando los devidos formatos
    placa=input("Ingrese la placa por favor, la placa del vehiculo: XXX-YYYY o XX-YYYY, donde X es una letra may�scula e Y es un d�gito: ")
    fecha=input("Ingrese la fecha por favor, la fecha a comprobar: AAAA-MM-DD: ")
    hora=input("Ingrese la hora por favor,la hora a comprobar: HH:MM:  ")

    pyp = PicoPlaca(placa, fecha, hora, enlinea)
  #En esta parte se muestra el vehiculo y su placa respectiva la cual puede o no 
  #estar en carretera con fecha y de que hora a que hora 
    if pyp.predecir():
        print(
            'El vehiculo con placa {} PUEDE estar en la carretera el {} a las {}.'.format(
                placa,
                fecha,
                hora))
    else:
        print(
            'El vehículo con la placa {} NOPUEDE estra en la carrtera el {} a las {}.'.format(
                placa,
                fecha,
                hora))