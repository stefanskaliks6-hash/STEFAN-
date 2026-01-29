"""Utilities for building a student housing research brief."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Mapping


@dataclass(frozen=True)
class HousingProfile:
    university: str
    city: str
    budget_range: str
    move_in_date: str
    duration_months: int
    roommates: str
    transportation: str
    pets: str
    accessibility: str
    safety_notes: str
    preferences: tuple[str, ...]


def _normalize_preferences(preferences: Iterable[str] | None) -> tuple[str, ...]:
    if not preferences:
        return tuple()
    return tuple(pref.strip() for pref in preferences if pref and pref.strip())


def build_profile(payload: Mapping[str, object]) -> HousingProfile:
    preferences = _normalize_preferences(payload.get("preferences"))
    return HousingProfile(
        university=str(payload.get("university", "")),
        city=str(payload.get("city", "")),
        budget_range=str(payload.get("budget_range", "")),
        move_in_date=str(payload.get("move_in_date", "")),
        duration_months=int(payload.get("duration_months", 0)),
        roommates=str(payload.get("roommates", "")),
        transportation=str(payload.get("transportation", "")),
        pets=str(payload.get("pets", "")),
        accessibility=str(payload.get("accessibility", "")),
        safety_notes=str(payload.get("safety_notes", "")),
        preferences=preferences,
    )


def build_housing_brief(profile: HousingProfile) -> str:
    """Return a structured brief template tailored to the student housing request."""
    today = date.today().isoformat()
    preference_block = (
        "\n".join(f"- {item}" for item in profile.preferences)
        if profile.preferences
        else "- None listed"
    )
    return """Student Housing Accelerator Brief
Generated: {today}

Student Context
- University: {university}
- City/Region: {city}
- Target budget: {budget_range}
- Move-in date: {move_in_date}
- Lease length: {duration_months} months
- Roommates: {roommates}
- Transportation: {transportation}
- Pets: {pets}
- Accessibility needs: {accessibility}
- Safety priorities: {safety_notes}

Core Preferences
{preference_block}

Research Checklist
1. Availability & timing
   - Confirm occupancy dates, waitlists, and sublet options.
   - Note move-in incentives or prorated pricing.
2. Pricing & fees
   - Verify base rent, utilities, deposits, parking, and renter's insurance.
   - Track required fees (application, admin, furniture, amenity).
3. Location & commute
   - Map distance to campus, transit, and bike routes.
   - Note grocery, pharmacy, and late-night dining proximity.
4. Building quality & amenities
   - Evaluate security access, maintenance response, and common areas.
   - Confirm in-unit laundry, internet speed, and furnished options.
5. Lease terms & policies
   - Check guarantor requirements, renewal terms, and early termination clauses.
   - Document sublet and roommate change policies.
6. Safety & neighborhood context
   - Review lighting, crime reports, and student feedback.
   - Flag emergency services access and safe-walk programs.
7. Application strategy
   - Compare acceptance timelines, documentation needs, and competition.
   - Prepare a checklist of required documents.

High-Impact Questions to Ask Leasing Teams
- What is the full monthly cost including utilities and mandatory fees?
- Are there student discounts, referral credits, or short-term lease options?
- How are maintenance requests handled, and what is the average response time?
- What security measures are in place (key fob access, cameras, patrols)?
- What are the exact move-in requirements and deadlines?

Next Steps
- Shortlist 3-5 properties matching the profile.
- Schedule tours and request sample leases.
- Compare total cost of ownership in a simple spreadsheet.
""".format(
        today=today,
        university=profile.university or "(provide)",
        city=profile.city or "(provide)",
        budget_range=profile.budget_range or "(provide)",
        move_in_date=profile.move_in_date or "(provide)",
        duration_months=profile.duration_months or 0,
        roommates=profile.roommates or "(provide)",
        transportation=profile.transportation or "(provide)",
        pets=profile.pets or "(provide)",
        accessibility=profile.accessibility or "(provide)",
        safety_notes=profile.safety_notes or "(provide)",
        preference_block=preference_block,
    )
