"""
missions.py  ─  Átomos Perdidos v2
Misión narrativa "El Elixir de la Vida": un alquimista despistado necesita
ayuda para sintetizar una serie de moléculas, de fácil a difícil.

La historia se integra como un pseudo-nivel ("story") que reutiliza el motor
de juego existente: cada capítulo apunta a una molécula ya definida en
molecules.py, y Octeto narra el diálogo antes de cada una.
"""

from molecules import get_molecule_by_id

MISSION = {
    "id": "elixir",
    "titulo": "El Elixir de la Vida",
    "intro": ("El alquimista Anselmo del Matraz lleva 40 años buscando el "
              "Elixir de la Vida… y acaba de descubrir que perdió sus apuntes. "
              "Octeto se ha ofrecido a ayudarle (a cambio de calamares NO, "
              "gracias). Reconstruye las moléculas de su receta, de la más "
              "simple a la más compleja."),
    # Capítulos en orden: mol_id debe existir en molecules.py
    "capitulos": [
        {"mol_id": "H2",
         "dialogo": ("Anselmo: «Todo empieza con el aliento del universo, la "
                     "sustancia más ligera que existe.» — Octeto: «Se refiere al "
                     "hidrógeno, no a sus pies. Empecemos fácil.»")},
        {"mol_id": "O2",
         "dialogo": ("Anselmo: «¡Ahora el soplo de la vida! Sin él, ni las velas "
                     "ni yo duramos mucho.» — Octeto: «Oxígeno. En mi arrecife "
                     "hay de sobra, aquí hay que fabricarlo.»")},
        {"mol_id": "H2O",
         "dialogo": ("Anselmo: «Une el aliento y el soplo… ¡y obtendrás la base "
                     "de todo elixir!» — Octeto: «Agua. Cuatro décadas para "
                     "llegar al agua. No digas nada, sígueme la corriente.»")},
        {"mol_id": "CO2",
         "dialogo": ("Anselmo: «¡Burbujas! Un elixir sin burbujas es solo sopa "
                     "fría.» — Octeto: «Dióxido de carbono. Técnicamente tiene "
                     "razón: sin CO₂ no hay gaseosa.»")},
        {"mol_id": "CH3COOH",
         "dialogo": ("Anselmo: «Un toque ácido para conservar la mezcla, como "
                     "hacían los sumerios.» — Octeto: «Ácido acético. Huele a "
                     "que el elixir va camino de ser una vinagreta.»")},
        {"mol_id": "C2H5OH",
         "dialogo": ("Anselmo: «Y por último… ¡el espíritu de la vida, el "
                     "spiritus vini!» — Octeto: «Etanol. Ahora entiendo por qué "
                     "el elixir le lleva 40 años: se lo va bebiendo.»")},
    ],
    "final": ("Anselmo mezcla las seis moléculas, lo prueba… y sonríe: «¡Es "
              "vinagreta con burbujas! Bueno, la vida son las pequeñas cosas.» "
              "Octeto: «Misión cumplida. El verdadero elixir era la química "
              "que aprendimos por el camino.» 🐙✨"),
}


def obtener_moleculas_historia() -> list:
    """
    Lista de moléculas (dicts completos de molecules.py) en el orden de la
    historia. Se registra como MOLECULES["story"] para reutilizar el motor.
    """
    mols = []
    for cap in MISSION["capitulos"]:
        m = get_molecule_by_id(cap["mol_id"])
        if m:
            mols.append(m)
    return mols


def obtener_dialogo(indice: int) -> str:
    """Diálogo del capítulo `indice` (0-based), o cadena vacía."""
    caps = MISSION["capitulos"]
    if 0 <= indice < len(caps):
        return caps[indice]["dialogo"]
    return ""


def total_capitulos() -> int:
    return len(MISSION["capitulos"])
