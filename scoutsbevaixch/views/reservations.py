from datetime import date, time, datetime
import json
import traceback
import locale

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from dotenv import load_dotenv
import os

from .google_calendar import get_events, add_event, get_event
from .telegram_chat import send_message_async

load_dotenv()

MAX_LENGTH = 14
MAX_FUTURE = 365
PRICE_MORNING = 180
PRICE_EVENING = 180
PRICE_EVENING_DORTOIRES = 230
CAUTION = 300
CURRENCY = " CHF"
tz = "Europe/Zurich"

# locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def validation(request, id):
    return render(request, "validation.html", {"id": id})


def validation_real(request, id):
    event_demandes = get_event(os.getenv("CALENDAR_DEMANDE"), id)
    event_locations = get_event_from_event(event_demandes)
    add_event(os.getenv("CALENDAR_LOCATIONS"), event_locations)
    return render(request, "validation_real.html")


def reservations_confirmation(request):
    return render(request, "reservations_confirmation.html")


class Reservations(View):
    async def get(self, request):
        return render(request, "reservations.html")

    async def post(self, request):
        return await Reservations.validation_pipeline(request, True)

    async def options(self, request):
        return await Reservations.validation_pipeline(request, False)

    async def validation_pipeline(request, write):
        error = None
        try:
            data = dict(json.loads(request.body))
            validate_date(data)
            compute_price(data)
            validate_age(data)
            validate_data(data)
            check_if_has_events(data)
            if write:
                create_description(data)
                data["event"] = add_event(
                    os.getenv("CALENDAR_DEMANDE"), get_event_from_location(data))
                message = data["description"] + \
                    "\nValidation:\nhttps://scouts-bevaix.ch/validation/" + \
                    data["event"]["id"]
                await send_message_async(message)
        except Exception as e:
            print(traceback.format_exc())
            error = "Erreur: " + e.args[0]

        output = {
            "prix": data.get("prix", ""),
            "caution": data.get("caution", CAUTION),
            "total": data.get("total", CAUTION),
            "error": error,
            "valid": error is None,
        }
        return JsonResponse(output)


def get_event_from_event(event):
    return {
        "summary": event["summary"],
        "start": event["start"],
        "end": event["end"],
    }


def get_event_from_location(data):
    return {
        "summary": "Location",
        "description": data["description"],
        "start": {
            "dateTime": data["start_datetime"].isoformat("T"),
            "timeZone": tz
        },
        "end": {
            "dateTime": data["end_datetime"].isoformat("T"),
            "timeZone": tz
        },
    }


def validate_data(data):
    mandatory = ["prenom", "nom", "adresse", "cp_localite", "email", "telephone", "date_de_naissance",
                 "date_debut", "date_fin", "heure_debut", "heure_fin", "nombre_de_personnes"]

    if not all(k in data.keys() for k in mandatory):
        raise Exception("Missing fields")


def create_description(data):
    start_date_str = datetime.strftime(
        data["start_datetime"], "%A %d %B %Y %H:%M")
    end_date_str = datetime.strftime(
        data["end_datetime"], "%A %d %B %Y %H:%M")
    naissance = datetime.strftime(
        data["date_de_naissance_datetime"], "%d %B %Y")

    data["description"] = f"""Prénom: {data['prenom']} {data['nom']}
Adresse: {data['adresse']}, {data['cp_localite']}
Email: {data['email']}
Téléphone: {data['telephone']}
Date de naissance: {naissance}

Début: {start_date_str}
Fin: {end_date_str}
Dortoires: {'avec' if 'dortoires' in data else 'sans'}
Prix (sans caution): {data['prix']}
Total (avec caution): {data['total']}

Remarques: {data["remarques"]}

{'À accepté le contrat' if 'accept_contract' in data else ''}
"""


def validate_age(data):
    try:
        date_de_naissance = datetime.combine(
            date.fromisoformat(data["date_de_naissance"]), time())
        data["date_de_naissance_datetime"] = date_de_naissance
        age = calculate_age_to_day(date_de_naissance, data["start_datetime"])
        if age < 18:
            raise Exception()
    except Exception as e:
        print(e)
        raise Exception(
            "La personne de contact doit être majeur le jour du début de la location")


def calculate_age_to_day(born, day):
    return day.year - born.year - ((day.month, day.day) < (born.month, born.day))


def compute_price(data):
    delta = data["end_datetime"] - data["start_datetime"]
    price_evening = PRICE_EVENING_DORTOIRES if "dortoires" in data else PRICE_EVENING
    price_day = price_evening + PRICE_MORNING
    price = delta.days * price_day
    if data["start_datetime"].hour == 11 and data["end_datetime"].hour == 17:
        price += PRICE_MORNING
    if data["start_datetime"].hour == 17 and data["end_datetime"].hour == 11:
        price += price_evening
    data["prix"] = str(price) + CURRENCY
    data["caution"] = str(CAUTION) + CURRENCY
    data["total"] = str(price + CAUTION) + CURRENCY


def validate_date(data):
    try:
        data["start_datetime"] = validate_datetime(
            data["date_debut"], data["heure_debut"])
        data["end_datetime"] = validate_datetime(
            data["date_fin"], data["heure_fin"])
    except Exception as e:
        raise Exception("Veuillez entrer un horaire de location")

    now = datetime.now()
    start_in = data["start_datetime"] - now
    length = (data["end_datetime"] - data["start_datetime"]).days

    if start_in.total_seconds() <= 0:
        raise Exception("La réservation ne peut pas commencer dans le passé")

    if start_in.days >= MAX_FUTURE:
        raise Exception(
            f"La réservation ne peut pas commencer dans plus de {MAX_FUTURE} jours")

    if length >= MAX_LENGTH:
        raise Exception(
            f"La réservation ne peut pas duréer plus de {MAX_LENGTH} jours, veuillez contacter le/la gérant.e")

    if (data["start_datetime"] >= data["end_datetime"]):
        raise Exception(
            "La réservation doit commencer avant qu'elle se finisse")


def validate_datetime(date_str, time_str):
    valid_time = [11, 17]
    date_ = date.fromisoformat(date_str)
    time_ = time(hour=int(time_str))
    if time_.hour not in valid_time:
        raise Exception()
    return datetime.combine(date_, time_)


def check_if_has_events(data):
    locations = get_events(os.getenv("CALENDAR_LOCATIONS"),
                           data["start_datetime"], data["end_datetime"])
    seances = get_events(os.getenv("CALENDAR_SEANCES"),
                         data["start_datetime"], data["end_datetime"])

    total = locations + seances
    if len(total) > 1:
        msg = f"Le chalet a déjà {len(total)} réservations dans la période sélectionnée"
        raise Exception(msg)
    if len(total) == 1:
        l = total[0]
        format = "%d.%m.%Y %Hh"
        start = datetime.fromisoformat(l["start"]["dateTime"]).strftime(format)
        end = datetime.fromisoformat(l["end"]["dateTime"]).strftime(format)
        raise Exception(f"Le chalet déjà reservé du {start} à {end}")
