"""
game.py

THE MISSING NECKLACE — A Detective Mystery Investigation
A single-file Python + Tkinter desktop mystery game.

Run with:
    python game.py

No external dependencies beyond the Python standard library.
"""

import json
import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox


# =============================================================================
# SECTION 1: STATIC CASE DATA
# =============================================================================

QUESTIONS = [
    {"id": "q_alibi", "text": "Where were you at 10:30 PM, when the necklace disappeared?"},
    {"id": "q_study", "text": "Did you enter the study at any point this evening?"},
    {"id": "q_lastseen", "text": "When did you last see the necklace?"},
    {"id": "q_suspect", "text": "Who do you suspect, and why?"},
    {"id": "q_unusual", "text": "Did you notice anything unusual tonight?"},
    {"id": "q_key", "text": "Do you know anything about the missing spare key?"},
]

SUSPECTS_DATA = [
    {
        "id": "edmund", "name": "Edmund Blackwood", "age": 62,
        "occupation": "Mansion Owner", "relationship": "Owner of the necklace",
        "personality": "Proud, controlling, and deeply image-conscious.",
        "motive": "He recently insured the necklace for a very large sum, just two weeks before it vanished.",
        "alibi": "Says he was in the Living Room greeting guests the entire evening.",
        "base_suspicion": 15,
        "answers": {
            "q_alibi": ("I was right here in the Living Room the entire time, surrounded by my guests. Ask any of them.", True),
            "q_study": ("Why would I need to enter my own study? I have nothing to hide in there.", True),
            "q_lastseen": ("I saw it gleaming in its case just before dinner, around 9:25.", True),
            "q_suspect": ("I hate to say it, but Richard has seemed different lately. Distracted. Nervous.", True),
            "q_unusual": ("The lights flickered oddly around 10:20. That's never happened before.", True),
            "q_key": ("There is only one spare key, kept in my desk drawer. Or... there was.", True),
        },
    },
    {
        "id": "isabelle", "name": "Isabelle Blackwood", "age": 29,
        "occupation": "Art Student", "relationship": "Edmund's daughter",
        "personality": "Rebellious and resentful of her father's control.",
        "motive": "Deep in debt from student loans and a struggling gallery project; has argued with Edmund about money before.",
        "alibi": "Claims she was in her Bedroom on a phone call with her boyfriend from 10:05 to 10:41 PM.",
        "base_suspicion": 30,
        "answers": {
            "q_alibi": ("I was on the phone with my boyfriend, in my room, from about ten past ten until nearly a quarter to eleven.", True),
            "q_study": ("No. I try to avoid Father's study whenever I can.", True),
            "q_lastseen": ("At dinner, same as everyone else.", True),
            "q_suspect": ("Honestly? Richard gives me a bad feeling. Always has.", True),
            "q_unusual": ("I heard the lights flicker, and later someone hurrying down the hall, but I didn't look.", True),
            "q_key": ("Father is paranoid about that key. I don't know where he keeps it, and I don't care to.", True),
        },
    },
    {
        "id": "richard", "name": "Richard Voss", "age": 45,
        "occupation": "Business Partner", "relationship": "Edmund's partner in their antiques trading firm",
        "personality": "Charming and smooth-talking, secretly desperate.",
        "motive": "Owes a massive gambling debt, and an upcoming financial audit is about to expose money he has quietly borrowed from the firm.",
        "alibi": "Claims he stepped into the Garden for fresh air from 10:10 PM to 10:30 PM, and never left it.",
        "base_suspicion": 20,
        "answers": {
            "q_alibi": ("I stepped out to the garden for some air around ten and stayed there until the commotion started. Needed to clear my head.", False),
            "q_study": ("No, never. That's Edmund's private room, I wouldn't dream of it.", False),
            "q_lastseen": ("At dinner, like everyone. Beautiful piece.", True),
            "q_suspect": ("I'd hate to point fingers. Maybe someone from outside got in.", False),
            "q_unusual": ("The power flickered. Old wiring, probably.", True),
            "q_key": ("Key? I wouldn't know the first thing about it.", False),
        },
    },
    {
        "id": "clara", "name": "Clara Whitfield", "age": 55,
        "occupation": "Antique Appraiser",
        "relationship": "Longtime family friend, hired to appraise the collection for a museum donation",
        "personality": "Meticulous, observant, with a dry wit.",
        "motive": "Would have earned a substantial commission from the museum donation, now jeopardized by the theft.",
        "alibi": "Was examining a set of paintings in the Living Room the entire evening, confirmed by Edmund and other guests.",
        "base_suspicion": 5,
        "answers": {
            "q_alibi": ("I was in the Living Room the whole evening, cataloguing the paintings. Edmund can confirm it.", True),
            "q_study": ("Only earlier, before dinner, to look over the necklace for the appraisal.", True),
            "q_lastseen": ("I examined it closely before dinner. Museum-grade piece, flawless.", True),
            "q_suspect": ("I try not to speculate, but that cabinet lock didn't look right to me when I glanced at it later.", True),
            "q_unusual": ("If you want my professional opinion: that lock was picked, not smashed. The scratch pattern is all wrong for force.", True),
            "q_key": ("Edmund mentioned a spare key exists, kept close, for emergencies.", True),
        },
    },
    {
        "id": "margaret", "name": "Margaret Doyle", "age": 50,
        "occupation": "Housekeeper", "relationship": "Has worked for the Blackwood family for over twenty years",
        "personality": "Loyal, sharp-eyed, and quietly protective of the family.",
        "motive": "None apparent. Deeply devoted to the household.",
        "alibi": "Was in the Kitchen preparing late refreshments for most of the evening.",
        "base_suspicion": 5,
        "answers": {
            "q_alibi": ("In the kitchen, preparing coffee and refreshments for the guests, as usual.", True),
            "q_study": ("No, not tonight. I had my hands full in the kitchen.", True),
            "q_lastseen": ("I don't make a habit of admiring the family's jewelry, dear.", True),
            "q_suspect": ("I don't like to gossip, but I did see Mr. Voss hurrying down the hall toward the study around a quarter past ten.", True),
            "q_unusual": ("I heard quick footsteps near the pantry, then the back door, around ten-sixteen or so.", True),
            "q_key": ("Mr. Blackwood keeps a spare in his desk. He's mentioned it before.", True),
        },
    },
    {
        "id": "thomas", "name": "Thomas Reyes", "age": 33,
        "occupation": "Security Guard", "relationship": "Hired for the evening's private gathering",
        "personality": "Diligent but anxious, terrified of losing his job over this.",
        "motive": "None apparent, though he fears being blamed for the security lapse.",
        "alibi": "Was monitoring the security room, except for a brief restroom break from 10:17 to 10:22 PM.",
        "base_suspicion": 10,
        "answers": {
            "q_alibi": ("In the security room, mostly. I stepped away briefly around 10:17, maybe five minutes.", True),
            "q_study": ("No, I stayed near the security room and the main hall all night.", True),
            "q_lastseen": ("I only saw it on the monitors, in its case.", True),
            "q_suspect": ("I really couldn't say. I just don't want to be blamed for this.", True),
            "q_unusual": ("One of the hallway cameras dropped offline for a while. I assumed it was a glitch, but it was a manual override, not a malfunction.", True),
            "q_key": ("That's not something I'd have access to. That's a family matter.", True),
        },
    },
]

LOCATIONS_DATA = [
    {"id": "main_hall", "name": "Main Hall", "icon": "H",
     "description": "The grand entrance hall, with a sweeping staircase and the security monitor station tucked behind the coat room.",
     "evidence_ids": ["security_log"]},
    {"id": "living_room", "name": "Living Room", "icon": "L",
     "description": "Where most guests gathered for drinks and conversation before and after dinner.",
     "evidence_ids": ["clock_discrepancy", "family_photo"]},
    {"id": "study", "name": "Study", "icon": "S",
     "description": "Edmund's private study, home to the locked glass display cabinet where the necklace was kept.",
     "evidence_ids": ["broken_lock", "missing_key", "muddy_footprint", "strange_note"]},
    {"id": "bedroom", "name": "Isabelle's Bedroom", "icon": "B",
     "description": "Isabelle's private room upstairs, where she says she spent much of the evening.",
     "evidence_ids": ["phone_record"]},
    {"id": "kitchen", "name": "Kitchen", "icon": "K",
     "description": "The busy kitchen, where Margaret spent the evening preparing refreshments.",
     "evidence_ids": ["witness_statement", "missing_cloth", "suspicious_movement"]},
    {"id": "garden", "name": "Garden", "icon": "G",
     "description": "The dark garden behind the mansion, bordered by tall hedges and flowerbeds.",
     "evidence_ids": ["disturbed_flowerbed", "hidden_lockpick", "torn_fabric"]},
]

EVIDENCE_DATA = [
    {"id": "broken_lock", "name": "Broken Cabinet Lock", "location_id": "study", "importance": "high",
     "related_suspects": ["richard"], "description": "The glass cabinet's lock is damaged.",
     "flavor": "Looking closely, the damage doesn't look like a violent break-in. There are fine scratch marks around the keyhole, consistent with careful lock-picking rather than force."},
    {"id": "missing_key", "name": "Missing Cabinet Key", "location_id": "study", "importance": "high",
     "related_suspects": ["edmund", "richard"], "description": "The cabinet's spare key, normally kept in Edmund's desk drawer, is gone.",
     "flavor": "The drawer where the spare key was kept is unlocked and empty. Whoever took it knew exactly where to look."},
    {"id": "muddy_footprint", "name": "Muddy Footprint", "location_id": "study", "importance": "medium",
     "related_suspects": ["richard"], "description": "A muddy footprint near the cabinet, tracked in from outside.",
     "flavor": "The mud is reddish and slightly clay-like, unusual for this part of the house. It looks like it came from somewhere with recently turned soil."},
    {"id": "strange_note", "name": "Strange Handwritten Note", "location_id": "study", "importance": "high",
     "related_suspects": ["richard"], "description": "A crumpled note, half-hidden in the study's wastebasket.",
     "flavor": "The note reads: Debt due Friday. No more extensions. Come see me. Signed R.V. The initials match Richard Voss."},
    {"id": "disturbed_flowerbed", "name": "Disturbed Flowerbed", "location_id": "garden", "importance": "medium",
     "related_suspects": ["richard"], "description": "The soil near one of the flowerbeds has been recently disturbed.",
     "flavor": "The reddish clay soil here matches the mud found tracked into the study almost exactly."},
    {"id": "hidden_lockpick", "name": "Hidden Pry Tool", "location_id": "garden", "importance": "high",
     "related_suspects": ["richard"], "description": "A small metal pry tool, hidden beneath an overturned flowerpot.",
     "flavor": "It's a thin, precise tool, the kind used by antique dealers to gently work old locks, not to force them. Its tip matches the scratch marks on the cabinet lock exactly."},
    {"id": "torn_fabric", "name": "Torn Piece of Fabric", "location_id": "garden", "importance": "high",
     "related_suspects": ["richard"], "description": "A scrap of dark fabric snagged on the garden hedge.",
     "flavor": "The fabric is a fine wool blend, the kind used in expensive tailored jackets. It looks freshly torn."},
    {"id": "witness_statement", "name": "Margaret's Witness Statement", "location_id": "kitchen", "importance": "high",
     "related_suspects": ["richard", "margaret"], "description": "Margaret recalls seeing someone hurrying toward the study.",
     "flavor": "Margaret is fairly certain she saw Richard heading quickly toward the study hallway around 10:15 PM, well before the theft was discovered."},
    {"id": "missing_cloth", "name": "Missing Cleaning Cloth", "location_id": "kitchen", "importance": "low",
     "related_suspects": [], "description": "One of the kitchen's cleaning cloths is missing from its usual hook.",
     "flavor": "After some checking, this turns out to be unrelated. Margaret remembers using it earlier to mop up a spilled drink and simply misplacing it."},
    {"id": "suspicious_movement", "name": "Suspicious Movement", "location_id": "kitchen", "importance": "medium",
     "related_suspects": ["richard"], "description": "Margaret mentions hearing hurried footsteps near the pantry.",
     "flavor": "She recalls the footsteps moving from the pantry toward the back door, roughly the same time she saw Richard head toward the study, suggesting he circled back through the house."},
    {"id": "clock_discrepancy", "name": "Clock Discrepancy", "location_id": "living_room", "importance": "medium",
     "related_suspects": [], "description": "The antique grandfather clock in the Living Room seems off.",
     "flavor": "The clock runs about ten minutes fast. Anyone timing events off this clock alone would be slightly mistaken, worth remembering when checking alibis."},
    {"id": "family_photo", "name": "Old Family Photo", "location_id": "living_room", "importance": "low",
     "related_suspects": ["isabelle"], "description": "A framed photo of Edmund and Isabelle, with a torn corner.",
     "flavor": "Interesting, but after some thought, this seems to be nothing more than old family history, unrelated to tonight's theft."},
    {"id": "phone_record", "name": "Phone Record", "location_id": "bedroom", "importance": "high",
     "related_suspects": ["richard"], "description": "A phone record left on a side table shows a recent call.",
     "flavor": "A call was placed to a known pawnbroker at 10:35 PM, just minutes after the theft was discovered. The number belongs to Richard's phone."},
    {"id": "security_log", "name": "Security Log", "location_id": "main_hall", "importance": "high",
     "related_suspects": ["richard", "thomas"], "description": "The mansion's security log, showing camera activity for the evening.",
     "flavor": "The study hallway camera went offline from 10:18 PM to 10:30 PM due to a manual override, not a malfunction. Whoever did this knew the system's override code."},
]

TIMELINE_DATA = [
    {"id": "t1", "time": "9:00 PM", "description": "Guests arrive at Blackwood Manor for the private gathering.", "note": ""},
    {"id": "t2", "time": "9:30 PM", "description": "Dinner begins in the main dining room.", "note": ""},
    {"id": "t3", "time": "10:00 PM", "description": "Guests separate after dinner, mingling throughout the mansion.", "note": ""},
    {"id": "t4", "time": "10:15 PM", "description": "Margaret sees someone hurrying toward the study hallway.",
     "note": "Compare with Richard's stated alibi for this time."},
    {"id": "t5", "time": "10:18 PM", "description": "The study hallway security camera goes offline for twelve minutes.",
     "note": "This was a manual override, not a malfunction."},
    {"id": "t6", "time": "10:20 PM", "description": "A brief power interruption affects the east wing lighting.", "note": ""},
    {"id": "t7", "time": "10:30 PM", "description": "The necklace is found missing from the locked cabinet.", "note": ""},
    {"id": "t8", "time": "10:35 PM", "description": "A call is placed from within the house to a known pawnbroker.", "note": ""},
    {"id": "t9", "time": "10:45 PM", "description": "The theft is formally discovered and announced to the household.", "note": ""},
]

DEDUCTIONS_DATA = [
    {"id": "d1", "evidence_a": "broken_lock", "evidence_b": "missing_key",
     "result_text": "The cabinet wasn't smashed open at all. Someone used the missing spare key, then damaged the lock afterward to make it look like a break-in. This was an inside job.",
     "target_suspect": "richard", "suspicion_delta": 15, "score_points": 20},
    {"id": "d2", "evidence_a": "witness_statement", "evidence_b": "security_log",
     "result_text": "Margaret saw Richard heading toward the study at almost the exact moment the hallway camera conveniently went offline. That is not a coincidence.",
     "target_suspect": "richard", "suspicion_delta": 20, "score_points": 25},
    {"id": "d3", "evidence_a": "muddy_footprint", "evidence_b": "disturbed_flowerbed",
     "result_text": "The reddish mud tracked into the study matches the freshly disturbed soil in the garden almost perfectly. Someone walked directly from one to the other.",
     "target_suspect": "richard", "suspicion_delta": 10, "score_points": 15},
    {"id": "d4", "evidence_a": "torn_fabric", "evidence_b": "suspicious_movement",
     "result_text": "The torn fabric on the garden hedge lines up with the path Margaret heard footsteps take, from the pantry, out the back door, and into the garden.",
     "target_suspect": "richard", "suspicion_delta": 10, "score_points": 15},
    {"id": "d5", "evidence_a": "strange_note", "evidence_b": "phone_record",
     "result_text": "The note about a debt due Friday and the late-night call to a known pawnbroker paint a very clear picture of financial desperation, and a plan already in motion.",
     "target_suspect": "richard", "suspicion_delta": 20, "score_points": 25},
    {"id": "d6", "evidence_a": "hidden_lockpick", "evidence_b": "broken_lock",
     "result_text": "The precise pry tool hidden in the garden matches the scratch marks on the cabinet lock exactly. This is very likely the tool that was used.",
     "target_suspect": "richard", "suspicion_delta": 15, "score_points": 20},
    {"id": "d7", "evidence_a": "clock_discrepancy", "evidence_b": "witness_statement",
     "result_text": "Even accounting for the fast-running clock, the timing still places Richard near the study at the critical moment. The discrepancy doesn't clear him.",
     "target_suspect": "richard", "suspicion_delta": 5, "score_points": 10},
    {"id": "d8", "evidence_a": "family_photo", "evidence_b": "missing_cloth",
     "result_text": "Neither the old photo nor the missing cloth turn out to be connected to tonight's theft, just ordinary household clutter. Still, ruling them out narrows the case.",
     "target_suspect": "isabelle", "suspicion_delta": -10, "score_points": 5},
]

CORRECT_SUSPECT_ID = "richard"
CORRECT_METHOD_ID = "duplicate_key"
STRONG_EVIDENCE_IDS = {"security_log", "witness_statement", "hidden_lockpick", "strange_note", "phone_record"}

ACCUSATION_METHODS = [
    {"id": "forced_entry", "text": "He forced the cabinet open by smashing the lock."},
    {"id": "duplicate_key", "text": "He used a hidden spare key to unlock the cabinet, staged the lock damage, and disabled the camera to cover his tracks."},
    {"id": "window_entry", "text": "He climbed in from outside through a window."},
    {"id": "accomplice", "text": "He had an accomplice let him in through the kitchen."},
]

MIN_EVIDENCE_FOR_ACCUSATION = 3

RANK_THRESHOLDS = [
    (500, "Master Detective"),
    (350, "Senior Detective"),
    (220, "Skilled Investigator"),
    (100, "Junior Investigator"),
    (0, "Novice Detective"),
]

OUTCOME_BONUSES = {
    "PERFECT_SOLUTION": 200,
    "SUCCESSFUL_INVESTIGATION": 120,
    "CORRECT_SUSPECT_WRONG_METHOD": 80,
    "INSUFFICIENT_EVIDENCE": -30,
    "WRONG_ACCUSATION": -100,
}

OUTCOME_TITLES = {
    "PERFECT_SOLUTION": "PERFECT SOLUTION",
    "SUCCESSFUL_INVESTIGATION": "SUCCESSFUL INVESTIGATION",
    "CORRECT_SUSPECT_WRONG_METHOD": "CORRECT SUSPECT, WRONG EXPLANATION",
    "INSUFFICIENT_EVIDENCE": "INSUFFICIENT EVIDENCE",
    "WRONG_ACCUSATION": "WRONG ACCUSATION",
}

OUTCOME_NARRATIVES = {
    "PERFECT_SOLUTION": (
        "You lay out the case piece by piece: the picked lock, the missing key, the muddy trail "
        "to the garden, the camera conveniently disabled at the crucial moment, and the debt that "
        "started it all. Richard's composure finally cracks. He admits he was going to pay it back "
        "before anyone even noticed it was gone. Edmund sits down heavily, more hurt than surprised. "
        "The necklace is recovered from a locker at the pawnbroker's the next morning."
    ),
    "SUCCESSFUL_INVESTIGATION": (
        "You correctly name Richard as the thief, and your explanation of how he did it holds up, "
        "though your case leans on thinner evidence than it could have. Under gentle pressure, Richard "
        "admits everything. The necklace is recovered, but you can't help feeling you left a few threads "
        "hanging."
    ),
    "CORRECT_SUSPECT_WRONG_METHOD": (
        "You correctly identify Richard as the culprit, and confronted with your accusation, he eventually "
        "confesses. But your theory of exactly how he pulled it off doesn't quite match what really happened, "
        "and it takes him gently correcting you before the full picture falls into place."
    ),
    "INSUFFICIENT_EVIDENCE": (
        "You make your accusation, but without enough evidence behind it, it falls flat. Edmund looks at you "
        "with polite disappointment, noting that's quite an accusation for so little proof. You'll need "
        "to investigate further before anyone will take this seriously."
    ),
    "WRONG_ACCUSATION": (
        "The room goes uncomfortably silent as you make your accusation. The accused suspect stares at you in "
        "disbelief, and after a tense moment, Edmund clears his throat, saying he thinks you've made a serious "
        "mistake, detective. Somewhere in the house, the real thief quietly breathes a sigh of relief."
    ),
}

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savegame.json")
# =============================================================================
# SECTION 2: DATA MODELS
# =============================================================================

class Suspect:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.age = data["age"]
        self.occupation = data["occupation"]
        self.relationship = data["relationship"]
        self.personality = data["personality"]
        self.motive = data["motive"]
        self.alibi = data["alibi"]
        self.base_suspicion = data.get("base_suspicion", 0)
        self.answers = data.get("answers", {})

    def answer_for(self, question_id):
        entry = self.answers.get(question_id)
        if entry is None:
            return "I have nothing more to say about that.", True
        return entry[0], entry[1]


class Evidence:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.location_id = data["location_id"]
        self.importance = data.get("importance", "medium")
        self.related_suspects = data.get("related_suspects", [])
        self.description = data.get("description", "")
        self.flavor = data.get("flavor", "")


class Location:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.icon = data.get("icon", "?")
        self.description = data.get("description", "")
        self.evidence_ids = data.get("evidence_ids", [])


class TimelineEvent:
    def __init__(self, data):
        self.id = data["id"]
        self.time = data["time"]
        self.description = data["description"]
        self.note = data.get("note", "")


class Deduction:
    def __init__(self, data):
        self.id = data["id"]
        self.evidence_a = data["evidence_a"]
        self.evidence_b = data["evidence_b"]
        self.result_text = data["result_text"]
        self.target_suspect = data.get("target_suspect")
        self.suspicion_delta = data.get("suspicion_delta", 0)
        self.score_points = data.get("score_points", 0)

    def matches(self, ev_a, ev_b):
        return {ev_a, ev_b} == {self.evidence_a, self.evidence_b}


class CaseNote:
    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {"text": self.text}

    @staticmethod
    def from_dict(data):
        return CaseNote(data.get("text", ""))


class GameData:
    """Loads and holds all static case data (built from the Python
    literals above -- no external files needed)."""

    def __init__(self):
        self.questions = QUESTIONS
        self.suspects = {s["id"]: Suspect(s) for s in SUSPECTS_DATA}
        self.evidence = {e["id"]: Evidence(e) for e in EVIDENCE_DATA}
        self.locations = {l["id"]: Location(l) for l in LOCATIONS_DATA}
        self.timeline = [TimelineEvent(t) for t in TIMELINE_DATA]
        self.deductions = [Deduction(d) for d in DEDUCTIONS_DATA]

    def suspect_list(self):
        return list(self.suspects.values())

    def location_list(self):
        return list(self.locations.values())

    def evidence_for_location(self, location_id):
        loc = self.locations.get(location_id)
        if not loc:
            return []
        return [self.evidence[eid] for eid in loc.evidence_ids if eid in self.evidence]

    def question_text(self, question_id):
        for q in self.questions:
            if q["id"] == question_id:
                return q["text"]
        return "?"


class Investigation:
    """Holds all dynamic per-playthrough state."""

    def __init__(self, suspects):
        self.discovered_evidence = set()
        self.examined_evidence = set()
        self.visited_locations = set()
        self.asked_questions = {s.id: set() for s in suspects}
        self.suspicion = {s.id: s.base_suspicion for s in suspects}
        self.deductions_made = set()
        self.notes = []
        self.score = 0
        self.accusation_made = False
        self.accusation_result = None
        self.final_rank = None

    def discover_evidence(self, evidence_id):
        is_new = evidence_id not in self.discovered_evidence
        self.discovered_evidence.add(evidence_id)
        if is_new:
            self.score += 10
        return is_new

    def examine_evidence(self, evidence_id):
        self.examined_evidence.add(evidence_id)

    def visit_location(self, location_id):
        self.visited_locations.add(location_id)

    def ask_question(self, suspect_id, question_id):
        is_new = question_id not in self.asked_questions.setdefault(suspect_id, set())
        self.asked_questions[suspect_id].add(question_id)
        if is_new:
            self.score += 2
        return is_new

    def adjust_suspicion(self, suspect_id, delta):
        if suspect_id not in self.suspicion:
            return
        self.suspicion[suspect_id] = max(0, min(100, self.suspicion[suspect_id] + delta))

    def register_deduction(self, deduction):
        is_new = deduction.id not in self.deductions_made
        self.deductions_made.add(deduction.id)
        if is_new:
            self.score += deduction.score_points
            if deduction.target_suspect:
                self.adjust_suspicion(deduction.target_suspect, deduction.suspicion_delta)
        return is_new

    def add_note(self, text):
        self.notes.append(CaseNote(text))

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]

    def to_dict(self):
        return {
            "discovered_evidence": sorted(self.discovered_evidence),
            "examined_evidence": sorted(self.examined_evidence),
            "visited_locations": sorted(self.visited_locations),
            "asked_questions": {k: sorted(v) for k, v in self.asked_questions.items()},
            "suspicion": self.suspicion,
            "deductions_made": sorted(self.deductions_made),
            "notes": [n.to_dict() for n in self.notes],
            "score": self.score,
            "accusation_made": self.accusation_made,
            "accusation_result": self.accusation_result,
            "final_rank": self.final_rank,
        }

    @staticmethod
    def from_dict(data, suspects):
        inv = Investigation(suspects)
        inv.discovered_evidence = set(data.get("discovered_evidence", []))
        inv.examined_evidence = set(data.get("examined_evidence", []))
        inv.visited_locations = set(data.get("visited_locations", []))
        aq = data.get("asked_questions", {})
        inv.asked_questions = {s.id: set(aq.get(s.id, [])) for s in suspects}
        saved_suspicion = data.get("suspicion", {})
        for s in suspects:
            inv.suspicion[s.id] = saved_suspicion.get(s.id, s.base_suspicion)
        inv.deductions_made = set(data.get("deductions_made", []))
        inv.notes = [CaseNote.from_dict(n) for n in data.get("notes", [])]
        inv.score = data.get("score", 0)
        inv.accusation_made = data.get("accusation_made", False)
        inv.accusation_result = data.get("accusation_result")
        inv.final_rank = data.get("final_rank")
        return inv


class SaveManager:
    def __init__(self, save_path=SAVE_FILE):
        self.save_path = save_path

    def save_exists(self):
        return os.path.isfile(self.save_path)

    def save_investigation(self, investigation):
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(investigation.to_dict(), f, indent=2)
            return True
        except (OSError, TypeError, ValueError):
            return False

    def load_investigation(self, suspects):
        if not self.save_exists():
            return None
        try:
            with open(self.save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Investigation.from_dict(data, suspects)
        except (OSError, ValueError, KeyError, TypeError):
            return None


def find_matching_deduction(game_data, evidence_a_id, evidence_b_id):
    for deduction in game_data.deductions:
        if deduction.matches(evidence_a_id, evidence_b_id):
            return deduction
    return None


def evaluate_accusation(investigation, suspect_id, method_id, evidence_id):
    if len(investigation.discovered_evidence) < MIN_EVIDENCE_FOR_ACCUSATION:
        return "INSUFFICIENT_EVIDENCE"
    if suspect_id != CORRECT_SUSPECT_ID:
        return "WRONG_ACCUSATION"
    if method_id != CORRECT_METHOD_ID:
        return "CORRECT_SUSPECT_WRONG_METHOD"
    if evidence_id in STRONG_EVIDENCE_IDS:
        return "PERFECT_SOLUTION"
    return "SUCCESSFUL_INVESTIGATION"


def finalize_score(investigation, outcome_key):
    investigation.score += OUTCOME_BONUSES.get(outcome_key, 0)
    investigation.score = max(0, investigation.score)
    return investigation.score


def rank_for_score(score):
    for threshold, rank in RANK_THRESHOLDS:
        if score >= threshold:
            return rank
    return RANK_THRESHOLDS[-1][1]
# =============================================================================
# SECTION 3: THEME / UI HELPERS
# =============================================================================

BG_DARK = "#12141c"
BG_PANEL = "#1b1e2b"
BG_PANEL_LIGHT = "#242838"
BG_INPUT = "#2c3040"
ACCENT_GOLD = "#c9a24b"
ACCENT_GOLD_DIM = "#8a7440"
ACCENT_RED = "#b0413e"
ACCENT_GREEN = "#5a9a6f"
TEXT_LIGHT = "#e8e6df"
TEXT_MUTED = "#9a9baa"
BORDER = "#3a3f52"


def safe_font(family, size, weight="normal", slant="roman"):
    try:
        return tkfont.Font(family=family, size=size, weight=weight, slant=slant)
    except tk.TclError:
        return tkfont.Font(family="TkDefaultFont", size=size, weight=weight, slant=slant)


def build_fonts():
    return {
        "title": safe_font("Georgia", 30, "bold"),
        "subtitle": safe_font("Georgia", 14, "normal", "italic"),
        "heading": safe_font("Georgia", 18, "bold"),
        "subheading": safe_font("Segoe UI", 13, "bold"),
        "body": safe_font("Segoe UI", 11, "normal"),
        "body_bold": safe_font("Segoe UI", 11, "bold"),
        "small": safe_font("Segoe UI", 9, "normal"),
        "button": safe_font("Segoe UI", 11, "bold"),
    }


def make_panel(parent, **kwargs):
    frame = tk.Frame(parent, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, bd=0)
    frame.configure(**kwargs)
    return frame


def make_title_bar(parent, fonts, text, subtitle=None):
    bar = tk.Frame(parent, bg=BG_DARK)
    tk.Label(bar, text=text, font=fonts["heading"], bg=BG_DARK, fg=ACCENT_GOLD).pack(anchor="w", padx=4, pady=(4, 0))
    if subtitle:
        tk.Label(bar, text=subtitle, font=fonts["small"], bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w", padx=4, pady=(0, 4))
    return bar


class HoverButton(tk.Button):
    def __init__(self, parent, text, command, fonts, bg=ACCENT_GOLD, fg=BG_DARK, hover_bg=None, width=None, **kwargs):
        self._normal_bg = bg
        self._hover_bg = hover_bg or ACCENT_GOLD_DIM
        super().__init__(parent, text=text, command=command, font=fonts.get("button"),
                          bg=bg, fg=fg, activebackground=self._hover_bg, activeforeground=fg,
                          relief="flat", bd=0, padx=14, pady=8, cursor="hand2", width=width, **kwargs)
        self.bind("<Enter>", lambda e: self.configure(bg=self._hover_bg))
        self.bind("<Leave>", lambda e: self.configure(bg=self._normal_bg))


def nav_button(parent, text, command, fonts, danger=False):
    bg = ACCENT_RED if danger else BG_PANEL_LIGHT
    hover = "#c65552" if danger else BORDER
    return HoverButton(parent, text, command, fonts, bg=bg, fg=TEXT_LIGHT, hover_bg=hover)


def suspicion_bar(parent, value, fonts, width=180, height=18):
    canvas = tk.Canvas(parent, width=width, height=height, bg=BG_PANEL_LIGHT,
                        highlightthickness=1, highlightbackground=BORDER)
    value = max(0, min(100, value))
    fill_width = int((value / 100.0) * width)
    if value < 34:
        color, label = ACCENT_GREEN, "LOW"
    elif value < 67:
        color, label = ACCENT_GOLD, "MEDIUM"
    else:
        color, label = ACCENT_RED, "HIGH"
    if fill_width > 0:
        canvas.create_rectangle(0, 0, fill_width, height, fill=color, outline="")
    canvas.create_text(width // 2, height // 2, text=f"{label} ({value})", fill=TEXT_LIGHT, font=fonts.get("small"))
    return canvas


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg=BG_DARK, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=bg)
        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            delta = -1 * int(event.delta / 120) if event.delta else 0
            canvas.yview_scroll(delta, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


IMPORTANCE_COLORS = {"low": TEXT_MUTED, "medium": ACCENT_GOLD, "high": ACCENT_RED}
OUTCOME_COLORS = {
    "PERFECT_SOLUTION": ACCENT_GREEN,
    "SUCCESSFUL_INVESTIGATION": ACCENT_GOLD,
    "CORRECT_SUSPECT_WRONG_METHOD": ACCENT_GOLD,
    "INSUFFICIENT_EVIDENCE": TEXT_MUTED,
    "WRONG_ACCUSATION": ACCENT_RED,
}
# =============================================================================
# SECTION 4: MAIN APPLICATION / FRAME CONTROLLER
# =============================================================================

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Missing Necklace - A Detective Mystery Investigation")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=BG_DARK)

        self.fonts = build_fonts()
        self.game_data = GameData()
        self.save_manager = SaveManager()
        self.investigation = None

        self.container = tk.Frame(self, bg=BG_DARK)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.show_frame(MainMenuFrame)

    def show_frame(self, frame_class, **kwargs):
        if self.current_frame is not None:
            self.current_frame.destroy()
        frame = frame_class(self.container, self, **kwargs)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def start_new_investigation(self):
        self.investigation = Investigation(self.game_data.suspect_list())

    def load_investigation(self):
        loaded = self.save_manager.load_investigation(self.game_data.suspect_list())
        if loaded is not None:
            self.investigation = loaded
            return True
        return False

    def save_current_investigation(self):
        if self.investigation is None:
            return False
        return self.save_manager.save_investigation(self.investigation)
    # =============================================================================
# SECTION 5: MAIN MENU
# =============================================================================

class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts

        center = tk.Frame(self, bg=BG_DARK)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="THE MISSING NECKLACE", font=fonts["title"], bg=BG_DARK, fg=ACCENT_GOLD).pack()
        tk.Label(center, text="A Detective Mystery Investigation", font=fonts["subtitle"],
                 bg=BG_DARK, fg=TEXT_MUTED).pack(pady=(2, 26))

        button_frame = tk.Frame(center, bg=BG_DARK)
        button_frame.pack()

        buttons = [
            ("New Investigation", self.new_investigation),
            ("Load Investigation", self.load_investigation),
            ("How to Play", self.how_to_play),
            ("About", self.about),
            ("Exit", self.exit_game),
        ]
        for text, cmd in buttons:
            HoverButton(button_frame, text, cmd, fonts, width=28).pack(pady=6, ipady=4)

    def new_investigation(self):
        self.controller.start_new_investigation()
        self.controller.show_frame(DashboardFrame)

    def load_investigation(self):
        if self.controller.load_investigation():
            self.controller.show_frame(DashboardFrame)
        else:
            messagebox.showinfo("No Saved Investigation",
                                 "There is no saved investigation to load yet.\n\n"
                                 "Start a New Investigation first, and it will be saveable afterwards.")

    def how_to_play(self):
        messagebox.showinfo("How to Play",
            "Investigate the disappearance of the Blackwood necklace.\n\n"
            "- Visit LOCATIONS to discover evidence.\n"
            "- Interview SUSPECTS and compare their statements.\n"
            "- Review the TIMELINE for the evening's events.\n"
            "- Use DEDUCTIONS to connect two clues and reveal new insights.\n"
            "- Write your theories in CASE NOTES.\n"
            "- Check CASE STATUS to track your progress and score.\n"
            "- When you're confident, make your ACCUSATION.\n\n"
            "Choose the correct suspect, the correct method, and your strongest\n"
            "evidence for the best possible outcome. Good luck, detective.")

    def about(self):
        messagebox.showinfo("About",
            "THE MISSING NECKLACE\n"
            "A Detective Mystery Investigation\n\n"
            "Built with Python and Tkinter.\n"
            "A self-contained desktop mystery game with a logical, predefined solution -- "
            "no randomness, no AI involved in solving the case, just careful detective work.")

    def exit_game(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit the investigation?"):
            self.controller.destroy()
            # =============================================================================
# SECTION 6: DASHBOARD
# =============================================================================

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation

        top_bar = tk.Frame(self, bg=BG_PANEL, height=70)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)
        tk.Label(top_bar, text="Investigation Dashboard", font=fonts["heading"],
                 bg=BG_PANEL, fg=ACCENT_GOLD).pack(side="left", padx=20)
        stats_text = f"Evidence: {len(inv.discovered_evidence)}/{len(controller.game_data.evidence)}    Score: {inv.score}"
        tk.Label(top_bar, text=stats_text, font=fonts["body"], bg=BG_PANEL, fg=TEXT_MUTED).pack(side="right", padx=20)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=30, pady=30)
        tk.Label(body, text="Blackwood Manor awaits your investigation.", font=fonts["subtitle"],
                 bg=BG_DARK, fg=TEXT_MUTED).pack(pady=(0, 20))

        grid = tk.Frame(body, bg=BG_DARK)
        grid.pack()
        sections = [
            ("SUSPECTS", self.open_suspects), ("LOCATIONS", self.open_locations),
            ("EVIDENCE", self.open_evidence), ("TIMELINE", self.open_timeline),
            ("DEDUCTIONS", self.open_deductions), ("CASE NOTES", self.open_notes),
            ("CASE STATUS", self.open_status), ("MAKE ACCUSATION", self.open_accusation),
        ]
        for index, (label, command) in enumerate(sections):
            row, col = divmod(index, 3)
            card = tk.Frame(grid, bg=BG_PANEL, highlightbackground=BORDER, highlightthickness=1, width=220, height=110)
            card.grid(row=row, column=col, padx=12, pady=12)
            card.grid_propagate(False)
            tk.Label(card, text=label, font=fonts["subheading"], bg=BG_PANEL, fg=TEXT_LIGHT,
                     wraplength=190, justify="center").pack(expand=True, pady=(14, 6))
            HoverButton(card, "Open", command, fonts, width=10).pack(pady=(0, 12))

        bottom_bar = tk.Frame(self, bg=BG_PANEL, height=56)
        bottom_bar.pack(fill="x", side="bottom")
        bottom_bar.pack_propagate(False)
        nav_button(bottom_bar, "Save Investigation", self.save_investigation, fonts).pack(side="left", padx=12, pady=10)
        nav_button(bottom_bar, "Reset Investigation", self.reset_investigation, fonts, danger=True).pack(side="left", padx=6, pady=10)
        nav_button(bottom_bar, "Main Menu", self.back_to_main_menu, fonts).pack(side="right", padx=12, pady=10)

    def open_suspects(self): self.controller.show_frame(SuspectListFrame)
    def open_locations(self): self.controller.show_frame(LocationListFrame)
    def open_evidence(self): self.controller.show_frame(EvidenceListFrame)
    def open_timeline(self): self.controller.show_frame(TimelineFrame)
    def open_deductions(self): self.controller.show_frame(DeductionFrame)
    def open_notes(self): self.controller.show_frame(NotesFrame)
    def open_status(self): self.controller.show_frame(CaseStatusFrame)
    def open_accusation(self): self.controller.show_frame(AccusationFrame)

    def save_investigation(self):
        if self.controller.save_current_investigation():
            messagebox.showinfo("Saved", "Your investigation has been saved.")
        else:
            messagebox.showerror("Save Failed", "The investigation could not be saved.")

    def reset_investigation(self):
        if messagebox.askyesno("Reset Investigation",
                                "This will erase all current progress and start a brand new investigation. Continue?"):
            self.controller.start_new_investigation()
            self.controller.show_frame(DashboardFrame)

    def back_to_main_menu(self):
        self.controller.show_frame(MainMenuFrame)
        # =============================================================================
# SECTION 7: SUSPECTS
# =============================================================================

class SuspectListFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation

        make_title_bar(self, fonts, "Suspects", "Select a suspect to view their profile and interview them.").pack(
            fill="x", padx=20, pady=(16, 6))

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for suspect in controller.game_data.suspect_list():
            row = make_panel(scroll.inner)
            row.pack(fill="x", pady=6, padx=4)
            info = tk.Frame(row, bg=BG_PANEL)
            info.pack(side="left", fill="both", expand=True, padx=12, pady=10)
            tk.Label(info, text=suspect.name, font=fonts["subheading"], bg=BG_PANEL, fg=TEXT_LIGHT).pack(anchor="w")
            tk.Label(info, text=f"{suspect.occupation} - {suspect.relationship}", font=fonts["small"],
                     bg=BG_PANEL, fg=TEXT_MUTED).pack(anchor="w")
            asked = len(inv.asked_questions.get(suspect.id, set()))
            total_q = len(controller.game_data.questions)
            tk.Label(info, text=f"Interview progress: {asked}/{total_q}", font=fonts["small"],
                     bg=BG_PANEL, fg=TEXT_MUTED).pack(anchor="w", pady=(4, 0))

            right = tk.Frame(row, bg=BG_PANEL)
            right.pack(side="right", padx=12, pady=10)
            suspicion_bar(right, inv.suspicion.get(suspect.id, 0), fonts).pack(pady=(0, 6))
            HoverButton(right, "View Profile", lambda sid=suspect.id: self.open_profile(sid), fonts, width=14).pack()

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)

    def open_profile(self, suspect_id):
        self.controller.show_frame(SuspectProfileFrame, suspect_id=suspect_id)


class SuspectProfileFrame(tk.Frame):
    def __init__(self, parent, controller, suspect_id):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self.suspect_id = suspect_id
        fonts = controller.fonts
        inv = controller.investigation
        suspect = controller.game_data.suspects[suspect_id]

        make_title_bar(self, fonts, suspect.name, suspect.occupation).pack(fill="x", padx=20, pady=(16, 6))

        body = make_panel(self)
        body.pack(fill="both", expand=True, padx=20, pady=10)
        left = tk.Frame(body, bg=BG_PANEL)
        left.pack(side="left", fill="both", expand=True, padx=20, pady=16)

        def field(label, value):
            tk.Label(left, text=label, font=fonts["body_bold"], bg=BG_PANEL, fg=ACCENT_GOLD).pack(anchor="w", pady=(8, 0))
            tk.Label(left, text=value, font=fonts["body"], bg=BG_PANEL, fg=TEXT_LIGHT,
                     wraplength=480, justify="left").pack(anchor="w")

        field("Name:", suspect.name)
        field("Age:", str(suspect.age))
        field("Occupation:", suspect.occupation)
        field("Relationship:", suspect.relationship)
        field("Personality:", suspect.personality)
        field("Motive:", suspect.motive)
        field("Alibi:", suspect.alibi)

        right = tk.Frame(body, bg=BG_PANEL)
        right.pack(side="right", fill="y", padx=20, pady=16)
        tk.Label(right, text="Current Suspicion:", font=fonts["body_bold"], bg=BG_PANEL, fg=ACCENT_GOLD).pack(anchor="w")
        suspicion_bar(right, inv.suspicion.get(suspect.id, 0), fonts, width=200).pack(pady=(4, 20))
        HoverButton(right, "Interview", self.open_interview, fonts, width=18).pack(pady=6)
        HoverButton(right, "View Statements", self.open_statements, fonts, width=18).pack(pady=6)
        HoverButton(right, "Related Evidence", self.open_related_evidence, fonts, width=18).pack(pady=6)

        nav_button(self, "Back to Suspects", self.back_to_list, fonts).pack(pady=14)

    def open_interview(self):
        self.controller.show_frame(InterviewFrame, suspect_id=self.suspect_id)

    def open_statements(self):
        self.controller.show_frame(StatementsFrame, suspect_id=self.suspect_id)

    def open_related_evidence(self):
        self.controller.show_frame(EvidenceListFrame, filter_suspect_id=self.suspect_id)

    def back_to_list(self):
        self.controller.show_frame(SuspectListFrame)


class InterviewFrame(tk.Frame):
    def __init__(self, parent, controller, suspect_id):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self.suspect_id = suspect_id
        fonts = controller.fonts
        suspect = controller.game_data.suspects[suspect_id]

        make_title_bar(self, fonts, f"Interviewing {suspect.name}", "Choose a question to ask.").pack(
            fill="x", padx=20, pady=(16, 6))

        content = tk.Frame(self, bg=BG_DARK)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        question_panel = make_panel(content)
        question_panel.pack(side="left", fill="y", padx=(0, 10), pady=4)
        tk.Label(question_panel, text="Questions", font=fonts["subheading"], bg=BG_PANEL,
                 fg=ACCENT_GOLD).pack(anchor="w", padx=14, pady=(12, 6))
        for q in controller.game_data.questions:
            HoverButton(question_panel, q["text"], lambda qid=q["id"]: self.ask(qid), fonts, width=32).pack(
                padx=12, pady=4, anchor="w")

        self.answer_panel = make_panel(content)
        self.answer_panel.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=4)
        self.answer_label = tk.Label(self.answer_panel,
            text="Select a question on the left to hear the suspect's response.",
            font=fonts["body"], bg=BG_PANEL, fg=TEXT_MUTED, wraplength=420, justify="left")
        self.answer_label.pack(padx=18, pady=18, anchor="n")

        nav_button(self, "Back to Profile", self.back_to_profile, fonts).pack(pady=14)

    def ask(self, question_id):
        suspect = self.controller.game_data.suspects[self.suspect_id]
        question_text = self.controller.game_data.question_text(question_id)
        answer_text, _truthful = suspect.answer_for(question_id)
        self.controller.investigation.ask_question(self.suspect_id, question_id)
        self.answer_label.configure(text=f"Q: {question_text}\n\n{answer_text}")

    def back_to_profile(self):
        self.controller.show_frame(SuspectProfileFrame, suspect_id=self.suspect_id)


class StatementsFrame(tk.Frame):
    def __init__(self, parent, controller, suspect_id):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self.suspect_id = suspect_id
        fonts = controller.fonts
        inv = controller.investigation
        suspect = controller.game_data.suspects[suspect_id]

        make_title_bar(self, fonts, f"Statements - {suspect.name}",
                       "A record of everything this suspect has told you.").pack(fill="x", padx=20, pady=(16, 6))

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        asked = inv.asked_questions.get(suspect_id, set())
        if not asked:
            tk.Label(scroll.inner, text="You haven't interviewed this suspect yet.", font=fonts["body"],
                     bg=BG_DARK, fg=TEXT_MUTED).pack(pady=20)
        else:
            for q in controller.game_data.questions:
                if q["id"] not in asked:
                    continue
                answer_text, _truthful = suspect.answer_for(q["id"])
                block = make_panel(scroll.inner)
                block.pack(fill="x", pady=6, padx=4)
                tk.Label(block, text=q["text"], font=fonts["body_bold"], bg=BG_PANEL, fg=ACCENT_GOLD,
                         wraplength=700, justify="left").pack(anchor="w", padx=14, pady=(10, 2))
                tk.Label(block, text=answer_text, font=fonts["body"], bg=BG_PANEL, fg=TEXT_LIGHT,
                         wraplength=700, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        nav_button(self, "Back to Profile", self.back_to_profile, fonts).pack(pady=14)

    def back_to_profile(self):
        self.controller.show_frame(SuspectProfileFrame, suspect_id=self.suspect_id)
        # =============================================================================
# SECTION 8: LOCATIONS
# =============================================================================

class LocationListFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation

        make_title_bar(self, fonts, "Locations", "Choose a room of the mansion to investigate.").pack(
            fill="x", padx=20, pady=(16, 6))

        grid = tk.Frame(self, bg=BG_DARK)
        grid.pack(fill="both", expand=True, padx=20, pady=10)

        for index, location in enumerate(controller.game_data.location_list()):
            row, col = divmod(index, 3)
            card = make_panel(grid, width=230, height=160)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)
            tk.Label(card, text=f"[{location.icon}] {location.name}", font=fonts["subheading"],
                     bg=BG_PANEL, fg=TEXT_LIGHT, wraplength=200).pack(pady=(18, 4))
            found = sum(1 for eid in location.evidence_ids if eid in inv.discovered_evidence)
            total = len(location.evidence_ids)
            visited_mark = "Visited" if location.id in inv.visited_locations else "Not yet visited"
            tk.Label(card, text=f"Evidence: {found}/{total}   ({visited_mark})", font=fonts["small"],
                     bg=BG_PANEL, fg=TEXT_MUTED).pack(pady=(4, 8))
            HoverButton(card, "Investigate", lambda lid=location.id: self.open_location(lid), fonts, width=14).pack()

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)

    def open_location(self, location_id):
        self.controller.show_frame(LocationDetailFrame, location_id=location_id)


class LocationDetailFrame(tk.Frame):
    def __init__(self, parent, controller, location_id):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self.location_id = location_id
        fonts = controller.fonts
        inv = controller.investigation
        location = controller.game_data.locations[location_id]
        inv.visit_location(location_id)

        make_title_bar(self, fonts, location.name, location.description).pack(fill="x", padx=20, pady=(16, 6))

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for evidence in controller.game_data.evidence_for_location(location_id):
            discovered = evidence.id in inv.discovered_evidence
            block = make_panel(scroll.inner)
            block.pack(fill="x", pady=6, padx=4)
            info = tk.Frame(block, bg=BG_PANEL)
            info.pack(side="left", fill="both", expand=True, padx=14, pady=10)

            if discovered:
                tk.Label(info, text=evidence.name, font=fonts["body_bold"], bg=BG_PANEL, fg=TEXT_LIGHT).pack(anchor="w")
                tk.Label(info, text=evidence.description, font=fonts["small"], bg=BG_PANEL, fg=TEXT_MUTED,
                         wraplength=600, justify="left").pack(anchor="w")
            else:
                tk.Label(info, text="Unexamined area", font=fonts["body_bold"], bg=BG_PANEL, fg=TEXT_MUTED).pack(anchor="w")
                tk.Label(info, text="Something here might be worth a closer look.", font=fonts["small"],
                         bg=BG_PANEL, fg=TEXT_MUTED).pack(anchor="w")

            button_area = tk.Frame(block, bg=BG_PANEL)
            button_area.pack(side="right", padx=14, pady=10)
            if discovered:
                HoverButton(button_area, "View Details", lambda eid=evidence.id: self.view_evidence(eid), fonts, width=14).pack()
            else:
                HoverButton(button_area, "Search Here", lambda eid=evidence.id: self.discover(eid), fonts, width=14).pack()

        nav_button(self, "Back to Locations", self.back_to_list, fonts).pack(pady=14)

    def discover(self, evidence_id):
        self.controller.investigation.discover_evidence(evidence_id)
        self.controller.show_frame(LocationDetailFrame, location_id=self.location_id)

    def view_evidence(self, evidence_id):
        self.controller.show_frame(EvidenceDetailFrame, evidence_id=evidence_id, return_location_id=self.location_id)

    def back_to_list(self):
        self.controller.show_frame(LocationListFrame)
        # =============================================================================
# SECTION 9: EVIDENCE
# =============================================================================

class EvidenceListFrame(tk.Frame):
    def __init__(self, parent, controller, filter_suspect_id=None):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self.filter_suspect_id = filter_suspect_id
        fonts = controller.fonts
        inv = controller.investigation

        subtitle = "All evidence you have discovered so far."
        if filter_suspect_id:
            suspect_name = controller.game_data.suspects[filter_suspect_id].name
            subtitle = f"Evidence related to {suspect_name}."

        make_title_bar(self, fonts, "Evidence", subtitle).pack(fill="x", padx=20, pady=(16, 6))

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        all_evidence = list(controller.game_data.evidence.values())
        if filter_suspect_id:
            all_evidence = [e for e in all_evidence if filter_suspect_id in e.related_suspects]

        discovered_any = False
        for evidence in all_evidence:
            if evidence.id not in inv.discovered_evidence:
                continue
            discovered_any = True
            examined = evidence.id in inv.examined_evidence
            block = make_panel(scroll.inner)
            block.pack(fill="x", pady=6, padx=4)
            info = tk.Frame(block, bg=BG_PANEL)
            info.pack(side="left", fill="both", expand=True, padx=14, pady=10)

            mark = "* " if evidence.importance == "high" else ""
            tk.Label(info, text=f"{mark}{evidence.name}", font=fonts["body_bold"], bg=BG_PANEL, fg=TEXT_LIGHT).pack(anchor="w")
            tk.Label(info, text=evidence.description, font=fonts["small"], bg=BG_PANEL, fg=TEXT_MUTED,
                     wraplength=560, justify="left").pack(anchor="w")
            color = IMPORTANCE_COLORS.get(evidence.importance, TEXT_MUTED)
            status = "(examined)" if examined else "(not yet examined)"
            tk.Label(info, text=f"Importance: {evidence.importance.upper()}  {status}", font=fonts["small"],
                     bg=BG_PANEL, fg=color).pack(anchor="w", pady=(2, 0))

            HoverButton(block, "View Details", lambda eid=evidence.id: self.view(eid), fonts, width=14).pack(
                side="right", padx=14, pady=10)

        if not discovered_any:
            tk.Label(scroll.inner, text="No evidence discovered yet. Investigate the locations!",
                     font=fonts["body"], bg=BG_DARK, fg=TEXT_MUTED).pack(pady=20)

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)

    def view(self, evidence_id):
        self.controller.show_frame(EvidenceDetailFrame, evidence_id=evidence_id)


class EvidenceDetailFrame(tk.Frame):
    def __init__(self, parent, controller, evidence_id, return_location_id=None):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        self.return_location_id = return_location_id
        fonts = controller.fonts
        inv = controller.investigation
        evidence = controller.game_data.evidence[evidence_id]
        inv.examine_evidence(evidence_id)

        location = controller.game_data.locations.get(evidence.location_id)
        location_name = location.name if location else "Unknown"

        make_title_bar(self, fonts, evidence.name,
                       f"Found in: {location_name}   |   Importance: {evidence.importance.upper()}").pack(
            fill="x", padx=20, pady=(16, 6))

        body = make_panel(self)
        body.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(body, text=evidence.description, font=fonts["body_bold"], bg=BG_PANEL, fg=TEXT_LIGHT,
                 wraplength=760, justify="left").pack(anchor="w", padx=20, pady=(20, 10))
        tk.Label(body, text=evidence.flavor, font=fonts["body"], bg=BG_PANEL, fg=TEXT_MUTED,
                 wraplength=760, justify="left").pack(anchor="w", padx=20, pady=(0, 20))

        if evidence.related_suspects:
            names = ", ".join(controller.game_data.suspects[sid].name for sid in evidence.related_suspects
                               if sid in controller.game_data.suspects)
            tk.Label(body, text=f"Related suspect(s): {names}", font=fonts["small"], bg=BG_PANEL,
                     fg=ACCENT_GOLD).pack(anchor="w", padx=20, pady=(0, 20))

        nav_button(self, "Back", self.go_back, fonts).pack(pady=14)

    def go_back(self):
        if self.return_location_id:
            self.controller.show_frame(LocationDetailFrame, location_id=self.return_location_id)
        else:
            self.controller.show_frame(EvidenceListFrame)
            # =============================================================================
# SECTION 10: TIMELINE
# =============================================================================

class TimelineFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts

        make_title_bar(self, fonts, "Timeline", "Reconstruct what happened during the evening.").pack(
            fill="x", padx=20, pady=(16, 6))

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for event in controller.game_data.timeline:
            block = make_panel(scroll.inner)
            block.pack(fill="x", pady=6, padx=4)
            row = tk.Frame(block, bg=BG_PANEL)
            row.pack(fill="x", padx=16, pady=10)
            tk.Label(row, text=event.time, font=fonts["subheading"], bg=BG_PANEL, fg=ACCENT_GOLD,
                     width=10, anchor="w").pack(side="left")
            text_col = tk.Frame(row, bg=BG_PANEL)
            text_col.pack(side="left", fill="x", expand=True)
            tk.Label(text_col, text=event.description, font=fonts["body"], bg=BG_PANEL, fg=TEXT_LIGHT,
                     wraplength=650, justify="left").pack(anchor="w")
            if event.note:
                tk.Label(text_col, text=f"Note: {event.note}", font=fonts["small"], bg=BG_PANEL,
                         fg=TEXT_MUTED, wraplength=650, justify="left").pack(anchor="w", pady=(2, 0))

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)
        # =============================================================================
# SECTION 11: DEDUCTIONS
# =============================================================================

class DeductionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation

        self.selected_a = tk.StringVar(value="")
        self.selected_b = tk.StringVar(value="")

        make_title_bar(self, fonts, "Deductions", "Select two pieces of evidence to see if they connect.").pack(
            fill="x", padx=20, pady=(16, 6))

        discovered = [controller.game_data.evidence[eid] for eid in inv.discovered_evidence]

        if len(discovered) < 2:
            tk.Label(self, text="You need at least two pieces of evidence before you can make a deduction. "
                                 "Keep investigating!", font=fonts["body"], bg=BG_DARK, fg=TEXT_MUTED,
                     wraplength=600).pack(pady=40)
        else:
            picker_frame = tk.Frame(self, bg=BG_DARK)
            picker_frame.pack(fill="x", padx=20, pady=10)
            self._build_picker(picker_frame, "Evidence A", self.selected_a, discovered)
            self._build_picker(picker_frame, "Evidence B", self.selected_b, discovered)
            HoverButton(self, "Connect Evidence", self.connect, fonts, width=24).pack(pady=10)

        self.result_panel = make_panel(self)
        self.result_panel.pack(fill="both", expand=True, padx=20, pady=10)
        self.result_label = tk.Label(self.result_panel, text="Your deduction result will appear here.",
                                      font=fonts["body"], bg=BG_PANEL, fg=TEXT_MUTED, wraplength=760, justify="left")
        self.result_label.pack(padx=20, pady=20, anchor="n")

        self._build_made_deductions_list(inv)

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)

    def _build_picker(self, parent, label, variable, evidence_list):
        fonts = self.controller.fonts
        col = tk.Frame(parent, bg=BG_DARK)
        col.pack(side="left", fill="x", expand=True, padx=10)
        tk.Label(col, text=label, font=fonts["body_bold"], bg=BG_DARK, fg=ACCENT_GOLD).pack(anchor="w")

        names = [e.name for e in evidence_list]
        ids_by_name = {e.name: e.id for e in evidence_list}
        variable.set(names[0])

        option = tk.OptionMenu(col, variable, *names)
        option.configure(bg=BG_INPUT, fg=TEXT_LIGHT, font=fonts["body"], highlightthickness=0,
                         activebackground=BORDER, relief="flat")
        option["menu"].configure(bg=BG_INPUT, fg=TEXT_LIGHT)
        option.pack(fill="x", pady=4)
        variable.ids_by_name = ids_by_name

    def connect(self):
        inv = self.controller.investigation
        id_a = self.selected_a.ids_by_name.get(self.selected_a.get())
        id_b = self.selected_b.ids_by_name.get(self.selected_b.get())

        if not id_a or not id_b:
            return
        if id_a == id_b:
            messagebox.showwarning("Same Evidence", "Please choose two different pieces of evidence.")
            return

        deduction = find_matching_deduction(self.controller.game_data, id_a, id_b)
        if deduction is None:
            self.result_label.configure(text="You don't find any meaningful connection between these two pieces of evidence.")
            return

        is_new = inv.register_deduction(deduction)
        prefix = "New Deduction!\n\n" if is_new else "(Already deduced)\n\n"
        self.result_label.configure(text=prefix + deduction.result_text)
        self.controller.show_frame(DeductionFrame)

    def _build_made_deductions_list(self, inv):
        fonts = self.controller.fonts
        if not inv.deductions_made:
            return
        tk.Label(self, text="Deductions made so far:", font=fonts["body_bold"], bg=BG_DARK,
                 fg=ACCENT_GOLD).pack(anchor="w", padx=24)
        made_scroll = ScrollableFrame(self)
        made_scroll.configure(height=120)
        made_scroll.pack(fill="x", padx=20, pady=(4, 10))
        for deduction_id in sorted(inv.deductions_made):
            deduction = next((d for d in self.controller.game_data.deductions if d.id == deduction_id), None)
            if deduction is None:
                continue
            tk.Label(made_scroll.inner, text=f"- {deduction.result_text}", font=fonts["small"], bg=BG_DARK,
                     fg=TEXT_MUTED, wraplength=740, justify="left").pack(anchor="w", pady=2)
            # =============================================================================
# SECTION 12: CASE NOTES
# =============================================================================

class NotesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts

        make_title_bar(self, fonts, "Case Notes", "Write down your theories as the investigation unfolds.").pack(
            fill="x", padx=20, pady=(16, 6))

        entry_panel = make_panel(self)
        entry_panel.pack(fill="x", padx=20, pady=10)
        self.text_entry = tk.Text(entry_panel, height=4, bg=BG_INPUT, fg=TEXT_LIGHT, font=fonts["body"],
                                   insertbackground=TEXT_LIGHT, relief="flat", wrap="word")
        self.text_entry.pack(fill="x", padx=14, pady=(14, 6))
        HoverButton(entry_panel, "Add Note", self.add_note, fonts, width=16).pack(anchor="e", padx=14, pady=(0, 14))

        tk.Label(self, text="Your Notes:", font=fonts["body_bold"], bg=BG_DARK, fg=ACCENT_GOLD).pack(
            anchor="w", padx=24, pady=(6, 0))

        self.notes_scroll = ScrollableFrame(self)
        self.notes_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        self._render_notes()

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)

    def _render_notes(self):
        for widget in self.notes_scroll.inner.winfo_children():
            widget.destroy()

        fonts = self.controller.fonts
        inv = self.controller.investigation

        if not inv.notes:
            tk.Label(self.notes_scroll.inner, text="No notes yet. Write your first theory above.",
                     font=fonts["body"], bg=BG_DARK, fg=TEXT_MUTED).pack(pady=10)
            return

        for index, note in enumerate(inv.notes):
            block = make_panel(self.notes_scroll.inner)
            block.pack(fill="x", pady=6, padx=4)
            tk.Label(block, text=note.text, font=fonts["body"], bg=BG_PANEL, fg=TEXT_LIGHT,
                     wraplength=650, justify="left").pack(side="left", padx=14, pady=12, fill="x", expand=True)
            HoverButton(block, "Delete", lambda i=index: self.delete_note(i), fonts, bg=ACCENT_RED, width=10).pack(
                side="right", padx=14, pady=12)

    def add_note(self):
        text = self.text_entry.get("1.0", "end").strip()
        if not text:
            return
        self.controller.investigation.add_note(text)
        self.text_entry.delete("1.0", "end")
        self._render_notes()

    def delete_note(self, index):
        self.controller.investigation.delete_note(index)
        self._render_notes()
        # =============================================================================
# SECTION 13: CASE STATUS
# =============================================================================

class CaseStatusFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation
        game_data = controller.game_data

        make_title_bar(self, fonts, "Case Status", "An overview of your investigation so far.").pack(
            fill="x", padx=20, pady=(16, 6))

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        summary = make_panel(scroll.inner)
        summary.pack(fill="x", pady=8, padx=4)

        interviewed_suspects = sum(1 for sid in game_data.suspects if len(inv.asked_questions.get(sid, set())) > 0)
        stats = [
            ("Evidence Discovered", f"{len(inv.discovered_evidence)} / {len(game_data.evidence)}"),
            ("Suspects Interviewed", f"{interviewed_suspects} / {len(game_data.suspects)}"),
            ("Deductions Made", f"{len(inv.deductions_made)} / {len(game_data.deductions)}"),
            ("Locations Visited", f"{len(inv.visited_locations)} / {len(game_data.locations)}"),
            ("Current Score", str(inv.score)),
        ]
        for label, value in stats:
            row = tk.Frame(summary, bg=BG_PANEL)
            row.pack(fill="x", padx=18, pady=6)
            tk.Label(row, text=label, font=fonts["body_bold"], bg=BG_PANEL, fg=TEXT_LIGHT).pack(side="left")
            tk.Label(row, text=value, font=fonts["body_bold"], bg=BG_PANEL, fg=ACCENT_GOLD).pack(side="right")

        tk.Label(scroll.inner, text="Suspicion Levels", font=fonts["subheading"], bg=BG_DARK,
                 fg=ACCENT_GOLD).pack(anchor="w", padx=8, pady=(16, 6))
        for suspect in game_data.suspect_list():
            row = make_panel(scroll.inner)
            row.pack(fill="x", pady=4, padx=4)
            tk.Label(row, text=suspect.name, font=fonts["body"], bg=BG_PANEL, fg=TEXT_LIGHT,
                     width=22, anchor="w").pack(side="left", padx=14, pady=8)
            suspicion_bar(row, inv.suspicion.get(suspect.id, 0), fonts).pack(side="left", padx=14, pady=8)

        tk.Label(scroll.inner, text="Important Discoveries", font=fonts["subheading"], bg=BG_DARK,
                 fg=ACCENT_GOLD).pack(anchor="w", padx=8, pady=(16, 6))
        important = [game_data.evidence[eid] for eid in inv.discovered_evidence
                     if game_data.evidence[eid].importance == "high"]
        if not important:
            tk.Label(scroll.inner, text="No major discoveries yet.", font=fonts["body"], bg=BG_DARK,
                     fg=TEXT_MUTED).pack(anchor="w", padx=8, pady=4)
        else:
            for evidence in important:
                tk.Label(scroll.inner, text=f"* {evidence.name}", font=fonts["body"], bg=BG_DARK,
                         fg=TEXT_LIGHT).pack(anchor="w", padx=8, pady=2)

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=14)
        # =============================================================================
# SECTION 14: ACCUSATION AND ENDING
# =============================================================================

class AccusationFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation
        game_data = controller.game_data

        make_title_bar(self, fonts, "Make Accusation",
                       "This is it. Choose carefully - this ends the investigation.").pack(
            fill="x", padx=20, pady=(16, 6))

        body = make_panel(self)
        body.pack(fill="both", expand=True, padx=20, pady=10)
        inner = tk.Frame(body, bg=BG_PANEL)
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(inner, text="Who stole the necklace?", font=fonts["body_bold"], bg=BG_PANEL,
                 fg=ACCENT_GOLD).pack(anchor="w", pady=(0, 4))
        suspect_names = [s.name for s in game_data.suspect_list()]
        self.suspect_ids_by_name = {s.name: s.id for s in game_data.suspect_list()}
        self.suspect_var = tk.StringVar(value=suspect_names[0])
        self._make_dropdown(inner, self.suspect_var, suspect_names)

        tk.Label(inner, text="How was it done?", font=fonts["body_bold"], bg=BG_PANEL,
                 fg=ACCENT_GOLD).pack(anchor="w", pady=(16, 4))
        method_texts = [m["text"] for m in ACCUSATION_METHODS]
        self.method_ids_by_text = {m["text"]: m["id"] for m in ACCUSATION_METHODS}
        self.method_var = tk.StringVar(value=method_texts[0])
        self._make_dropdown(inner, self.method_var, method_texts, width=60)

        tk.Label(inner, text="What is your strongest evidence?", font=fonts["body_bold"], bg=BG_PANEL,
                 fg=ACCENT_GOLD).pack(anchor="w", pady=(16, 4))
        discovered = [game_data.evidence[eid] for eid in inv.discovered_evidence]
        if discovered:
            evidence_names = [e.name for e in discovered]
            self.evidence_ids_by_name = {e.name: e.id for e in discovered}
            self.evidence_var = tk.StringVar(value=evidence_names[0])
            self._make_dropdown(inner, self.evidence_var, evidence_names)
        else:
            self.evidence_ids_by_name = {}
            self.evidence_var = tk.StringVar(value="")
            tk.Label(inner, text="(No evidence discovered yet.)", font=fonts["body"], bg=BG_PANEL,
                     fg=TEXT_MUTED).pack(anchor="w")

        HoverButton(inner, "Submit Accusation", self.submit, fonts, width=26, bg=ACCENT_RED,
                    hover_bg="#c65552").pack(pady=(24, 4))

        nav_button(self, "Back to Dashboard", lambda: controller.show_frame(DashboardFrame), fonts).pack(pady=10)

    def _make_dropdown(self, parent, variable, options, width=40):
        fonts = self.controller.fonts
        option = tk.OptionMenu(parent, variable, *options)
        option.configure(bg=BG_INPUT, fg=TEXT_LIGHT, font=fonts["body"], highlightthickness=0,
                         activebackground=BORDER, relief="flat", width=width, anchor="w")
        option["menu"].configure(bg=BG_INPUT, fg=TEXT_LIGHT)
        option.pack(anchor="w")

    def submit(self):
        if not self.evidence_ids_by_name:
            messagebox.showwarning("No Evidence", "You have no evidence to present. "
                                                    "Investigate more before accusing anyone.")
            return

        if not messagebox.askyesno("Confirm Accusation",
                                    "Are you sure you want to make this accusation? "
                                    "This will end the investigation."):
            return

        suspect_id = self.suspect_ids_by_name[self.suspect_var.get()]
        method_id = self.method_ids_by_text[self.method_var.get()]
        evidence_id = self.evidence_ids_by_name[self.evidence_var.get()]

        inv = self.controller.investigation
        outcome_key = evaluate_accusation(inv, suspect_id, method_id, evidence_id)
        final_score = finalize_score(inv, outcome_key)
        rank = rank_for_score(final_score)

        inv.accusation_made = True
        inv.accusation_result = outcome_key
        inv.final_rank = rank

        self.controller.show_frame(EndingFrame, outcome_key=outcome_key, accused_suspect_id=suspect_id)


class EndingFrame(tk.Frame):
    def __init__(self, parent, controller, outcome_key, accused_suspect_id):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        fonts = controller.fonts
        inv = controller.investigation
        color = OUTCOME_COLORS.get(outcome_key, ACCENT_GOLD)

        center = tk.Frame(self, bg=BG_DARK)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text=OUTCOME_TITLES.get(outcome_key, "CASE CLOSED"), font=fonts["title"],
                 bg=BG_DARK, fg=color, wraplength=800, justify="center").pack(pady=(0, 16))
        tk.Label(center, text=OUTCOME_NARRATIVES.get(outcome_key, ""), font=fonts["body"], bg=BG_DARK,
                 fg=TEXT_LIGHT, wraplength=700, justify="center").pack(pady=(0, 20))
        tk.Label(center, text=f"FINAL SCORE: {inv.score}", font=fonts["heading"], bg=BG_DARK,
                 fg=ACCENT_GOLD).pack()
        tk.Label(center, text=f"DETECTIVE RANK: {inv.final_rank}", font=fonts["subheading"], bg=BG_DARK,
                 fg=TEXT_LIGHT).pack(pady=(2, 24))

        button_row = tk.Frame(center, bg=BG_DARK)
        button_row.pack()
        HoverButton(button_row, "New Investigation", self.new_investigation, fonts, width=20).pack(side="left", padx=6)
        HoverButton(button_row, "Main Menu", lambda: controller.show_frame(MainMenuFrame), fonts, width=20).pack(
            side="left", padx=6)

    def new_investigation(self):
        self.controller.start_new_investigation()
        self.controller.show_frame(DashboardFrame)


# =============================================================================
# SECTION 15: ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
