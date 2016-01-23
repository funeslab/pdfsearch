# -*- coding: utf-8 -*-
programs = (
    ['ciudadanos', 'Ciudadanos'],
    ['enmarea', 'En Marea'],
    ['nos', 'Nós'],
    ['podemos', 'Podemos'],
    ['pp', 'PP'],
    ['psoe', 'PSOE'],
    ['up', 'Unidad Popular'],
    ['upyd', 'UPyD']
)

idx = {}
i = 0
for p in programs:
    idx[p[0]] = i
    i += 1

zones = (
    {'title': 'PP, PSOE, Cs, Podemos, UP, UPyD',
     'parties': [idx[p] for p in ('ciudadanos', 'podemos', 'pp',
                                  'psoe', 'up', 'upyd')]},
    {'title': 'Galicia',
     'parties': [idx[p] for p in ('ciudadanos', 'enmarea', 'nos', 'pp',
                                  'psoe', 'upyd')]}
)


def intersec_zone_parties(zone, parties):
    """ from integer indexes to parties program name """
    zone_parties = zones[zone]['parties']
    if parties:
        result = list(set(parties).intersection(zone_parties))
    else:
        result = zone_parties
    return [programs[i][0] for i in result]


# INE. Relación de comunidades y ciudades autónomas con sus códigos
data_INE = {
    '01': 'Andalucía',
    '02': 'Aragón',
    '03': 'Asturias, Principado de',
    '04': 'Balears, Illes',
    '05': 'Canarias',
    '06': 'Cantabria',
    '07': 'Castilla y León',
    '08': 'Castilla - La Mancha',
    '09': 'Cataluña',
    '10': 'Comunitat Valenciana',
    '11': 'Extremadura',
    '12': 'Galicia',
    '13': 'Madrid, Comunidad de',
    '14': 'Murcia, Región de',
    '15': 'Navarra, Comunidad Foral de',
    '16': 'País Vasco',
    '17': 'Rioja, La',
    '18': 'Ceuta',
    '19': 'Melilla'
}
