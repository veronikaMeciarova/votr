from datetime import datetime
from fladgejt.structures import Termin, Prihlasena_osoba


def get_terminy():
    return [Termin(id=1,
                   predmet_id=15,
                   datum=datetime(datetime.today().year - 1, 12, 24).date(),
                   cas=datetime.time(10, 0),
                   miestnost='FMFI M 217',
                   pocet_prihlasenych=0,
                   maximalne_prihlasenych=5,
                   hodnotiaci='RNDr. Emanuel Vyhadzovač, PhD.',
                   prihlasovanie_od=datetime(
                       datetime.today().year - 1, 12, 22, 9, 0),
                   prihlasovanie_do=datetime(
                       datetime.today().year - 1, 12, 24, 9, 59),
                   poznamka=None,
                   moznost_prihlasit='A'),
            Termin(id=2,
                   predmet_id=15,
                   datum=datetime(datetime.today().year, 1, 12).date(),
                   cas=datetime.time(14, 0),
                   miestnost='FMFI M 118',
                   pocet_prihlasenych=3,
                   maximalne_prihlasenych=7,
                   hodnotiaci='RNDr. Emanuel Vyhadzovač, PhD.',
                   prihlasovanie_od=datetime(
                       datetime.today().year, 1, 1, 9, 0),
                   prihlasovanie_do=datetime(
                       datetime.today().year, 1, 11, 23, 59),
                   poznamka='Prineste si pero a papier.',
                   moznost_prihlasit='A'),
            Termin(id=3,
                   predmet_id=15,
                   datum=datetime(datetime.today().year, 1, 20).date(),
                   cas=datetime.time(10, 0),
                   miestnost='FMFI I-8',
                   pocet_prihlasenych=4,
                   maximalne_prihlasenych=4,
                   hodnotiaci='RNDr. Emanuel Vyhadzovač, PhD.',
                   prihlasovanie_od=datetime(
                       datetime.today().year, 12, 22, 15, 0),
                   prihlasovanie_do=datetime(
                       datetime.today().year + 1, 1, 19, 20, 59),
                   poznamka=None,
                   moznost_prihlasit='N'),
            Termin(id=4,
                   predmet_id=16,
                   datum=datetime(datetime.today().year, 2, 1).date(),
                   cas=datetime.time(17, 0),
                   miestnost='FMFI F 108',
                   pocet_prihlasenych=0,
                   maximalne_prihlasenych=5,
                   hodnotiaci='RNDr. Emanuel Vyhadzovač, PhD.',
                   prihlasovanie_od=datetime(
                       datetime.today().year, 1, 10, 9, 0),
                   prihlasovanie_do=datetime(
                       datetime.today().year, 2, 1, 9, 59),
                   poznamka=None,
                   moznost_prihlasit='A'),
            Termin(id=5,
                   predmet_id=10,
                   datum=datetime(datetime.today().year, 12, 22).date(),
                   cas=datetime.time(17, 0),
                   miestnost='FMFI F 2',
                   pocet_prihlasenych=1,
                   maximalne_prihlasenych=5,
                   hodnotiaci='RNDr. Emanuel Vyhadzovač, PhD.',
                   prihlasovanie_od=datetime(
                       datetime.today().year, 12, 18, 9, 0),
                   prihlasovanie_do=datetime(
                       datetime.today().year, 12, 22, 9, 59),
                   poznamka=None,
                   moznost_prihlasit='N')]


def zoznam_prihlasenych(termin_id):
    if termin_id == 2:
        return [Prihlasena_osoba(skratka='INF',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 1, 1, 9, 1),
                                 plne_meno='Ignác Poctivý',
                                 rocnik=2),
                Prihlasena_osoba(skratka='mINF',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 1, 9, 19, 1),
                                 plne_meno='Bc. Gustáv Šikovný',
                                 rocnik=1),
                Prihlasena_osoba(skratka='FYZ',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 1, 2, 14, 2),
                                 plne_meno='Alexandra Múdra',
                                 rocnik=2)]
    elif termin_id == 3:
        return [Prihlasena_osoba(skratka='MAT',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 1, 1, 9, 1),
                                 plne_meno='Karol František Normálny',
                                 rocnik=2),
                Prihlasena_osoba(skratka='mINF',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 1, 7, 19, 1),
                                 plne_meno='Bc. Ján von Informačný',
                                 rocnik=1),
                Prihlasena_osoba(skratka='FYZ',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 12, 23, 14, 2),
                                 plne_meno='Albert Relatívny',
                                 rocnik=2),
                Prihlasena_osoba(skratka='INF',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 12, 24, 9, 1),
                                 plne_meno='Alan Stavový',
                                 rocnik=2)]
    elif termin_id == 5:
        return [Prihlasena_osoba(skratka='mINF',
                                 datum_prihlasenia=datetime(
                                     datetime.today().year, 12, 19, 19, 1),
                                 plne_meno='Bc. Ján von Informačný',
                                 rocnik=1)]
    else:
        raise KeyError('Požadovaný termin_id neexistuje.')


def get_prihlasene_terminy():
    return [termin
            for termin in get_terminy()
            if termin.id == 3 or termin.id == 5]