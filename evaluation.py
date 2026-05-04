def check_has_citations(answer):
    citation_markers = ["[", "]", "page", ".pdf", ".txt", ".md"]

    return any(marker in answer.lower() for marker in citation_markers)


def check_not_empty(answer):
    return bool(answer and len(answer.strip()) > 50)


def check_has_structure(answer):
    structure_markers = ["#", "##", "1.", "2.", "-", "**"]

    return any(marker in answer for marker in structure_markers)


def evaluate_response(answer):
    results = {
        "Has citations": check_has_citations(answer),
        "Not empty": check_not_empty(answer),
        "Structured output": check_has_structure(answer),
    }

    score = sum(results.values())
    total = len(results)

    return {
        "score": score,
        "total": total,
        "results": results
    }