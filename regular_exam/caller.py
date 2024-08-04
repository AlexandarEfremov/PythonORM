import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Sum, F, Avg
from main_app.models import Astronaut, Mission, Spacecraft


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronaut = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by("name")

    if not astronaut:
        return ""

    ast_info = []

    for a in astronaut:
        ast_info.append(f"Astronaut: {a.name}, "
                        f"phone number: {a.phone_number}, "
                        f"status: {'Active' if a.is_active else 'Inactive'}")

    return "\n".join(ast_info)


def get_top_astronaut():
    astronaut = Astronaut.objects.annotate(most_mis=Count("missions")).order_by("-most_mis", "phone_number").first()

    if not astronaut or astronaut.most_mis == 0:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.most_mis} missions."


def get_top_commander():
    commander = Astronaut.objects.annotate(most_command=Count("mission_commander")).order_by(
        "-most_command",
        "phone_number"
    ).first()

    if not commander or commander.most_command == 0:
        return "No data."

    return f"Top Commander: {commander.name} with {commander.most_command} commanded missions."


def get_last_completed_mission():
    last_mission = Mission.objects.filter(status="Completed").annotate(
        tot_sw=Sum("astronauts__spacewalks")
    ).order_by("-launch_date").first()

    if not last_mission:
        return "No data."

    commander = last_mission.commander.name if last_mission.commander else 'TBA'
    astronauts = ', '.join(a.name for a in last_mission.astronauts.all().order_by("name"))

    total_spacewalks = last_mission.tot_sw if last_mission.tot_sw else 0

    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {commander}. "
            f"Astronauts: {astronauts}. "
            f"Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(mis=Count("missions")).order_by("-mis", "name").first()

    if not spacecraft or spacecraft.mis == 0:
        return "No data."

    # total_missions = spacecraft.mis if spacecraft.mis > 0 else 0
    total_astronauts = Astronaut.objects.filter(missions__spacecraft=spacecraft).distinct().count()

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.mis} missions, astronauts on missions: {total_astronauts}.")


def decrease_spacecrafts_weight():

    spacecraft = Spacecraft.objects.filter(missions__status="Planned", weight__gte=200.0).distinct()

    count_of_spacecrafts = spacecraft.count()

    if count_of_spacecrafts == 0:
        return "No changes in weight."

    spacecraft.update(weight=F('weight') - 200.0)

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {count_of_spacecrafts} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")


