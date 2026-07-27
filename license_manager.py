"""
license_manager.py
-------------------
DataForge CLI — RGS Labs™

Maneja la lectura, escritura y validación local del archivo de licencia
(~/.dataforge/license.json).

Este módulo reemplaza el esquema anterior:

    [{"key": "...", "plan": "pro", "active": true}]

por un esquema "profesional", pensado para crecer sin romper nada:

    {
      "license":     "DFORGE-PRO-8F92A-B41C9",
      "plan":        "pro",          # free | pro | teams | enterprise
      "owner":       "client@email.com",
      "issued_at":   "2026-08-24T14:25:00Z",
      "expires_at":  null,           # null = sin vencimiento (compra única / lifetime)
      "seats":       null,           # solo se usa en teams/enterprise
      "activation":  "online",       # online | offline
      "version":     "1.0",          # versión del ESQUEMA del archivo, no del CLI
      "signature":   "2F91C83A9E...",# firma emitida por el backend (no se genera aquí)
      "status":      "active",       # active | revoked | expired | suspended
      "renewed_at":  null,           # última renovación, para historial de suscripción
      "history":     []              # lista de eventos futuros (renovación, revocación, etc.)
    }

IMPORTANTE — sobre la firma (`signature`):
El HMAC_SHA256(email + plan, MASTER_SECRET) se calcula del lado del servidor
(webhook de Lemon Squeezy), NUNCA en el cliente. Si el CLI conociera
MASTER_SECRET, cualquier usuario podría fabricar sus propias licencias.
Por ahora, mientras no exista un backend real, `activate_license()` solo
valida el FORMATO del código y arma el registro localmente — está marcado
con un TODO para conectarlo a un endpoint de verificación en cuanto exista.
"""

import os
import re
import json
import uuid
from datetime import datetime, timezone

# ------------------------------------------------------------------
# Rutas y constantes
# ------------------------------------------------------------------

LICENSE_DIR = os.path.expanduser("~/.dataforge")
LICENSE_FILE = os.path.join(LICENSE_DIR, "license.json")

SCHEMA_VERSION = "1.0"

VALID_PLANS = ("free", "pro", "teams", "enterprise")
VALID_STATUS = ("active", "revoked", "expired", "suspended")
VALID_ACTIVATION_TYPES = ("online", "offline")

# DFORGE-PRO-8F92A-B41C9  /  DFORGE-TEAMS-XXXX-XXXXX  /  DFORGE-ENT-XXXX-XXXXX
LICENSE_CODE_PATTERN = re.compile(
    r"^DFORGE-(PRO|TEAMS|ENT)-[A-Z0-9]{4,6}-[A-Z0-9]{4,6}$"
)

_PLAN_BY_CODE_PREFIX = {
    "PRO": "pro",
    "TEAMS": "teams",
    "ENT": "enterprise",
}

FREE_PLAN_RECORD = {
    "license": None,
    "plan": "free",
    "owner": None,
    "issued_at": None,
    "expires_at": None,
    "seats": None,
    "activation": None,
    "version": SCHEMA_VERSION,
    "signature": None,
    "status": "active",
    "renewed_at": None,
    "history": [],
}


# ------------------------------------------------------------------
# Utilidades internas
# ------------------------------------------------------------------

def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ensure_dir():
    os.makedirs(LICENSE_DIR, exist_ok=True)


def _placeholder_signature(license_code, plan):
    """
    Marcador de posición local, NO es una firma criptográfica válida.
    Sirve solo para que el archivo tenga la forma correcta mientras no
    exista un backend de licencias. Se debe sobrescribir con la firma
    real que devuelva el servidor (HMAC_SHA256(email+plan, MASTER_SECRET)).
    """
    return f"UNVERIFIED-{uuid.uuid4().hex[:16].upper()}"


# ------------------------------------------------------------------
# Lectura / escritura
# ------------------------------------------------------------------

def load_license():
    """
    Devuelve el registro de licencia actual.
    Si no existe archivo, o está corrupto, devuelve el registro Free
    por defecto (nunca lanza excepción hacia el resto del CLI).
    """
    if not os.path.exists(LICENSE_FILE):
        return dict(FREE_PLAN_RECORD)

    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(FREE_PLAN_RECORD)

    if not isinstance(data, dict) or "plan" not in data:
        return dict(FREE_PLAN_RECORD)

    return data


def save_license(record):
    """Escribe el registro de licencia en ~/.dataforge/license.json."""
    _ensure_dir()
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    return record


def clear_license():
    """Vuelve al plan Free eliminando el archivo de licencia local."""
    if os.path.exists(LICENSE_FILE):
        os.remove(LICENSE_FILE)


# ------------------------------------------------------------------
# Validación
# ------------------------------------------------------------------

def is_expired(record):
    expires_at = record.get("expires_at")
    if not expires_at:
        return False
    try:
        expiry = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    return datetime.now(timezone.utc) > expiry


def is_active(record=None):
    """True si la licencia local está activa y no vencida."""
    record = record or load_license()
    if record.get("status") != "active":
        return False
    if is_expired(record):
        return False
    return True


def get_plan(record=None):
    """Devuelve el plan efectivo: 'free' si no hay licencia activa."""
    record = record or load_license()
    if not is_active(record):
        return "free"
    return record.get("plan", "free")


def has_feature(feature, record=None):
    """
    Chequeo simple de features por plan. Se puede ir enriqueciendo
    a futuro sin tocar el resto del CLI.
    """
    plan = get_plan(record)
    feature_map = {
        "ask": ("pro", "teams", "enterprise"),
        "history": ("pro", "teams", "enterprise"),
        "team_admin": ("teams", "enterprise"),
    }
    allowed_plans = feature_map.get(feature, VALID_PLANS)
    return plan in allowed_plans


# ------------------------------------------------------------------
# Activación
# ------------------------------------------------------------------

def activate_license(code, owner_email=None):
    """
    Activa una licencia localmente a partir de un código con formato
    DFORGE-<PLAN>-XXXX-XXXXX.

    Devuelve (ok: bool, message: str, record: dict | None).

    TODO (cuando exista backend de licencias):
    Reemplazar esta validación de formato por una llamada real al
    endpoint de verificación, y guardar la `signature` que devuelva
    el servidor en lugar del placeholder local.
    """
    code = (code or "").strip().upper()

    match = LICENSE_CODE_PATTERN.match(code)
    if not match:
        return False, "El código de licencia no tiene un formato válido (DFORGE-PLAN-XXXX-XXXXX).", None

    plan = _PLAN_BY_CODE_PREFIX[match.group(1)]

    record = {
        "license": code,
        "plan": plan,
        "owner": owner_email,
        "issued_at": _now_iso(),
        "expires_at": None,
        "seats": None if plan in ("free", "pro") else 1,
        "activation": "online",
        "version": SCHEMA_VERSION,
        "signature": _placeholder_signature(code, plan),
        "status": "active",
        "renewed_at": None,
        "history": [
            {"event": "activated", "at": _now_iso()}
        ],
    }

    save_license(record)
    return True, f"Licencia {plan.upper()} activada correctamente.", record


def revoke_license(reason=None):
    """Marca la licencia local como revocada, sin borrar el historial."""
    record = load_license()
    if record.get("plan") == "free":
        return False, "No hay ninguna licencia activa para revocar."

    record["status"] = "revoked"
    record.setdefault("history", []).append(
        {"event": "revoked", "at": _now_iso(), "reason": reason}
    )
    save_license(record)
    return True, "Licencia revocada localmente."
