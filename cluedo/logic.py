import openai
import os
import random
from .models import GameState

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


CASES = [
    {
        "id": 1,
        "title": "Asesinato en la mansión",
        "description": "Esta noche hubo un asesinato en la mansión. El cuerpo fue encontrado en la biblioteca con signos de lucha.",
        "details": (
            "El mayordomo estaba ausente a las 11pm. "
            "La jardinera vio una sombra sospechosa cerca de la biblioteca. "
            "El vecino curioso merodeaba por los pasillos intentando escuchar conversaciones. "
            "El detective retirado había sido invitado por la víctima para una consulta privada. "
            "El periodista llegó inesperadamente, buscando una exclusiva. "
            "El chef discutió con la víctima por un cambio de menú de última hora. "
            "La anciana afirmó haber visto a alguien salir corriendo, pero no recuerda quién. "
            "El niño prodigio encontró una pluma ensangrentada bajo una alfombra."
        )
    },
    {
        "id": 2,
        "title": "El misterio del robo",
        "description": "Un valioso diamante desapareció durante la fiesta en la villa.",
        "details": (
            "El chef estaba en la cocina pero parecía nervioso. "
            "El vecino tenía una coartada dudosa. "
            "El mayordomo fue quien recibió al joyero esa noche. "
            "La jardinera encontró tierra suelta cerca de la caja fuerte. "
            "El detective retirado señaló que alguien había manipulado las cámaras. "
            "La anciana confundió la caja del diamante con una caja de bombones. "
            "El periodista fue sorprendido husmeando en el despacho. "
            "El niño prodigio descubrió una huella pequeña en el cristal del expositor."
        )
    },
    {
        "id": 3,
        "title": "El secreto del sótano",
        "description": "Se encontraron huellas extrañas en el sótano de la casa.",
        "details": (
            "La anciana escuchó ruidos extraños a medianoche. "
            "El periodista investigaba un caso antiguo relacionado con la familia. "
            "El chef bajó a buscar un vino raro, pero tardó más de lo normal. "
            "El mayordomo guardaba documentos en una caja oculta. "
            "La jardinera dejó herramientas olvidadas allí días antes. "
            "El vecino vio luces encenderse cuando todos dormían. "
            "El detective retirado sospechó que se usó una entrada secreta. "
            "El niño prodigio halló símbolos escritos con tiza en la pared."
        )
    },
    {
        "id": 4,
        "title": "La desaparición del testigo",
        "description": "Un testigo clave desapareció justo antes del juicio.",
        "details": (
            "El niño prodigio vio una figura sospechosa saliendo por la puerta trasera. "
            "El detective retirado estaba vigilando la zona por encargo. "
            "El periodista había contactado al testigo para una entrevista. "
            "La jardinera escuchó un grito ahogado cerca del invernadero. "
            "El mayordomo dijo haber preparado la habitación del testigo. "
            "El chef notó que faltaba comida del refrigerador. "
            "La anciana dijo que alguien entró en su habitación confundido. "
            "El vecino se ofreció a ayudar con la búsqueda, pero desapareció por horas."
        )
    },
    {
        "id": 5,
        "title": "El veneno en la cena",
        "description": "Alguien fue envenenado durante la cena de gala.",
        "details": (
            "El chef preparó el plato principal con ingredientes inusuales. "
            "La jardinera manipuló las flores que decoraban la mesa. "
            "El mayordomo sirvió el vino, pero no bebió nada. "
            "El periodista estaba investigando a uno de los invitados. "
            "La anciana notó un sabor extraño en su sopa, pero no dijo nada. "
            "El detective retirado revisó la cocina tras el incidente. "
            "El niño prodigio detectó un patrón en los platos afectados. "
            "El vecino fue visto con una caja misteriosa cerca de la despensa."
        )
    },
    {
        "id": 6,
        "title": "La carta anónima",
        "description": "Una carta anónima amenazante fue recibida por la víctima.",
        "details": (
            "El mayordomo encontró la carta en el despacho. "
            "El vecino actuó de manera nerviosa tras la llegada del sobre. "
            "El periodista reconoció el tipo de letra usada. "
            "La jardinera dijo haber visto a alguien merodear por el buzón. "
            "El chef negó saber escribir a máquina, pero tenía tinta en las manos. "
            "La anciana creyó que era una carta de amor mal escrita. "
            "El detective retirado detectó que la carta usaba papel del archivo familiar. "
            "El niño prodigio descubrió que el sobre había sido manipulado con guantes."
        )
    },
    {
        "id": 7,
        "title": "El robo del cuadro",
        "description": "Un cuadro valioso desapareció sin dejar rastro.",
        "details": (
            "La anciana cuidaba la galería, pero se quedó dormida. "
            "El periodista había estado investigando al dueño del cuadro. "
            "El mayordomo tenía la llave del salón donde colgaba la obra. "
            "La jardinera limpiaba una planta cercana y escuchó un ruido sordo. "
            "El chef fue visto en la galería, buscando especias para una receta. "
            "El vecino aseguró haber visto una figura encapuchada. "
            "El detective retirado notó que la alarma fue desactivada manualmente. "
            "El niño prodigio encontró restos de pintura en el suelo."
        )
    },
        {
        "id": 8,
        "title": "El último brindis",
        "description": "El anfitrión cayó fulminado tras proponer un brindis en la cena de gala. Su copa de champán contenía un potente veneno inodoro.",
        "details": (
            "El mayordomo fue quien sirvió las copas desde una bandeja de plata. "
            "El chef tenía acceso a veneno para ratas en la despensa de la cocina. "
            "La anciana estaba sentada a su derecha y se le vio intercambiar las copas. "
            "El periodista distrajo a todos con un flashazo justo antes del brindis. "
            "El detective retirado notó un olor a almendras amargas, pero calló. "
            "El vecino trajo su propia botella de vino y la ofreció insistentemente. "
            "La jardinera cultiva adelfas venenosas en el patio trasero. "
            "El niño prodigio recogió la copa vacía antes de que la policía la analizara."
        )
    },
    {
        "id": 9,
        "title": "La caída fatal",
        "description": "La víctima fue encontrada al pie de la gran escalera de mármol. Parece un accidente, pero el pasamanos estaba aflojado intencionalmente.",
        "details": (
            "El vecino fue visto subiendo las escaleras con una caja de herramientas. "
            "La jardinera limpió el piso superior con cera extra deslizante. "
            "El detective retirado estaba en el rellano y escuchó una discusión previa. "
            "El mayordomo asegura que la alfombra de la escalera estaba bien colocada antes. "
            "El niño prodigio estaba jugando con canicas cerca del borde de los escalones. "
            "El periodista tomó fotos del cadáver desde un ángulo sospechosamente perfecto. "
            "La anciana dice que vio un 'fantasma' empujando a la víctima. "
            "El chef tenía una vieja rencilla con la víctima por un préstamo no devuelto."
        )
    },
    {
        "id":10,
        "title": "Crimen en el cuarto oscuro",
        "description": "Durante el revelado de fotografías en el laboratorio casero, alguien apuñaló a la víctima aprovechando la total oscuridad y el ruido del extractor de aire.",
        "details": (
            "El periodista era el único que sabía usar el equipo de revelado. "
            "La anciana entró por error buscando el baño y escuchó un gemido. "
            "El mayordomo cerró la puerta con llave desde fuera 'por costumbre'. "
            "El vecino tiene una colección de cuchillos que coincide con la herida. "
            "El niño prodigio cortó la electricidad de la casa por unos segundos. "
            "El chef estaba limpiando pescado cerca y tenía las manos manchadas de rojo. "
            "La jardinera necesitaba químicos del laboratorio para sus fertilizantes. "
            "El detective retirado encontró huellas dactilares borradas en el interruptor."
        )
    },
    {
        "id": 11,
        "title": "Ahogado en la fuente",
        "description": "A la mañana siguiente, el cuerpo del abogado de la familia apareció flotando en la fuente ornamental del jardín, con un golpe en la nuca.",
        "details": (
            "La jardinera fue la primera en llegar y tenía las botas empapadas. "
            "El detective retirado encontró un trozo de tela enganchado en una estatua. "
            "El mayordomo discutió con el abogado sobre su salario la noche anterior. "
            "El vecino fue visto saltando la valla del jardín a medianoche. "
            "El chef admite haber tirado restos de comida cerca de la fuente. "
            "La anciana escuchó un chapoteo, pero pensó que era el perro. "
            "El periodista buscaba documentos que el abogado llevaba en su maletín. "
            "El niño prodigio estaba probando su barco teledirigido en esa misma fuente."
        )
    },
    {
        "id": 12,
        "title": "La daga ceremonial",
        "description": "El coleccionista de antigüedades fue hallado muerto en su estudio. La vitrina está rota y falta una valiosa daga persa, el arma del crimen.",
        "details": (
            "El detective retirado sabía exactamente cuánto valía esa daga. "
            "El mayordomo tenía la única copia de la llave de la vitrina. "
            "El vecino había ofrecido comprar la daga tres veces y fue rechazado. "
            "La jardinera entró por la ventana del estudio para regar los helechos. "
            "El periodista escribió un artículo exponiendo que la daga era robada. "
            "La anciana limpió los cristales rotos antes de que llegara nadie. "
            "El niño prodigio dibujó la daga en su cuaderno con detalles inquietantes. "
            "El chef usó un cuchillo muy similar para cortar el asado de la cena."
        )
    },
    {
        "id": 13,
        "title": "Muerte en el baño turco",
        "description": "La víctima quedó encerrada en la sauna de la mansión. Alguien bloqueó la puerta y subió la temperatura al máximo, provocando un fallo cardíaco.",
        "details": (
            "El mayordomo encendió la sauna, pero jura que la dejó a temperatura media. "
            "El chef se quejó del vapor que entraba en su cocina contigua. "
            "El vecino es electricista y sabe cómo puentear el termostato. "
            "La anciana dice que vio a alguien poner una silla atrancando la puerta. "
            "El detective retirado encontró un cronómetro cerca de la entrada. "
            "La jardinera usaba la sauna para secar hierbas aromáticas en secreto. "
            "El periodista tenía una cita con la víctima en el spa, pero no se presentó. "
            "El niño prodigio sabe la combinación numérica del panel de control."
        )
    },
    {
        "id": 14,
        "title": "La partida de póker",
        "description": "En medio de una partida de cartas de altas apuestas, se fue la luz. Al volver, el ganador yacía muerto sobre la mesa con las fichas esparcidas.",
        "details": (
            "El vecino había perdido una fortuna contra la víctima minutos antes. "
            "El mayordomo sostenía un candelabro pesado que tiene manchas sospechosas. "
            "El detective retirado estaba vigilando la partida para evitar trampas. "
            "El chef sirvió whisky y vio quién tenía la mejor mano. "
            "La jardinera cortó las rosas exteriores y pudo haber cortado el cable de luz. "
            "El periodista estaba escondido debajo de la mesa grabando la partida. "
            "La anciana dice que la víctima le guiñó el ojo antes de morir. "
            "El niño prodigio contó las cartas y sabía que la víctima estaba haciendo trampa."
        )
    },
    {
        "id": 15,
        "title": "El accidente de caza",
        "description": "En la sala de trofeos, una escopeta antigua que debía estar descargada se disparó 'accidentalmente' mientras la víctima la limpiaba.",
        "details": (
            "El detective retirado revisó el arma ayer y aseguró que era segura. "
            "El mayordomo entregó el kit de limpieza a la víctima. "
            "El vecino es un experto tirador y odiaba a la víctima. "
            "El niño prodigio encontró cartuchos vivos en el cubo de basura. "
            "La anciana estaba en la habitación de al lado y no escuchó el disparo. "
            "El periodista escribió sobre la venta ilegal de armas de la familia. "
            "La jardinera vio a alguien salir corriendo por la ventana de la sala. "
            "El chef usó pólvora para un truco de cocina flambé esa noche."
        )
    },
    {
        "id": 16,
        "title": "El collar de perlas",
        "description": "La dueña de la casa fue estrangulada con su propio collar de perlas. Las perlas rodaron por todo el suelo del dormitorio, haciendo caer al asesino.",
        "details": (
            "La anciana codiciaba ese collar desde hacía cincuenta años. "
            "El mayordomo tiene un moretón en la rodilla, como si se hubiera caído. "
            "El periodista encontró una perla en su bolsillo y no sabe cómo llegó ahí. "
            "La jardinera barrió el pasillo y encontró el cierre roto del collar. "
            "El detective retirado analizó el nudo y dijo que era de estilo marinero. "
            "El vecino fue visto en una casa de empeños preguntando por perlas. "
            "El niño prodigio estaba haciendo un collar falso con cuentas de plástico. "
            "El chef llevó el desayuno a la cama y encontró el cuerpo primero."
        )
    },
        {
        "id": 17,
        "title": "El secreto del armario",
        "description": "El patriarca de la familia fue encontrado muerto en su despacho justo antes de publicar sus memorias, donde planeaba revelar su relación secreta de 40 años con su 'mejor amigo'.",
        "details": (
            "La anciana (su esposa) sabía la verdad y temía el escándalo social. "
            "El mayordomo era ese 'mejor amigo' y heredero secreto, ahora principal sospechoso. "
            "El vecino chantajeaba a la víctima con fotos antiguas de ambos hombres. "
            "El periodista quería la exclusiva y forzó la caja fuerte buscando el manuscrito. "
            "El detective retirado investigó el pasado de la víctima por encargo de los hijos. "
            "El niño prodigio encontró una carta de amor a medio quemar en la chimenea. "
            "La jardinera escuchó una pelea sobre 'arruinar la reputación de la familia'. "
            "El chef preparó una cena romántica para dos hombres esa noche, que nadie probó."
        )
    },
    {
        "id": 18,
        "title": "La diva silenciada",
        "description": "Durante una fiesta privada, la famosa Drag Queen 'Lady Diamond' fue envenenada en su camerino improvisado. Su peluca ocultaba un documento crucial.",
        "details": (
            "El periodista era una expareja rencorosa que fue ridiculizada en el show. "
            "La anciana se ofendió por la actuación y fue vista manipulando las bebidas. "
            "El niño prodigio vio a alguien poner polvo en el maquillaje de la artista. "
            "El chef odiaba a la víctima por una crítica mordaz a su catering en el pasado. "
            "El vecino es un político conservador que temía ser reconocido por la artista. "
            "El mayordomo ayudó a la víctima a vestirse y fue el último en verla viva. "
            "La jardinera encontró las tacones de la víctima rotos intencionalmente en el jardín. "
            "El detective retirado descubrió que 'Lady Diamond' era en realidad el heredero desaparecido de la mansión."
        )
    },
    {
        "id": 19,
        "title": "La boda interrumpida",
        "description": "Iba a celebrarse la primera boda entre dos mujeres en la historia de la mansión, pero una de las novias desapareció y se hallaron restos de sangre en el altar.",
        "details": (
            "El vecino estaba enamorado obsesivamente de una de las novias. "
            "La jardinera, ex-pareja de la víctima, estaba podando arbustos cerca del altar. "
            "El mayordomo se oponía a la boda alegando 'tradiciones familiares'. "
            "El chef discutió con la pareja por el diseño del pastel nupcial. "
            "La anciana amenazó con desheredar a su nieta si la boda continuaba. "
            "El periodista se coló en la ceremonia buscando drama familiar. "
            "El detective retirado encontró el velo rasgado y manchado en el sótano. "
            "El niño prodigio vio a alguien huir en el coche de los recien casados."
        )
    },
    {
        "id": 20,
        "title": "El cambio de testamento",
        "description": "El tío millonario anunció que dejaría toda su fortuna a una fundación de apoyo a jóvenes trans, desheredando a su familia. Esa misma noche fue empujado por el balcón.",
        "details": (
            "El sobrino (representado por el vecino) estaba furioso por perder la herencia. "
            "El mayordomo fue testigo de la firma del nuevo testamento. "
            "La anciana creía que la fundación era una estafa y quería 'proteger' el dinero. "
            "El periodista investigaba las finanzas de la fundación en secreto. "
            "El chef temía perder su empleo si la mansión se convertía en sede de la ONG. "
            "La jardinera es voluntaria en la fundación y visitó a la víctima esa noche. "
            "El detective retirado notó que la barandilla del balcón fue serrada. "
            "El niño prodigio escuchó el grito de caída, pero pensó que era la televisión."
        )
    },
      {
        "id": 21,
        "title": "La escultura de carne",
        "description": "La víctima no fue asesinada, fue 'reorganizada'. Sus extremidades fueron cosidas en lugares incorrectos para formar una grotesca estatua humana en el centro del salón de baile.",
        "details": (
            "El mayordomo encontró hilo quirúrgico en el bolsillo del abrigo del vecino. "
            "El chef se quejó de que faltaban sus cuchillos de deshuesar más afilados. "
            "La jardinera notó que la tierra del invernadero olía a formol. "
            "El niño prodigio dibujó la 'estatua' días antes de que apareciera. "
            "La anciana cree que es una obra de arte moderno y la admira sin horror. "
            "El detective retirado vomitó al ver la precisión anatómica de los cortes. "
            "El periodista descubrió que la víctima estaba viva durante el proceso. "
            "El vecino tenía un manual de taxidermia abierto en su mesita de noche."
        )
    },
    {
        "id": 22,
        "title": "El banquete caníbal",
        "description": "Los invitados cenaron un estofado exquisito, solo para descubrir al final que la víctima desaparecida había sido el ingrediente principal. Su cabeza fue servida como postre en una bandeja de plata.",
        "details": (
            "El chef lloraba en la cocina mientras afilaba un hacha de carnicero. "
            "La anciana pidió repetir el plato, diciendo que la carne era muy tierna. "
            "El mayordomo sirvió el vino con manos temblorosas y manchadas de rojo seco. "
            "El periodista encontró un dedo humano en su copa de brandy. "
            "El vecino es un cazador que sabe despellejar presas en minutos. "
            "El niño prodigio se negó a comer porque 'la comida le habló'. "
            "La jardinera encontró restos de ropa ensangrentada en el compostador. "
            "El detective retirado notó que faltaban órganos específicos en los restos."
        )
    },
    {
        "id": 23,
        "title": "La caja de música humana",
        "description": "El cuerpo fue hallado abierto en canal, con sus órganos conectados a un mecanismo de relojería. Al dar cuerda, los pulmones y el corazón se movían al ritmo de una macabra melodía.",
        "details": (
            "El niño prodigio estaba fascinado con los engranajes insertados en el pecho. "
            "El vecino relojero había perdido sus herramientas de precisión esa mañana. "
            "El mayordomo escuchó un 'tic-tac' constante proveniente del cadáver. "
            "La anciana tarareaba la misma canción que tocaba el cuerpo. "
            "El periodista vio planos de anatomía mecánica en el cuarto del chef. "
            "La jardinera encontró venas usadas como cuerdas de violín en el suelo. "
            "El detective retirado identificó la técnica como una tortura medieval modernizada. "
            "El chef usó pinzas para extraer el hígado sin detener el mecanismo."
        )
    },
    {
        "id": 24,
        "title": "Los ojos del voyeur",
        "description": "La víctima fue encontrada atada a una silla frente a una pared llena de espejos. Sus párpados fueron cortados para que no pudiera cerrar los ojos ni siquiera al morir de terror.",
        "details": (
            "El periodista tenía una colección de fotos de ojos humanos en su cámara. "
            "El mayordomo limpió los espejos, pero dejó marcas de arrastre. "
            "La anciana dijo que la víctima 'ahora sí podía ver la verdad'. "
            "El vecino fue visto comprando gotas para dilatar las pupilas. "
            "El detective retirado encontró un bisturí oxidado bajo la alfombra. "
            "El niño prodigio jugaba a 'quien parpadea pierde' con el cadáver. "
            "El chef usó salmuera, lo que aumentó el dolor de la víctima. "
            "La jardinera podó las rosas con tijeras que tenían restos de pestañas."
        )
    },
    {
        "id": 25,
        "title": "La piel ajena",
        "description": "El cadáver apareció desollado con una precisión quirúrgica. Lo más terrorífico es que alguien está caminando por la mansión vistiendo la piel de la víctima como un traje.",
        "details": (
            "El mayordomo notó que el 'señor' sudaba sangre y olía a carne cruda. "
            "La jardinera encontró la piel del rostro secándose en el tendero. "
            "El detective retirado vio una cremallera cosida en la espalda del sospechoso. "
            "El niño prodigio preguntó por qué el vecino tenía dos ombligos hoy. "
            "La anciana acarició el brazo del asesino y notó que estaba frío y húmedo. "
            "El chef encontró restos de dermis en el triturador de basura. "
            "El periodista notó que la ropa le quedaba grande a la víctima, o a quien fingía serlo. "
            "El vecino tenía un kit de curtido de pieles oculto en su garaje."
        )
    },
    {
        "id": 26,
        "title": "El jardín de los gritos",
        "description": "Las víctimas fueron enterradas hasta el cuello en el jardín y rociadas con feromonas para atraer insectos y roedores, siendo devoradas vivas lentamente.",
        "details": (
            "La jardinera cuidaba las cabezas como si fueran coles, regándolas. "
            "El vecino criaba ratas hambrientas en el sótano. "
            "El mayordomo escuchó los gritos pero subió el volumen de la música clásica. "
            "El niño prodigio capturaba hormigas rojas y las soltaba cerca de las caras. "
            "El periodista grabó el sonido de la agonía para un podcast de terror. "
            "La anciana pensó que las cabezas eran adornos de Halloween muy realistas. "
            "El chef usó miel para cubrir los rostros de las víctimas. "
            "El detective retirado encontró un cronómetro midiendo el tiempo de muerte."
        )
    },
    {
        "id": 27,
        "title": "La marioneta de sangre",
        "description": "La víctima fue colgada del techo del vestíbulo con alambres de púas atravesando sus articulaciones. El asesino la manipulaba desde arriba, haciéndola 'bailar' mientras se desangraba.",
        "details": (
            "El niño prodigio aplaudía al ver al cuerpo moverse espasmódicamente. "
            "El mayordomo tenía las manos llenas de cortes por manipular los alambres. "
            "El vecino es experto en nudos y poleas. "
            "La anciana pidió que la marioneta hiciera una reverencia final. "
            "El periodista notó que los alambres estaban conectados a la lámpara de araña. "
            "El chef se resbaló en el charco de sangre que se formaba bajo el cuerpo. "
            "La jardinera usó guantes gruesos para no pincharse con las púas. "
            "El detective retirado disparó a la cuerda para acabar con el sufrimiento."
        )
    },
    {
        "id": 28,
        "title": "La transfusión inversa",
        "description": "La víctima fue conectada a una máquina que, en lugar de darle sangre, la reemplazó lentamente con ácido corrosivo mientras estaba consciente y atada.",
        "details": (
            "El chef tenía botellas de ácido industrial para limpiar hornos. "
            "El detective retirado reconoció las marcas de agujas en los brazos. "
            "El vecino, un ex-químico, diseñó la mezcla para que no matara al instante. "
            "El mayordomo vigilaba el flujo del líquido como si fuera un experimento. "
            "La anciana se quejó del olor a 'huevo podrido' (azufre) en la habitación. "
            "El niño prodigio calculó cuánto tiempo tardaría en disolverse el corazón. "
            "El periodista tomó fotos del cambio de color en las venas de la víctima. "
            "La jardinera usó la sangre drenada para regar sus orquídeas negras."
        )
    },
    {
        "id": 29,
        "title": "El parto de la bestia",
        "description": "Se encontró el cuerpo de un hombre con el abdomen abierto brutalmente. Dentro de él, alguien había cosido un animal vivo (una rata o un gato) que intentaba salir arañando desde el interior.",
        "details": (
            "La anciana decía que escuchaba maullidos provenientes del estómago del muerto. "
            "El chef notó que faltaba el gato de la cocina. "
            "El vecino tenía hilo de pescar grueso y agujas curvas ensangrentadas. "
            "El niño prodigio miraba fijamente el movimiento bajo la piel del cadáver. "
            "El mayordomo limpió las huellas de garras en el suelo alrededor del cuerpo. "
            "El periodista escribió 'bizarro' en su libreta con mano temblorosa. "
            "La jardinera atrapó al animal cuando finalmente logró salir. "
            "El detective retirado nunca había visto tal crueldad en 30 años de servicio."
        )
    },
    {
        "id": 30,
        "title": "El rompecabezas humano",
        "description": "La víctima fue cortada en cubos perfectos de 10x10 cm. Los trozos fueron numerados y esparcidos por la casa para que los invitados tuvieran que 'rearmar' al muerto.",
        "details": (
            "El niño prodigio resolvió el rompecabezas en tiempo récord. "
            "El chef usó una cortadora de fiambre industrial para lograr la precisión. "
            "El mayordomo encontró la pieza número 4 (la nariz) en el buzón. "
            "La anciana guardó un cubo en su bolso pensando que era un regalo. "
            "El vecino ayudó a mover los trozos más pesados del torso. "
            "El periodista encontró la pieza faltante dentro de la pecera. "
            "La jardinera se negó a tocar los trozos porque manchaban la alfombra. "
            "El detective retirado notó que faltaba el corazón: el asesino se lo quedó."
        )
    }
  
]


NPCS = {
    "npc1": "Eres un mayordomo educado pero reservado.",
    "npc2": "Eres una jardinera que oculta cosas.",
    "npc3": "Eres un vecino curioso.",
    "npc4": "Eres un detective retirado, sabio pero escéptico.",
    "npc5": "Eres una periodista ambiciosa.",
    "npc6": "Eres un chef excéntrico y observador.",
    "npc7": "Eres una anciana sabia, algo olvidadiza.",
    "npc8": "Eres un niño prodigio muy observador."
}

# ---------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------

def reset_gamestate():
    """Crea un nuevo juego con un caso y asesino aleatorio."""
    GameState.objects.filter(id=1).delete()
    gs = GameState.objects.create(
        id=1,
        assassin=random.choice(list(NPCS.keys())),
        case_id=random.choice(CASES)["id"]
    )
    return gs


def get_gamestate():
    """Devuelve el estado actual sin modificarlo.
       Si no existe, crea uno nuevo."""
    try:
        return GameState.objects.get(id=1)
    except GameState.DoesNotExist:
        return reset_gamestate()


def get_current_case():
    gs = get_gamestate()
    for case in CASES:
        if case["id"] == gs.case_id:
            return case
    return None


# ---------------------------------------------
# PROMPT CREATION
# ---------------------------------------------

def get_npc_prompt(npc_id):
    gs = get_gamestate()
    assassin = gs.assassin
    case = get_current_case()

    # Contexto del caso
    case_context = (
        f"Caso: {case['title']}\n"
        f"Descripción: {case['description']}\n"
        f"Detalles conocidos: {case['details']}\n\n"
        "IMPORTANTE: Puedes ampliar, inferir o añadir detalles menores "
        "siempre que no contradigas los hechos principales.\n\n"
    )

    # Rol base del NPC
    npc_personality = NPCS[npc_id]

    # Inocentes vs Asesino
    if npc_id == assassin:
        role = (
            "Eres el asesino. Debes mentir con creatividad, ofrecer coartadas nuevas, "
            "desviar sospechas y generar detalles falsos que parezcan plausibles. "
            "Tu objetivo es confundir."
        )
    else:
        role = (
            "Eres inocente. Ayudas con sinceridad e intentas aportar "
            "recuerdos, impresiones, pistas nuevas o teorías razonables "
            "que no están explícitamente en los detalles pero que podrían ayudar al jugador."
        )

    # Forma de hablar
    style = (
        "Responde siempre en primera persona, como si realmente estuvieras allí. "
        "NO pongas tu nombre ni etiquetas. No repitas literalmente las frases del caso. "
        "Cada respuesta debe aportar algo nuevo: una observación, un detalle, "
        "una emoción, una suposición o un recuerdo."
    )

    return f"{case_context}{npc_personality} {role} {style}"


# ---------------------------------------------
# NPC RESPONSE GENERATION
# ---------------------------------------------

def get_npc_response(npc_id, history):
    """
    history debe ser una lista de mensajes:
    [
        {"role": "user", "content": "texto del jugador"},
        {"role": "assistant", "content": "respuesta anterior del NPC"},
        ...
    ]
    """
    if not isinstance(history, list):
        # Fallback en caso de que aún lo envíes como texto
        history = [{"role": "user", "content": history}]

    system_prompt = get_npc_prompt(npc_id)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",             
        messages=messages,
        temperature=0.80,                
        max_tokens=250,
        presence_penalty=0.8,             
        frequency_penalty=0.4
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------
# ACCUSATION CHECK
# ---------------------------------------------

def check_accusation(npc_id):
    gs = get_gamestate()
    if npc_id == gs.assassin:
        return True, f"¡Correcto! {npc_id} es el culpable. Has resuelto el caso."
    else:
        return False, f"No, {npc_id} no es el culpable. Sigue investigando."
