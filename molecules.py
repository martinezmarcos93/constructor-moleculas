"""
molecules.py  ─  Átomos Perdidos v1.1
Base de datos ampliada: 63 moléculas (21 fácil · 21 medio · 21 difícil)
Drop-in replacement del original — app.py NO necesita cambios.

Cada entrada:
  id, name, formula, atoms[], missing[], hints[], fun_fact, svg_key
"""

MOLECULES = {

# ══════════════════════════════════════════════════
#  FÁCIL — 21 moléculas · siempre falta 1 átomo
# ══════════════════════════════════════════════════
"easy": [

  {"id":"H2","name":"Hidrógeno molecular","formula":"H₂",
   "atoms":["H","H"],"missing":[1],
   "hints":["1 electrón de valencia, nivel s.",
            "Grupo 1, Período 1.",
            "Configuración completa: 1s¹"],
   "fun_fact":"El H₂ es el elemento más abundante del universo (≈75 % en masa). Las estrellas lo fusionan liberando energía nuclear y produciendo helio.",
   "svg_key":"H2"},

  {"id":"O2","name":"Oxígeno molecular","formula":"O₂",
   "atoms":["O","O"],"missing":[0],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"El O₂ representa el 21 % del aire. Lo identificó Priestley en 1774 calentando óxido de mercurio rojo con una lupa.",
   "svg_key":"O2"},

  {"id":"N2","name":"Nitrógeno molecular","formula":"N₂",
   "atoms":["N","N"],"missing":[1],
   "hints":["5 electrones de valencia.",
            "Grupo 15, Período 2.",
            "Configuración: [He] 2s² 2p³"],
   "fun_fact":"El N₂ tiene el triple enlace covalente más fuerte conocido (945 kJ/mol). Por eso es tan difícil fijarlo industrialmente.",
   "svg_key":"N2"},

  {"id":"HCl","name":"Cloruro de hidrógeno","formula":"HCl",
   "atoms":["H","Cl"],"missing":[1],
   "hints":["7 electrones de valencia.",
            "Grupo 17 (halógenos), Período 3.",
            "Configuración: [Ne] 3s² 3p⁵"],
   "fun_fact":"El HCl en agua da ácido clorhídrico, presente en el jugo gástrico a ≈0,1 M. También limpia metales oxidados antes de soldarlos.",
   "svg_key":"HCl"},

  {"id":"HF","name":"Fluoruro de hidrógeno","formula":"HF",
   "atoms":["H","F"],"missing":[1],
   "hints":["7 e⁻ de valencia; elemento más electronegativo.",
            "Grupo 17, Período 2.",
            "Configuración: [He] 2s² 2p⁵"],
   "fun_fact":"El HF disuelve el vidrio (SiO₂ + 4 HF → SiF₄ + 2 H₂O). Se almacena en plástico y se usa para grabar microchips de silicio.",
   "svg_key":"HF"},

  {"id":"HBr","name":"Bromuro de hidrógeno","formula":"HBr",
   "atoms":["H","Br"],"missing":[0],
   "hints":["1 electrón de valencia.",
            "Grupo 1, Período 1.",
            "Configuración completa: 1s¹"],
   "fun_fact":"El HBr es ácido fuerte. En síntesis orgánica se adiciona a alquenos (regla de Markovnikov) para obtener bromuros de alquilo.",
   "svg_key":"HBr"},

  {"id":"HI","name":"Yoduro de hidrógeno","formula":"HI",
   "atoms":["H","I"],"missing":[1],
   "hints":["7 e⁻ de valencia; período 5.",
            "Grupo 17, Período 5.",
            "Configuración: [Kr] 4d¹⁰ 5s² 5p⁵"],
   "fun_fact":"El HI acuoso es el ácido más fuerte de los halácidos. El yodo dietético proviene del yoduro de potasio añadido a la sal de mesa.",
   "svg_key":"HI"},

  {"id":"CO","name":"Monóxido de carbono","formula":"CO",
   "atoms":["C","O"],"missing":[0],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El CO se une a la hemoglobina con 250 × más afinidad que el O₂, bloqueando el transporte de oxígeno. Los detectores de CO salvan miles de vidas al año.",
   "svg_key":"CO"},

  {"id":"NO","name":"Monóxido de nitrógeno","formula":"NO",
   "atoms":["N","O"],"missing":[1],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"El NO es mensajero biológico: dilata vasos sanguíneos. La nitroglicerina actúa liberando NO. El Nobel 1998 fue otorgado por este descubrimiento.",
   "svg_key":"NO"},

  {"id":"Cl2","name":"Cloro molecular","formula":"Cl₂",
   "atoms":["Cl","Cl"],"missing":[0],
   "hints":["7 electrones de valencia.",
            "Grupo 17, Período 3.",
            "Configuración: [Ne] 3s² 3p⁵"],
   "fun_fact":"El Cl₂ fue el primer arma química usada en combate (Ypres, 1915). Hoy purifica el agua potable de más de 2 000 millones de personas.",
   "svg_key":"Cl2"},

  {"id":"Br2","name":"Bromo molecular","formula":"Br₂",
   "atoms":["Br","Br"],"missing":[1],
   "hints":["7 e⁻ de valencia; período 4.",
            "Grupo 17, Período 4.",
            "Configuración: [Ar] 3d¹⁰ 4s² 4p⁵"],
   "fun_fact":"El Br₂ es uno de los dos únicos elementos líquidos a temperatura ambiente. Tiene un olor sofocante y una peligrosa capacidad de penetrar la piel.",
   "svg_key":"Br2"},

  {"id":"I2","name":"Yodo molecular","formula":"I₂",
   "atoms":["I","I"],"missing":[0],
   "hints":["7 e⁻ de valencia; período 5.",
            "Grupo 17, Período 5.",
            "Configuración: [Kr] 4d¹⁰ 5s² 5p⁵"],
   "fun_fact":"El I₂ sublime de sólido a gas violeta directamente. Es esencial para las hormonas tiroideas T3 y T4.",
   "svg_key":"I2"},

  {"id":"NaCl","name":"Cloruro de sodio","formula":"NaCl",
   "atoms":["Na","Cl"],"missing":[0],
   "hints":["1 electrón de valencia, orbital 3s.",
            "Grupo 1 (metal alcalino), Período 3.",
            "Configuración: [Ne] 3s¹"],
   "fun_fact":"La palabra 'salario' viene del latín salarium (pago en sal). El NaCl regula la presión osmótica celular y es esencial para la transmisión nerviosa.",
   "svg_key":"NaCl"},

  {"id":"LiH","name":"Hidruro de litio","formula":"LiH",
   "atoms":["Li","H"],"missing":[0],
   "hints":["1 electrón de valencia, orbital 2s.",
            "Grupo 1, Período 2.",
            "Configuración: [He] 2s¹"],
   "fun_fact":"El LiH (deuteruro de litio-6) es el componente activo de las armas termonucleares. También es reductor en síntesis orgánica y fuente sólida de hidrógeno.",
   "svg_key":"LiH"},

  {"id":"KBr","name":"Bromuro de potasio","formula":"KBr",
   "atoms":["K","Br"],"missing":[0],
   "hints":["1 electrón de valencia, orbital 4s.",
            "Grupo 1, Período 4.",
            "Configuración: [Ar] 4s¹"],
   "fun_fact":"El KBr fue el primer sedante/anticonvulsivo moderno (s. XIX). Como ventana óptica IR, es transparente de 0,25 a 25 µm, ideal para espectroscopía infrarroja.",
   "svg_key":"KBr"},

  {"id":"MgO","name":"Óxido de magnesio","formula":"MgO",
   "atoms":["Mg","O"],"missing":[0],
   "hints":["2 electrones de valencia.",
            "Grupo 2, Período 3.",
            "Configuración: [Ne] 3s²"],
   "fun_fact":"El MgO funde a 2 852 °C, uno de los puntos de fusión más altos. Se usa para recubrir el interior de los hornos de arco eléctrico que fabrican acero.",
   "svg_key":"MgO"},

  {"id":"CaO","name":"Óxido de calcio","formula":"CaO",
   "atoms":["Ca","O"],"missing":[0],
   "hints":["2 electrones de valencia; período 4.",
            "Grupo 2, Período 4.",
            "Configuración: [Ar] 4s²"],
   "fun_fact":"La cal viva (CaO) reacciona violentamente con agua liberando calor. Es fundamental para fabricar cemento Portland y para neutralizar suelos ácidos.",
   "svg_key":"CaO"},

  {"id":"Na2O","name":"Óxido de sodio","formula":"Na₂O",
   "atoms":["Na","Na","O"],"missing":[2],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"El Na₂O aparece en vidrios especiales y es muy reactivo. Al contacto con agua forma NaOH inmediatamente. Se genera como subproducto en la combustión de sodio.",
   "svg_key":"Na2O"},

  {"id":"SO3","name":"Trióxido de azufre","formula":"SO₃",
   "atoms":["S","O","O","O"],"missing":[0],
   "hints":["6 electrones de valencia; período 3.",
            "Grupo 16, Período 3.",
            "Configuración: [Ne] 3s² 3p⁴"],
   "fun_fact":"El SO₃ más agua forma H₂SO₄ en la atmósfera, lo que causa lluvia ácida. Industrialmente se usa para producir ácido sulfúrico en el proceso de contacto.",
   "svg_key":"SO3"},

  {"id":"P4","name":"Fósforo blanco","formula":"P₄",
   "atoms":["P","P","P","P"],"missing":[3],
   "hints":["5 electrones de valencia.",
            "Grupo 15, Período 3.",
            "Configuración: [Ne] 3s² 3p³"],
   "fun_fact":"El P₄ se inflama espontáneamente en el aire y se almacena bajo agua. Fue descubierto en 1669 al destilar orina. La cabeza de los fósforos contiene P rojo, más estable.",
   "svg_key":"P4"},

  {"id":"SiO2","name":"Dióxido de silicio","formula":"SiO₂",
   "atoms":["Si","O","O"],"missing":[0],
   "hints":["4 electrones de valencia; metaloide.",
            "Grupo 14, Período 3.",
            "Configuración: [Ne] 3s² 3p²"],
   "fun_fact":"El SiO₂ es el componente del cuarzo, la arena y el vidrio. Los procesadores de computadora se fabrican con silicio ultrapuro obtenido reduciendo SiO₂ con carbono.",
   "svg_key":"SiO2"},

],  # fin easy


# ══════════════════════════════════════════════════
#  MEDIO — 21 moléculas · faltan 1-2 átomos
# ══════════════════════════════════════════════════
"medium": [

  {"id":"H2O","name":"Agua","formula":"H₂O",
   "atoms":["H","H","O"],"missing":[2],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"El H₂O tiene ángulo de enlace de 104,5° por los pares solitarios del oxígeno. Es el único compuesto natural que existe en los tres estados físicos en la superficie terrestre.",
   "svg_key":"H2O"},

  {"id":"CO2","name":"Dióxido de carbono","formula":"CO₂",
   "atoms":["C","O","O"],"missing":[0,2],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El CO₂ es lineal y apolar aunque sus enlaces C=O son polares (momentos dipolares opuestos se cancelan). Las plantas lo convierten en glucosa mediante fotosíntesis.",
   "svg_key":"CO2"},

  {"id":"NH3","name":"Amoníaco","formula":"NH₃",
   "atoms":["N","H","H","H"],"missing":[1,3],
   "hints":["1 electrón de valencia.",
            "Grupo 1, Período 1.",
            "Configuración completa: 1s¹"],
   "fun_fact":"El proceso Haber-Bosch produce NH₃ con catalizador de Fe a 400 °C y 200 atm. Sin este proceso, la Tierra no podría alimentar a 8 000 millones de personas.",
   "svg_key":"NH3"},

  {"id":"CH4","name":"Metano","formula":"CH₄",
   "atoms":["C","H","H","H","H"],"missing":[0],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El CH₄ tiene geometría tetraédrica perfecta (109,5°). Las vacas emiten ≈100 kg/año por fermentación entérica. En Titán (luna de Saturno) hay ríos y lagos de metano líquido.",
   "svg_key":"CH4"},

  {"id":"SO2","name":"Dióxido de azufre","formula":"SO₂",
   "atoms":["S","O","O"],"missing":[0],
   "hints":["6 electrones de valencia; período 3.",
            "Grupo 16, Período 3.",
            "Configuración: [Ne] 3s² 3p⁴"],
   "fun_fact":"El SO₂ es el conservante E-220 en vinos y frutas secas. Los volcanes liberan megatoneladas. Al mezclarse con vapor de agua forma H₂SO₃ (lluvia ácida).",
   "svg_key":"SO2"},

  {"id":"H2S","name":"Sulfuro de hidrógeno","formula":"H₂S",
   "atoms":["H","H","S"],"missing":[2],
   "hints":["6 electrones de valencia; período 3.",
            "Grupo 16, Período 3.",
            "Configuración: [Ne] 3s² 3p⁴"],
   "fun_fact":"El H₂S huele a huevos podridos y es tan tóxico como el HCN. Bacterias quimioautotróficas en fuentes hidrotermales marinas lo usan como fuente de energía.",
   "svg_key":"H2S"},

  {"id":"NO2","name":"Dióxido de nitrógeno","formula":"NO₂",
   "atoms":["N","O","O"],"missing":[1],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"El NO₂ es un radical libre pardo-rojizo que forma el smog fotoquímico. Dos moléculas se asocian a N₂O₄ incoloro en equilibrio dependiente de la temperatura.",
   "svg_key":"NO2"},

  {"id":"H2O2","name":"Peróxido de hidrógeno","formula":"H₂O₂",
   "atoms":["H","O","O","H"],"missing":[1,2],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"Al 3 % es agua oxigenada antiséptica; al 90 % fue propelente del V-2. El escarabajo bombardero sintetiza H₂O₂ al 25 % para lanzar chorros defensivos hirvientes.",
   "svg_key":"H2O2"},

  {"id":"N2O","name":"Óxido nitroso","formula":"N₂O",
   "atoms":["N","N","O"],"missing":[2],
   "hints":["6 electrones de valencia.",
            "Grupo 16, Período 2.",
            "Configuración: [He] 2s² 2p⁴"],
   "fun_fact":"El N₂O es el 'gas de la risa', anestésico desde 1844. Es 300 × más potente como gas de invernadero que el CO₂ y se usa para turboalimentar motores de competición.",
   "svg_key":"N2O"},

  {"id":"C2H2","name":"Acetileno (etino)","formula":"C₂H₂",
   "atoms":["C","C","H","H"],"missing":[0,1],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El C₂H₂ tiene triple enlace C≡C (hibridación sp, 180°). La llama oxiacetilénica alcanza 3 500 °C, la más caliente obtenible con un soplete de gas convencional.",
   "svg_key":"C2H2"},

  {"id":"C2H4","name":"Etileno (eteno)","formula":"C₂H₄",
   "atoms":["C","C","H","H","H","H"],"missing":[0],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El etileno es la hormona de maduración de las frutas. Se inyecta en cámaras frigoríficas para madurar plátanos verdes. El polietileno (plásticos) se fabrica polimerizando C₂H₄.",
   "svg_key":"C2H4"},

  {"id":"C2H6","name":"Etano","formula":"C₂H₆",
   "atoms":["C","C","H","H","H","H","H","H"],"missing":[0],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El etano es el segundo componente del gas natural (~10 %). A -89 °C se licúa y se separa criogénicamente para producir etileno, el monómero del polietileno.",
   "svg_key":"C2H6"},

  {"id":"CH3OH","name":"Metanol","formula":"CH₃OH",
   "atoms":["C","H","H","H","O","H"],"missing":[0,4],
   "hints":["Pos. 1 (C): 4 e⁻ de valencia.  Pos. 5 (O): 6 e⁻ de valencia.",
            "C: Grupo 14, P2.  O: Grupo 16, P2.",
            "C: [He] 2s² 2p²  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El metanol es muy tóxico: 10 mL causan ceguera y 30 mL pueden ser letales. Es base del biodiesel, anticongelante de tuberías y combustible histórico de la Fórmula 1.",
   "svg_key":"CH3OH"},

  {"id":"HCHO","name":"Formaldehído","formula":"HCHO",
   "atoms":["H","C","H","O"],"missing":[1],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"La formalina (37 % en agua) conserva tejidos biológicos desde el s. XIX. Es cancerígeno Grupo 1 (IARC). También se usa para producir resinas de melamina y madera contrachapada.",
   "svg_key":"HCHO"},

  {"id":"N2H4","name":"Hidracina","formula":"N₂H₄",
   "atoms":["N","N","H","H","H","H"],"missing":[0,1],
   "hints":["5 electrones de valencia.",
            "Grupo 15, Período 2.",
            "Configuración: [He] 2s² 2p³"],
   "fun_fact":"La hidracina fue el propelente del Transbordador Espacial (maniobras). Hoy propulsa satélites en correcciones orbitales. Es muy tóxica, cancerígena y explosiva.",
   "svg_key":"N2H4"},

  {"id":"CCl4","name":"Tetracloruro de carbono","formula":"CCl₄",
   "atoms":["C","Cl","Cl","Cl","Cl"],"missing":[0],
   "hints":["4 electrones de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El CCl₄ fue el primer extintor portátil (1900) y disolvente de tintorería. Se prohibió al confirmarse que destruye la capa de ozono y es hepatotóxico (causa cáncer de hígado).",
   "svg_key":"CCl4"},

  {"id":"PCl3","name":"Tricloruro de fósforo","formula":"PCl₃",
   "atoms":["P","Cl","Cl","Cl"],"missing":[0],
   "hints":["5 electrones de valencia.",
            "Grupo 15, Período 3.",
            "Configuración: [Ne] 3s² 3p³"],
   "fun_fact":"El PCl₃ tiene geometría piramidal y es precursor de pesticidas organofosforados. Lamentablemente también es el punto de partida para la síntesis de agentes nerviosos (sarín, VX).",
   "svg_key":"PCl3"},

  {"id":"SF6","name":"Hexafluoruro de azufre","formula":"SF₆",
   "atoms":["S","F","F","F","F","F","F"],"missing":[0],
   "hints":["6 electrones de valencia; período 3.",
            "Grupo 16, Período 3.",
            "Configuración: [Ne] 3s² 3p⁴"],
   "fun_fact":"El SF₆ es el gas de invernadero más potente (23 500 × CO₂). Se usa en interruptores de alta tensión porque no conduce ni se ioniza. Inhalarlo baja el tono de la voz (contrario al helio).",
   "svg_key":"SF6"},

  {"id":"PH3","name":"Fosfina","formula":"PH₃",
   "atoms":["P","H","H","H"],"missing":[0],
   "hints":["5 electrones de valencia.",
            "Grupo 15, Período 3.",
            "Configuración: [Ne] 3s² 3p³"],
   "fun_fact":"La PH₃ fue detectada en Venus en 2020, sugiriendo posible actividad biológica o geológica desconocida. En la Tierra la producen bacterias anaeróbicas en pantanos y rellenos sanitarios.",
   "svg_key":"PH3"},

  {"id":"SiH4","name":"Silano","formula":"SiH₄",
   "atoms":["Si","H","H","H","H"],"missing":[0],
   "hints":["4 electrones de valencia; metaloide.",
            "Grupo 14, Período 3.",
            "Configuración: [Ne] 3s² 3p²"],
   "fun_fact":"El SiH₄ se usa para depositar capas ultrafinas de silicio puro (proceso CVD) en la fabricación de paneles solares y semiconductores de última generación.",
   "svg_key":"SiH4"},

  {"id":"BH3","name":"Borano","formula":"BH₃",
   "atoms":["B","H","H","H"],"missing":[0],
   "hints":["3 electrones de valencia.",
            "Grupo 13, Período 2.",
            "Configuración: [He] 2s² 2p¹"],
   "fun_fact":"El BH₃ libre es inestable y dimeriza a B₂H₆ (diborano). Como ácido de Lewis muy fuerte (boro con solo 6 e⁻), acepta pares de electrones y se usa como agente hidroborador en síntesis orgánica.",
   "svg_key":"BH3"},

],  # fin medium


# ══════════════════════════════════════════════════
#  DIFÍCIL — 21 moléculas · faltan 2-3 átomos
# ══════════════════════════════════════════════════
"hard": [

  {"id":"H2SO4","name":"Ácido sulfúrico","formula":"H₂SO₄",
   "atoms":["H","H","S","O","O","O","O"],"missing":[2,3],
   "hints":["Pos. 3 (S): 6 e⁻ valencia, período 3.  Pos. 4 (O): 6 e⁻ de valencia.",
            "S: Grupo 16, Período 3.  O: Grupo 16, Período 2.",
            "S: [Ne] 3s² 3p⁴  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El H₂SO₄ es el compuesto industrial más producido (≈200 Mt/año). Se usa en fertilizantes, baterías de plomo, refino de petróleo y síntesis de casi todo lo demás en química industrial.",
   "svg_key":"H2SO4"},

  {"id":"HNO3","name":"Ácido nítrico","formula":"HNO₃",
   "atoms":["H","N","O","O","O"],"missing":[1,4],
   "hints":["Pos. 2 (N): 5 e⁻ de valencia.",
            "Grupo 15, Período 2.",
            "Configuración: [He] 2s² 2p³"],
   "fun_fact":"El HNO₃ es esencial para explosivos (TNT, nitroglicerina) y fertilizantes. La mezcla 1:3 con HCl (agua regia) disuelve oro y platino, los metales más resistentes.",
   "svg_key":"HNO3"},

  {"id":"H3PO4","name":"Ácido fosfórico","formula":"H₃PO₄",
   "atoms":["H","H","H","P","O","O","O","O"],"missing":[3,7],
   "hints":["Pos. 4 (P): 5 e⁻ de valencia.  Pos. 8 (O): 6 e⁻ de valencia.",
            "P: Grupo 15, P3.  O: Grupo 16, P2.",
            "P: [Ne] 3s² 3p³  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El H₃PO₄ le da el sabor ácido a las colas. El 90 % de la producción mundial va a fertilizantes fosfatados. El ATP (energía celular) contiene tres grupos fosfato.",
   "svg_key":"H3PO4"},

  {"id":"C2H5OH","name":"Etanol","formula":"C₂H₅OH",
   "atoms":["C","C","H","H","H","H","H","O","H"],"missing":[0,7],
   "hints":["Pos. 1 (C): 4 e⁻ de valencia.  Pos. 8 (O): 6 e⁻ de valencia.",
            "C: Grupo 14, P2.  O: Grupo 16, P2.",
            "C: [He] 2s² 2p²  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El etanol se produce por fermentación desde hace 9 000 años. Brasil produce 30 000 millones de litros/año de bioetanol de caña de azúcar como combustible renovable.",
   "svg_key":"C2H5OH"},

  {"id":"CH3COOH","name":"Ácido acético","formula":"CH₃COOH",
   "atoms":["C","H","H","H","C","O","O","H"],"missing":[0,5],
   "hints":["Ambos átomos faltantes tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El vinagre es 5-8 % CH₃COOH. Los sumerios ya lo producían hace 5 000 años. Es clave en bioquímica: el acetil-CoA transporta grupos acetilo en el ciclo de Krebs.",
   "svg_key":"CH3COOH"},

  {"id":"NaOH","name":"Hidróxido de sodio","formula":"NaOH",
   "atoms":["Na","O","H"],"missing":[1,2],
   "hints":["Pos. 2 (O): 6 e⁻ de valencia, Grupo 16, P2.  Pos. 3 (H): 1 e⁻, Grupo 1, P1.",
            "O: Período 2.  H: Período 1.",
            "O: [He] 2s² 2p⁴  |  H: 1s¹"],
   "fun_fact":"La soda cáustica se produce electrolizando salmuera (proceso cloro-álcali). Disuelve tejido orgánico, grasa y papel. Se usa en jabones, tratamiento de aguas y limpieza de tuberías.",
   "svg_key":"NaOH"},

  {"id":"MgCl2","name":"Cloruro de magnesio","formula":"MgCl₂",
   "atoms":["Mg","Cl","Cl"],"missing":[0],
   "hints":["2 electrones de valencia.",
            "Grupo 2, Período 3.",
            "Configuración: [Ne] 3s²"],
   "fun_fact":"El nigari (MgCl₂ del agua de mar japonesa) coagula la soja para hacer tofu desde hace 2 000 años. También funde hielo en carreteras sin dañar la vegetación como la sal común.",
   "svg_key":"MgCl2"},

  {"id":"CaCO3","name":"Carbonato de calcio","formula":"CaCO₃",
   "atoms":["Ca","C","O","O","O"],"missing":[1,4],
   "hints":["Pos. 2 (C): 4 e⁻ de valencia.  Pos. 5 (O): 6 e⁻ de valencia.",
            "C: Grupo 14, P2.  O: Grupo 16, P2.",
            "C: [He] 2s² 2p²  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El CaCO₃ forma mármol, caliza y arrecifes de coral. Los océanos son el mayor sumidero de CO₂: lo fijan como bicarbonato y carbonato calcico en sedimentos marinos.",
   "svg_key":"CaCO3"},

  {"id":"C3H8","name":"Propano","formula":"C₃H₈",
   "atoms":["C","C","C","H","H","H","H","H","H","H","H"],"missing":[0,2],
   "hints":["Ambos tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El propano (GLP) de las bombonas azules se licúa a solo 8 atm a 20 °C. Arde con 2 220 kJ/mol. En América del Norte calienta millones de hogares rurales sin acceso a gas de red.",
   "svg_key":"C3H8"},

  {"id":"C4H10","name":"Butano","formula":"C₄H₁₀",
   "atoms":["C","C","C","C","H","H","H","H","H","H","H","H","H","H"],"missing":[0,3],
   "hints":["Ambos tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El n-butano es el gas de los mecheros desechables. A -0,5 °C ya es líquido. El isobutano (isómero de ramificación) es refrigerante ecológico R600a en neveras modernas.",
   "svg_key":"C4H10"},

  {"id":"C6H6","name":"Benceno","formula":"C₆H₆",
   "atoms":["C","C","C","C","C","C","H","H","H","H","H","H"],"missing":[0,3],
   "hints":["Ambos tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"Kekulé soñó la estructura cíclica del benceno (1865) visualizando una serpiente mordiéndose la cola. El anillo aromático con electrones π deslocalizados le da estabilidad excepcional.",
   "svg_key":"C6H6"},

  {"id":"CH3COCH3","name":"Acetona","formula":"CH₃COCH₃",
   "atoms":["C","H","H","H","C","O","C","H","H","H"],"missing":[0,4,6],
   "hints":["Los 3 átomos faltantes tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"La acetona es el disolvente orgánico más producido del mundo. El cuerpo la genera durante la cetosis. Está presente en quitaesmaltes; su olor dulce delata derrames en el laboratorio.",
   "svg_key":"CH3COCH3"},

  {"id":"NH4NO3","name":"Nitrato de amonio","formula":"NH₄NO₃",
   "atoms":["N","H","H","H","H","N","O","O","O"],"missing":[0,5],
   "hints":["Ambos átomos tienen 5 e⁻ de valencia.",
            "Grupo 15, Período 2.",
            "Configuración: [He] 2s² 2p³"],
   "fun_fact":"El NH₄NO₃ es el fertilizante nitrogenado más usado del mundo, pero también un explosivo potente. Las tragedias de Texas City (1947) y Beirut (2020) fueron detonaciones accidentales.",
   "svg_key":"NH4NO3"},

  {"id":"C6H5OH","name":"Fenol","formula":"C₆H₅OH",
   "atoms":["C","C","C","C","C","C","H","H","H","H","H","O","H"],"missing":[0,11],
   "hints":["Pos. 1 (C): 4 e⁻ de valencia.  Pos. 12 (O): 6 e⁻ de valencia.",
            "C: Grupo 14, P2.  O: Grupo 16, P2.",
            "C: [He] 2s² 2p²  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El fenol fue el primer antiséptico quirúrgico (Lister, 1867). Hoy es materia prima de la baquelita (primer plástico sintético, 1907) y de la aspirina.",
   "svg_key":"C6H5OH"},

  {"id":"C6H5CH3","name":"Tolueno","formula":"C₆H₅CH₃",
   "atoms":["C","C","C","C","C","C","C","H","H","H","H","H","H","H","H"],"missing":[0,6],
   "hints":["Ambos tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El tolueno es el precursor del TNT (2,4,6-trinitrotolueno). También es disolvente de pinturas y pegamentos. Su inhalación crónica provoca daño neurológico permanente.",
   "svg_key":"C6H5CH3"},

  {"id":"C6H5NH2","name":"Anilina","formula":"C₆H₅NH₂",
   "atoms":["C","C","C","C","C","C","H","H","H","H","H","N","H","H"],"missing":[0,11],
   "hints":["Pos. 1 (C): 4 e⁻ de valencia.  Pos. 12 (N): 5 e⁻ de valencia.",
            "C: Grupo 14, P2.  N: Grupo 15, P2.",
            "C: [He] 2s² 2p²  |  N: [He] 2s² 2p³"],
   "fun_fact":"En 1856 Perkin, intentando sintetizar quinina con anilina, obtuvo accidentalmente malveína, el primer colorante sintético. Así nació la industria química moderna de los tintes.",
   "svg_key":"C6H5NH2"},

  {"id":"C6H5NO2","name":"Nitrobenceno","formula":"C₆H₅NO₂",
   "atoms":["C","C","C","C","C","C","H","H","H","H","H","N","O","O"],"missing":[0,11],
   "hints":["Pos. 1 (C): 4 e⁻ de valencia.  Pos. 12 (N): 5 e⁻ de valencia.",
            "C: Grupo 14, P2.  N: Grupo 15, P2.",
            "C: [He] 2s² 2p²  |  N: [He] 2s² 2p³"],
   "fun_fact":"El nitrobenceno huele a almendras amargas y es muy tóxico: cruza la piel convirtiendo la hemoglobina en metahemoglobina. Es el precursor industrial de la anilina y los colorantes sintéticos.",
   "svg_key":"C6H5NO2"},

  {"id":"C2H5OC2H5","name":"Éter dietílico","formula":"C₂H₅OC₂H₅",
   "atoms":["C","C","O","C","C","H","H","H","H","H","H","H","H","H","H"],"missing":[0,2,3],
   "hints":["Pos. 1 y 4 (C): 4 e⁻ de valencia.  Pos. 3 (O): 6 e⁻ de valencia.",
            "C: Grupo 14, P2.  O: Grupo 16, P2.",
            "C: [He] 2s² 2p²  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El éter dietílico fue el primer anestésico general exitoso (1842). Es tan inflamable que su vapor puede recorrer metros hasta una chispa. Hoy se usa como disolvente en extracciones orgánicas.",
   "svg_key":"C2H5OC2H5"},

  {"id":"HCOOH","name":"Ácido fórmico","formula":"HCOOH",
   "atoms":["H","C","O","O","H"],"missing":[1,3],
   "hints":["Pos. 2 (C): 4 e⁻ de valencia.  Pos. 4 (O): 6 e⁻ de valencia.",
            "C: Grupo 14, P2.  O: Grupo 16, P2.",
            "C: [He] 2s² 2p²  |  O: [He] 2s² 2p⁴"],
   "fun_fact":"El ácido fórmico (del latín formica, hormiga) es el veneno de las hormigas y las ortigas. Se usa para preservar forraje en silos y como antibacteriano natural en apicultura.",
   "svg_key":"HCOOH"},

  {"id":"CH3NH2","name":"Metilamina","formula":"CH₃NH₂",
   "atoms":["C","H","H","H","N","H","H"],"missing":[0,4],
   "hints":["Pos. 1 (C): 4 e⁻ de valencia.  Pos. 5 (N): 5 e⁻ de valencia.",
            "C: Grupo 14, P2.  N: Grupo 15, P2.",
            "C: [He] 2s² 2p²  |  N: [He] 2s² 2p³"],
   "fun_fact":"La metilamina huele a pescado en descomposición. Ha sido detectada en nubes moleculares interestelares, lo que sugiere que la química orgánica es universal. Es también precursora de muchos fármacos.",
   "svg_key":"CH3NH2"},

  {"id":"C8H18","name":"Octano","formula":"C₈H₁₈",
   "atoms":["C","C","C","C","C","C","C","C",
            "H","H","H","H","H","H","H","H","H","H"],"missing":[0,7],
   "hints":["Ambos tienen 4 e⁻ de valencia.",
            "Grupo 14, Período 2.",
            "Configuración: [He] 2s² 2p²"],
   "fun_fact":"El iso-octano (2,2,4-trimetilpentano) fue fijado arbitrariamente como referencia de 100 octanos. El número de octanaje indica la resistencia de la gasolina a la detonación prematura en el motor.",
   "svg_key":"C8H18"},

],  # fin hard
}  # fin MOLECULES


# ═══════════════════════════════════════════════════════════
#  LÓGICA DE JUEGO — idéntica a la original (drop-in safe)
# ═══════════════════════════════════════════════════════════

LEVEL_LABELS = {"easy": "Fácil", "medium": "Medio", "hard": "Difícil"}


class GameSession:
    MAX_HINTS = 3

    def __init__(self, level: str):
        if level not in MOLECULES:
            raise ValueError(f"Nivel '{level}' inválido.")
        self.level         = level
        self.molecules     = MOLECULES[level]
        self.current_index = 0
        self.score         = 0
        self.hints_used    = 0
        self.attempts      = 0

    @property
    def current_molecule(self):
        return self.molecules[self.current_index] if self.current_index < len(self.molecules) else None

    @property
    def is_finished(self):
        return self.current_index >= len(self.molecules)

    @property
    def hints_remaining(self):
        return self.MAX_HINTS - self.hints_used

    def get_display_atoms(self):
        mol = self.current_molecule
        if not mol:
            return []
        return [
            {"symbol": "?", "missing": True,  "index": i} if i in mol["missing"]
            else {"symbol": sym, "missing": False, "index": i}
            for i, sym in enumerate(mol["atoms"])
        ]

    def request_hint(self):
        mol = self.current_molecule
        if not mol:
            return {"ok": False, "msg": "Sin molécula activa."}
        if self.hints_used >= self.MAX_HINTS:
            return {"ok": False, "msg": "Sin pistas restantes."}
        hint_text = mol["hints"][self.hints_used]
        self.hints_used += 1
        return {"ok": True, "hint": hint_text,
                "hint_number": self.hints_used, "remaining": self.hints_remaining}

    def submit_answer(self, slot_index: int, element_symbol: str):
        mol = self.current_molecule
        if not mol:
            return {"ok": False, "correct": False}
        expected = mol["atoms"][slot_index]
        self.attempts += 1
        correct = element_symbol.strip().capitalize() == expected
        return {"ok": True, "correct": correct, "expected": expected}

    def complete_molecule(self):
        pts = max(10 - self.hints_used * 3, 1)
        self.score        += pts
        self.current_index += 1
        self.hints_used    = 0
        self.attempts      = 0
        return {"points_earned": pts, "total_score": self.score}

    def reset(self):
        self.current_index = 0
        self.score         = 0
        self.hints_used    = 0
        self.attempts      = 0


def get_molecule_list(level: str) -> list:
    return [{"id": m["id"], "name": m["name"], "formula": m["formula"]}
            for m in MOLECULES.get(level, [])]

def get_molecule_by_id(mol_id: str):
    for level_mols in MOLECULES.values():
        for m in level_mols:
            if m["id"] == mol_id:
                return m
    return None

def score_for_hints(hints_used: int) -> int:
    return {0: 10, 1: 7, 2: 4, 3: 1}.get(min(hints_used, 3), 1)
