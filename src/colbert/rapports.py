# -*- coding: utf-8 -*-

import datetime, pytz
import copy
from icalendar import Calendar

from colbert import daterange
from colbert.utils import DATE_FMT
from colbert.utils import latex_escape

DATE_RAPPORT_FMT = "%A %d"
HOUR_MIN_FMT = "%H.%M"

def rapport_activite(calendrier_ical, date_debut, date_fin, titre, ref_facture):
    """Extract activity data from an iCal-endar for a period. """
    
    rapport = {
        "titre": titre,
        "ref_facture": ref_facture,
        "detail": [],
    }

    cal = Calendar.from_ical(calendrier_ical.read())

    # First, we gather events by datetime.date.
    events_by_date = {}
    for component in cal.walk():
        if component.name == "VEVENT":
            date_debut_event = component["DTSTART"].dt
            date_fin_event = component["DTEND"].dt
            # La date de fin des Events de type journée complète n'est pas inclusive.
            # http://www.bedework.org/trac/bedework/wiki/Bedework/DevDocs/DtstartEndNotes
            if not hasattr(date_fin_event, "date"):
                date_fin_event = date_fin_event - datetime.timedelta(1)

            date_debut_event_date, date_fin_event_date = [(lambda d: (hasattr(d, "date") and d.date() or d))(day)
                                                            for day in (date_debut_event, date_fin_event)]
            if (date_debut <= date_debut_event_date <= date_fin):
                for day in daterange.daterange(date_debut_event_date, date_fin_event_date):
                    events = events_by_date.setdefault(day, [])
                    events.append((date_debut_event, date_fin_event, unicode(component["SUMMARY"])))

    # Then, events are sorted by date_debut in the same day but we must cast date in datetime to compare.
    def sort_date_and_datetime(x, y):
        x, y = [(lambda d: (not hasattr(d, "date") and \
                            datetime.datetime(d.year, d.month, d.day, tzinfo=pytz.utc) or \
                            d))(d) for d in (x, y)]
        return cmp(x, y)

    for day in events_by_date.keys():
        events_by_date[day] = sorted(events_by_date[day],
                                     key=lambda e: e[0],
                                     cmp=sort_date_and_datetime)

    # Then we are distinguishing datetime.date and datetime.datetime in the same day.
    for day in sorted(events_by_date):
        rapport["detail"].append([
            day, [{
                "from": hasattr(debut, "hour") and debut.strftime(HOUR_MIN_FMT) or None,
                "to": hasattr(fin, "hour") and fin.strftime(HOUR_MIN_FMT) or None,
                "intitule": intitule
            } for debut, fin, intitule in events_by_date[day]]
        ])

    rapport["nb_jours"] = len(rapport["detail"])
    return rapport

def rapport_activite_to_tex(activite, tex_template, output_file):
    """Produce a TeX file from a template and a json activity file.
    
    >>> activite = {
    ...     "titre": "Mon rapport d'activité - Mars 2012",
    ...     "ref_facture": "2012-003",
    ...     "nb_jours": 3,
    ...     "detail": [
    ...         ["datetime.date(2012, 3, 9)", [
    ...             {
    ...                 "intitule": "A long task, during 3 days!"
    ...             }, 
    ...             {
    ...                 "from": "19.00",
    ...                 "to": "19.30",
    ...                 "intitule":"Go somewhere, done something."
    ...             }
    ...         ]],
    ...         ["datetime.date(2012, 3, 10)", [
    ...             {
    ...                 "intitule": "A long task, during 3 days!"
    ...             }
    ...         ]],
    ...         ["datetime.date(2012, 3, 11)", [
    ...             {
    ...                 "intitule": "A long task, during 3 days!"
    ...             }, 
    ...             {
    ...                 "from": "9.00",
    ...                 "to": "9.30",
    ...                 "intitule":"Fix the printer."
    ...             }, 
    ...             {
    ...                 "from": "10.00",
    ...                 "to": "10.30",
    ...                 "intitule": "Change some CSS stuffs.",
    ...             }, 
    ...             {
    ...                 "from": "14.00",
    ...                 "to": "15.30",
    ...                 "intitule": "Make some coffee.",
    ...             }, 
    ...             {
    ...                 "from": "16.15",
    ...                 "to": "17.45",
    ...                 "intitule": "Was there at a stupid brainstorming with marketing guys.",
    ...             }
    ...         ]]
    ...     ]
    ... }

    """

    kwargs = activite.copy()

    # Lignes de facturation.
    lignes_activites = []
    for date, activities in activite["detail"]:
        for i, activite_jour in enumerate(activities):
            col_1 = ""
            if i == 0:
                col_1 = datetime.datetime.strptime(date, DATE_FMT).strftime(DATE_RAPPORT_FMT)
            lignes_activites.append(u" %s  & %s\\\\" % (col_1, intitule_activite_to_tex(activite_jour)))

    kwargs["lignes_activites"] = "\n".join(lignes_activites)
    tex_string = tex_template.read() % kwargs
    output_file.write(tex_string)

def intitule_activite_to_tex(activite_jour):
    tex_fmt = "\\emph{%s}"
    if not activite_jour.get("to"):
        tex_fmt = "%s"

    return tex_fmt % latex_escape(activite_jour["intitule"])
