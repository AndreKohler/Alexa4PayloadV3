# Alexa4PayloadV3
Alexa4PayloadV3

Die Daten des Plugin müssen in den Ordner /usr/local/smarthome/plugins/alexa4p3/ (wie gewohnt)
Die Rechte entsprechend setzen.

Um die neuen Payload-Features nutzen zu können muss lediglich die Skill-Version in der Amazon Hölle auf
PayLoad Version 3 umgestellt werden. Alles andere kann unverändert weiterverwendet werden.

Das Plugin muss in der plugin.yaml eingefügt werden :

<pre><code>    
Alexa4P3:
    class_name: Alexa4P3
    class_path: plugins.alexa4p3
    service_port: 9000
</code></pre>

Das ursprünglich Plugin kann deaktiviertwerden :

<pre><code>    
#alexa:
#    class_name: Alexa
#    class_path: plugins.alexa
#    service_port: 9000
</code></pre>

Idealerweise kopiert man sich seine ganzen conf/yaml Files aus dem Items-Verzeichnis.
und ersetzt dann die "alten" Actions durch die "Neuen". Nachdem der Skill auf Payload V3 umgestellt wurde
muss ein Discover durchgeführt werden. Im besten Fall funktioniert dann alles wie gewohnt.

In den Items sind die "neuen" V3 Actions zu definieren :

Zum Beispiel :

PayloadV2 : turnon
PayloadV3 : TurnOn

Die Actions unterscheiden sich zwischen Payload V2 und V3 oft nur durch Gross/Klein-Schreibung

Optional kann im Item angegeben werden welches Icon in der Alexa-App verwendet werden soll :

        alexa_icon = "LIGHT"

default = "Switch" (vergleiche : https://developer.amazon.com/docs/device-apis/alexa-discovery.html#display-categories )

Die sonstigen Parameter aus dem ursprüngliche Alexa-Plugin bleiben erhalten und werden weiterhin genutzt.
(alexa_name / alexa_device / alexa_description / alexa_actions /alexa_item_range)

Beispiel für Item:

<pre><code>    
[OG]
    [[Flur]]
        name = Flur_Obeschoss
        [[[Spots]]]
        alexa_name = "Licht Flur OG"
        alexa_device = Licht_Flur_OG
	alexa_actions = "TurnOn TurnOff"
        alexa_icon = "LIGHT"
        type = bool
        visu_acl = rw
        knx_dpt = 1
        knx_listen = 1/1/107
        knx_send = 1/1/107
        enforce_updates = true
            [[[[dimmen]]]]
                type = num
                alexa_device = Licht_Flur_OG 
               	alexa_actions = "AdjustBrightness SetBrightness"                
                alexa_retrievable= True
                alexa_item_range = 0-255
                visu_acl = rw
                knx_dpt = 5
                knx_listen = 1/4/100
                knx_send = 1/3/100
                knx_init = 1/4/100
                enforce_updates = true
        [[[Treppe]]]
        type = bool
        visu_acl = rw
        knx_dpt = 1
        knx_listen = 1/1/133
        knx_send = 1/1/133
        enforce_updates = true

</code></pre>

Um weitere Actions hinzuzufügen muss die Datei p3_actions.py mit den entsprechenden Actions ergänzt werden.
(wie ursprünglich als selbstregistrierende Funktion)

</pre><code>

@alexa('action_name', 'directive_type', 'response_type','namespace') // in der Datei p3_actions.py
@alexa('TurnOn', 'TurnOn', 'powerState','Alexa.PowerController') // in der Datei p3_actions.py

</code></pre>

Hierbei ist zu beachten, das in für die jeweilige Action die folgenden Paramter übergeben werden :

action_name     = neuer Action-Name z.B.: TurnOn (gleich geschrieben wie in der Amazon-Beschreibung - auch Gross/Klein) 

directive_type  = gleich wie action_name (nur notwendig wegen Kompatibilität V2 und V3)

response_type   = Property des Alexa Interfaces
siehe Amazon z.B. : https://developer.amazon.com/docs/device-apis/alexa-brightnesscontroller.html#properties

namespace       = NameSpace des Alexa Interfaces
siehe Amazon z.B.: https://developer.amazon.com/docs/device-apis/alexa-brightnesscontroller.html#directives

In der "service.py" muss für den ReportState der Rückgabewert für die neue Action hinzugefügt werden.
(siehe Quellcode)



