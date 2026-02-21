from typing import Dict, Any

RISK_LEVELS = {
    "LOW": (0, 25),
    "MODERATE": (26, 50),
    "HIGH": (51, 75),
    "CRITICAL": (76, 100)
}

def classify_risk(score: float) -> str:
    """Classify risk score into level"""
    for level, (min_score, max_score) in RISK_LEVELS.items():
        if min_score <= score <= max_score:
            return level
    return "UNKNOWN"

def get_risk_color(level: str) -> str:
    """Get color for risk level"""
    colors = {
        "LOW": "#10b981",      # Green
        "MODERATE": "#f59e0b",  # Amber
        "HIGH": "#f97316",      # Orange
        "CRITICAL": "#ef4444",  # Red
        "UNKNOWN": "#6b7280"    # Gray
    }
    return colors.get(level, "#6b7280")