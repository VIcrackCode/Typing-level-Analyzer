from __future__ import annotations

import json
import os
import random
import time
import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


APP_DIR = Path(__file__).resolve().parent
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
TEST_SECONDS = 60
WORD_COUNT = 100
SESSION_TTL_SECONDS = 15 * 60

WORDS_POOL = [
    "apple", "banana", "computer", "keyboard", "python", "screen", "internet",
    "science", "engineer", "project", "development", "programming", "logic",
    "algorithm", "network", "database", "function", "variable", "object",
    "class", "method", "loop", "condition", "array", "string", "integer",
    "compile", "execute", "memory", "storage", "cloud", "system", "design",
    "structure", "testing", "debug", "performance", "security", "data",
    "analysis", "model", "training", "learning", "automation", "software",
    "able", "acid", "aged", "also", "area", "army", "away", "baby", "back",
    "ball", "band", "bank", "base", "bath", "bear", "beat", "been", "beer",
    "bell", "belt", "best", "bill", "bird", "blow", "blue", "boat", "body",
    "bond", "bone", "book", "boom", "born", "boss", "both", "bowl", "bulk",
    "burn", "bush", "busy", "call", "calm", "came", "camp", "card", "care",
    "case", "cash", "cast", "cell", "chat", "chip", "city", "club", "coal",
    "coat", "code", "cold", "come", "cook", "cool", "cope", "copy", "core",
    "cost", "crew", "crop", "dark", "date", "dawn", "days", "dead", "deal",
    "dean", "dear", "debt", "deep", "deny", "desk", "dial", "diet", "disc",
    "disk", "does", "done", "door", "dose", "down", "draw", "drew", "drop",
    "drug", "dual", "duke", "dust", "duty", "each", "earn", "ease", "east",
    "easy", "edge", "else", "even", "ever", "evil", "exit", "face", "fact",
    "fail", "fair", "fall", "farm", "fast", "fate", "fear", "feed", "feel",
    "feet", "fell", "felt", "file", "fill", "film", "find", "fine", "fire",
    "firm", "fish", "five", "flat", "flow", "food", "foot", "ford", "form",
    "fort", "four", "free", "from", "fuel", "full", "fund", "gain", "game",
    "gate", "gave", "gear", "gene", "gift", "girl", "give", "glad", "goal",
    "goes", "gold", "golf", "gone", "good", "gray", "grew", "grey", "grow",
    "gulf", "hair", "half", "hall", "hand", "hang", "hard", "harm", "hate",
    "have", "head", "hear", "heat", "held", "help", "here", "hero", "high",
    "hill", "hire", "hold", "hole", "home", "hope", "host", "hour", "huge",
    "hung", "hunt", "hurt", "idea", "inch", "into", "iron", "item", "join",
    "jump", "jury", "just", "keen", "keep", "kept", "kick", "kill", "kind",
    "king", "knew", "know", "lack", "lady", "laid", "lake", "land", "lane",
    "last", "late", "lead", "left", "less", "life", "lift", "like", "line",
    "link", "list", "live", "load", "loan", "lock", "logo", "long", "look",
    "lose", "loss", "lost", "love", "luck", "made", "mail", "main", "make",
    "male", "many", "mark", "mass", "meal", "mean", "meat", "meet", "menu",
    "mile", "milk", "mill", "mind", "mine", "miss", "mode", "mood", "moon",
    "more", "most", "move", "much", "must", "name", "navy", "near", "neck",
    "need", "news", "next", "nice", "nine", "none", "nose", "note", "okay",
    "once", "only", "onto", "open", "oral", "over", "pace", "pack", "page",
    "paid", "pain", "pair", "palm", "park", "part", "pass", "past", "path",
    "peak", "pick", "pink", "pipe", "plan", "play", "plot", "plug", "plus",
    "poll", "pool", "poor", "port", "post", "pull", "pure", "push", "race",
    "rail", "rain", "rank", "rare", "rate", "read", "real", "rear", "rely",
    "rent", "rest", "rice", "rich", "ride", "ring", "rise", "risk", "road",
    "rock", "role", "roll", "roof", "room", "root", "rose", "rule", "rush",
    "safe", "said", "sake", "sale", "salt", "same", "sand", "save", "seat",
    "seed", "seek", "seem", "seen", "self", "sell", "send", "sent", "ship",
    "shop", "shot", "show", "shut", "sick", "side", "sign", "site", "size",
    "skin", "slip", "slow", "snow", "soft", "soil", "sold", "sole", "some",
    "song", "soon", "sort", "soul", "spot", "star", "stay", "step", "stop",
    "such", "suit", "sure", "take", "tale", "talk", "tall", "tank", "tape",
    "task", "team", "tech", "tell", "tend", "term", "test", "text", "than",
    "that", "them", "then", "they", "thin", "this", "thus", "till", "time",
    "tiny", "told", "toll", "tone", "took", "tool", "tour", "town", "tree",
    "trip", "true", "tune", "turn", "twin", "type", "unit", "upon", "used",
    "user", "vary", "vast", "very", "vice", "view", "vote", "wage", "wait",
    "wake", "walk", "wall", "want", "ward", "warm", "wash", "wave", "ways",
    "weak", "wear", "week", "well", "went", "were", "west", "what", "when",
    "whom", "wide", "wife", "wild", "will", "wind", "wine", "wing", "wire",
    "wise", "wish", "with", "wood", "word", "wore", "work", "yard", "yeah",
    "year", "your", "zero", "angle", "award", "basic", "beach", "birth",
    "block", "brain", "brand", "bread", "break", "brown", "build", "buyer",
    "cause", "chain", "chair", "chart", "check", "chief", "child", "claim",
    "clean", "clear", "click", "clock", "coach", "coast", "could", "count",
    "court", "cover", "craft", "crash", "cream", "crime", "cross", "crowd",
    "crown", "cycle", "daily", "dance", "death", "depth", "doubt", "draft",
    "drama", "dream", "dress", "drink", "drive", "earth", "enemy", "entry",
    "equal", "error", "event", "faith", "false", "fault", "field", "fight",
    "final", "floor", "focus", "force", "frame", "fresh", "front", "fruit",
    "glass", "grant", "grass", "green", "group", "guide", "heart", "heavy",
    "hotel", "house", "human", "image", "index", "inner", "input", "issue",
    "judge", "knife", "large", "laser", "later", "layer", "learn", "least",
    "leave", "legal", "level", "light", "limit", "local", "loose", "lower",
    "lucky", "lunch", "major", "maker", "march", "match", "maybe", "mayor",
    "media", "metal", "might", "minor", "money", "month", "motor", "mount",
    "mouse", "mouth", "movie", "music", "never", "night", "noise", "north",
    "novel", "nurse", "occur", "offer", "often", "order", "other", "owner",
    "panel", "paper", "party", "peace", "phase", "phone", "photo", "piece",
    "pilot", "pitch", "place", "plain", "plane", "plant", "plate", "point",
    "power", "press", "price", "pride", "prime", "print", "prior", "prize",
    "proof", "proud", "prove", "queen", "quick", "quiet", "radio", "raise",
    "range", "rapid", "ratio", "reach", "ready", "refer", "right", "rival",
    "river", "rough", "round", "route", "royal", "rural", "scale", "scene",
    "scope", "score", "sense", "serve", "seven", "shall", "shape", "share",
    "sharp", "sheet", "shift", "shine", "shirt", "shock", "shoot", "short",
    "shown", "sight", "since", "skill", "sleep", "slide", "small", "smart",
    "smile", "smoke", "solid", "solve", "sorry", "sound", "south", "space",
    "spare", "speak", "speed", "spend", "spent", "split", "spoke", "sport",
    "staff", "stage", "stand", "start", "state", "steam", "steel", "stick",
    "still", "stock", "stone", "store", "storm", "story", "strip", "stuck",
    "study", "stuff", "style", "sugar", "suite", "super", "sweet", "table",
    "taken", "taste", "teach", "thank", "their", "theme", "there", "these",
    "thing", "think", "third", "those", "three", "throw", "tight", "title",
    "today", "topic", "total", "touch", "tough", "tower", "track", "trade",
    "train", "treat", "trend", "trial", "trust", "truth", "under", "union",
    "unity", "upper", "upset", "urban", "usage", "usual", "valid", "value",
    "video", "virus", "visit", "vital", "voice", "waste", "watch", "water",
    "wheel", "where", "which", "while", "white", "whole", "whose", "woman",
    "women", "world", "worry", "worth", "write", "wrong", "yield", "young",
]


@dataclass(slots=True)
class TestSession:
    words: list[str]
    created_at: float = field(default_factory=time.time)


SESSIONS: dict[str, TestSession] = {}


def generate_words(count: int = WORD_COUNT) -> list[str]:
    """Return a fresh prompt of random words for one test session."""
    return random.choices(WORDS_POOL, k=count)


def get_level(correct_words: int) -> str:
    if correct_words < 20:
        return "Beginner"
    if correct_words < 40:
        return "Intermediate"
    return "Master"


def evaluate_attempts(
    words: list[str],
    attempts: list[dict[str, Any]],
    elapsed_seconds: int = TEST_SECONDS,
) -> dict[str, Any]:
    visited_indexes: set[int] = set()
    correct_words = 0
    characters = 0

    for attempt in attempts:
        index = attempt.get("index")
        typed = str(attempt.get("typed", "")).strip().lower()

        if not isinstance(index, int) or index < 0 or index >= len(words):
            continue
        if index in visited_indexes:
            continue

        visited_indexes.add(index)
        if typed == words[index]:
            correct_words += 1
            characters += len(words[index])

    visited_words = len(visited_indexes)
    elapsed_minutes = max(1, min(elapsed_seconds, TEST_SECONDS)) / 60
    accuracy = (correct_words / visited_words * 100) if visited_words else 0.0
    error_rate = ((visited_words - correct_words) / visited_words * 100) if visited_words else 0.0

    return {
        "visited_words": visited_words,
        "correct_words": correct_words,
        "characters": characters,
        "words_per_minute": round(correct_words / elapsed_minutes),
        "chars_per_minute": round(characters / elapsed_minutes),
        "accuracy": round(accuracy, 2),
        "error_rate": round(error_rate, 2),
        "level": get_level(correct_words),
    }


def cleanup_sessions() -> None:
    now = time.time()
    expired_ids = [
        session_id
        for session_id, session in SESSIONS.items()
        if now - session.created_at > SESSION_TTL_SECONDS
    ]
    for session_id in expired_ids:
        del SESSIONS[session_id]


class TypingTestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/session":
            self.create_session()
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/result":
            self.submit_result()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "API endpoint not found")

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_cors_headers()
        self.end_headers()

    def create_session(self) -> None:
        cleanup_sessions()
        session_id = uuid.uuid4().hex
        session = TestSession(words=generate_words())
        SESSIONS[session_id] = session
        self.send_json(
            {
                "session_id": session_id,
                "words": session.words,
                "seconds": TEST_SECONDS,
            }
        )

    def submit_result(self) -> None:
        payload = self.read_json()
        session_id = str(payload.get("session_id", ""))
        attempts = payload.get("attempts", [])
        elapsed_seconds = payload.get("elapsed_seconds", TEST_SECONDS)

        if not isinstance(attempts, list):
            self.send_json({"error": "Attempts must be a list."}, HTTPStatus.BAD_REQUEST)
            return
        if not isinstance(elapsed_seconds, int):
            elapsed_seconds = TEST_SECONDS

        session = SESSIONS.get(session_id)
        if session is None:
            self.send_json({"error": "Session expired or invalid."}, HTTPStatus.NOT_FOUND)
            return

        result = evaluate_attempts(session.words, attempts, elapsed_seconds)
        self.send_json(result)

    def read_json(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        if not raw_body:
            return {}
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return {}
        return body if isinstance(body, dict) else {}

    def send_json(self, data: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def run_server() -> None:
    server = ThreadingHTTPServer((HOST, PORT), TypingTestHandler)
    local_url = f"http://127.0.0.1:{PORT}"
    print(f"Typing Speed Test running on {HOST}:{PORT}")
    print(f"Local URL: {local_url}")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
