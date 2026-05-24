from .ai_input_builder import build_ai_input
from .calculations import calculate_lagna, calculate_graha_positions, graha_house_map
from .rules import graha_score, house_score, final_interpretation
from .report_ai import generate_report
from .config import HOUSES

def run_engine_from_user_info(
    name: str,
    date: str,
    time: str,
    place: str,
    question: str = ""
) -> dict:
    ai_input = build_ai_input(name, date, time, place, question)

    lagna = calculate_lagna(
        ai_input["date"],
        ai_input["time"],
        ai_input["place"]
    )

    graha_positions = calculate_graha_positions(
        ai_input["date"],
        ai_input["time"],
        ai_input["place"]
    )

    house_map = graha_house_map(graha_positions)

    graha_scores = {}
    for graha, house in graha_positions.items():
        graha_scores[graha] = graha_score(graha, house, lagna)

    house_scores = {}
    for house in HOUSES:
        house_scores[house] = house_score(
            house=house,
            grahas=house_map.get(house, []),
            event_type=ai_input["event_type"]
        )

    total_score = sum(graha_scores.values()) + sum(house_scores.values())

    result = {
        "name": ai_input["name"],
        "date": ai_input["date"],
        "time": ai_input["time"],
        "place": ai_input["place"],
        "question": ai_input["question"],
        "event_type": ai_input["event_type"],
        "lagna": lagna,
        "graha_positions": graha_positions,
        "house_map": house_map,
        "graha_scores": graha_scores,
        "house_scores": house_scores,
        "total_score": total_score,
        "result": final_interpretation(total_score)
    }

    result["ai_report"] = generate_report(result)
    return result
