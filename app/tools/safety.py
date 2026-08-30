def calculate_safety_risk(
    wave_height,
    wind_speed,
    wind_gusts,
    swell_height,
):
    """
    Deterministic marine safety risk assessment.

    Returns:
        risk_level: LOW / MODERATE / HIGH
        reasons: list of factors contributing to the risk
    """

    risk_score = 0
    reasons = []

    # --------------------------------
    # WAVE HEIGHT
    # --------------------------------

    if wave_height != "N/A":

        if wave_height >= 2.5:
            risk_score += 4
            reasons.append(
                f"Very high wave height ({wave_height} m)"
            )

        elif wave_height >= 1.5:
            risk_score += 3
            reasons.append(
                f"High wave height ({wave_height} m)"
            )

        elif wave_height >= 1.0:
            risk_score += 2
            reasons.append(
                f"Moderate wave height ({wave_height} m)"
            )

        elif wave_height >= 0.5:
            risk_score += 1
            reasons.append(
                f"Noticeable wave height ({wave_height} m)"
            )

    # --------------------------------
    # WIND SPEED
    # --------------------------------

    if wind_speed != "N/A":

        if wind_speed >= 40:
            risk_score += 4
            reasons.append(
                f"Very strong wind ({wind_speed} km/h)"
            )

        elif wind_speed >= 30:
            risk_score += 3
            reasons.append(
                f"Strong wind ({wind_speed} km/h)"
            )

        elif wind_speed >= 20:
            risk_score += 2
            reasons.append(
                f"Moderate-to-strong wind ({wind_speed} km/h)"
            )

        elif wind_speed >= 10:
            risk_score += 1
            reasons.append(
                f"Moderate wind ({wind_speed} km/h)"
            )

    # --------------------------------
    # WIND GUSTS
    # --------------------------------

    if wind_gusts != "N/A":

        if wind_gusts >= 60:
            risk_score += 4
            reasons.append(
                f"Very strong wind gusts ({wind_gusts} km/h)"
            )

        elif wind_gusts >= 45:
            risk_score += 3
            reasons.append(
                f"Strong wind gusts ({wind_gusts} km/h)"
            )

        elif wind_gusts >= 30:
            risk_score += 2
            reasons.append(
                f"Significant wind gusts ({wind_gusts} km/h)"
            )

        elif wind_gusts >= 20:
            risk_score += 1
            reasons.append(
                f"Noticeable wind gusts ({wind_gusts} km/h)"
            )

    # --------------------------------
    # SWELL HEIGHT
    # --------------------------------

    if swell_height != "N/A":

        if swell_height >= 2.5:
            risk_score += 3
            reasons.append(
                f"Very high swell ({swell_height} m)"
            )

        elif swell_height >= 1.5:
            risk_score += 2
            reasons.append(
                f"High swell ({swell_height} m)"
            )

        elif swell_height >= 1.0:
            risk_score += 1
            reasons.append(
                f"Noticeable swell ({swell_height} m)"
            )

    # --------------------------------
    # FINAL RISK LEVEL
    # --------------------------------

    if risk_score >= 7:
        risk_level = "HIGH"

    elif risk_score >= 3:
        risk_level = "MODERATE"

    else:
        risk_level = "LOW"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "reasons": reasons,
    }