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

Optional kann im Item angegeben werden ob es durch Amazon abgefragt werden kann :
<pre><code>    
	alexa_retrievable = true
</code></pre>

default = false


Die sonstigen Parameter aus dem ursprüngliche Alexa-Plugin bleiben erhalten und werden weiterhin genutzt.
(alexa_name / alexa_device / alexa_description / alexa_actions /alexa_item_range)

Beispiel für Item im .conf-Format:

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

im .yaml-Format :

<pre><code>    
%YAML 1.1
---

OG:

    Flur:
        name: Flur_Obeschoss

        Spots:
            alexa_name: Licht Flur OG
            alexa_device: Licht_Flur_OG
            alexa_actions: TurnOn TurnOff
            alexa_icon: LIGHT
            type: bool
            visu_acl: rw
            knx_dpt: 1
            knx_listen: 1/1/107
            knx_send: 1/1/107
            enforce_updates: 'true'

            dimmen:
                type: num
                alexa_device: Licht_Flur_OG
                alexa_actions: AdjustBrightness SetBrightness
                alexa_retrievable: 'True'
                alexa_item_range: 0-255
                visu_acl: rw
                knx_dpt: 5
                knx_listen: 1/4/100
                knx_send: 1/3/100
                knx_init: 1/4/100
                enforce_updates: 'true'

        Treppe:
            type: bool
            visu_acl: rw
            knx_dpt: 1
            knx_listen: 1/1/133
            knx_send: 1/1/133
            enforce_updates: 'true'
</code></pre>


Um weitere Actions hinzuzufügen muss die Datei p3_actions.py mit den entsprechenden Actions ergänzt werden.
(wie ursprünglich als selbstregistrierende Funktion)

<pre><code>

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

# Alexa-ThermostatController + Thermosensor hinzugefügt


Es kann nun via Alexa die Solltemperatur verändert werden und der Modus des Thermostaten kann umgestellt werden.
Die Konfiguration der YAML-Datei sieht wie folgt aus

Es müssen beim Thermostaten in YAML die Einträge für :
alexa_thermo_config, alexa_icon, alexa_actions vorgenommen werden.

alexa_thermo_config = "0:AUTO 1:HEAT 2:COOL 3:ECO 4:ECO"
Hierbei stehen die Werte für für die KNX-Werte von DPT 20

<pre><code>   
$00 Auto
$01 Comfort
$02 Standby
$03 Economy
$04 Building Protection
</code></pre>

Die Modi AUTO / HEAT / COOL / ECO / OFF entsprechen den Alexa-Befehlen aus dem Theromstatconroller
siehe Amazon : https://developer.amazon.com/docs/device-apis/alexa-property-schemas.html#thermostatmode

<pre><code>   
alexa_icon = "THERMOSTAT" = Thermostatcontroller

alexa_icon = "TEMPERATURE_SENSOR" = Temperatursensor
</code></pre>

Der Temperartursensor wird beim Item der Ist-Temperatur hinterlegt.
Der Thermostatconroller wird beim Thermostat-Item hinterlegt. An Amazon werden die Icons als Array übertragen.
Die Abfrage der Ist-Temperatur muss mit der Action  "ReportTemperature" beim Item der Ist-Temperatur hinterlegt werden.

<pre><code>   
alexa_actions : "ReportTemperature"
</code></pre>

Alexa wie ist die Temperatur in der Küche ?

<pre><code>  
alexa_actions = "SetTargetTemperature AdjustTargetTemperature" 
</code></pre>

Hiermit werden die Solltemperatur auf einen Wert gesetzt oder die Temperatur erhöht.
Diese Actions müssen beim Item des Soll-Wertes des Thermostaten eingetragen werden

Alexa erhöhe die Temperatur in der Küche um zwei Grad

Alexa stelle die Temperatur in der Küche auf zweiundzwanzig Grad


alexa_actions = "SetThermostatMode"
Hier wird das Item des Modus angesteuert. Diese Action muss beim Item des Thermostat-Modes eingetragen werden.
Falls keine Modes angegeben wurden wird "0:AUTO" als default gesetzt

Alexa stelle den Thermostaten Küche auf Heizen


<pre><code>   
%YAML 1.1
---
EG:
    name: EG
    sv_page: cat_seperator
    Kueche:
        temperature:
            name: Raumtemperatur
            alexa_description : "Küche Thermostat"
            alexa_name : "Küche Thermostat"
            alexa_device : thermo_Kueche 
            alexa_thermo_config : "0:AUTO 1:HEAT 2:OFF 3:ECO 4:ECO"
            alexa_icon : "THERMOSTAT"
            actual:
                type: num
                sqlite: 'yes'
                visu: 'yes'
                knx_dpt: 9
                initial_value: 21.8
                alexa_device : thermo_Kueche 
                alexa_retrievable : True
                alexa_actions : "ReportTemperature"
                alexa_icon : "TEMPERATURE_SENSOR"
            SollBasis:
                type: num
                visu_acl: rw
                knx_dpt: 9
                initial_value: 21.0
                alexa_device : thermo_Kueche 
                alexa_actions : "SetTargetTemperature AdjustTargetTemperature"
            Soll:
                type: num
                sqlite: 'yes'
                visu: 'yes'
                visu_acl: rw
                knx_dpt: 9
                initial_value: 21.0
                alexa_device : thermo_Kueche 
            mode:
                type: num
                visu_acl: rw
                knx_dpt: 20
                initial_value: 1.0
                alexa_device : thermo_Kueche 
                alexa_actions : "SetThermostatMode"
            state:
                type: bool
                visu_acl: r
                sqlite: 'yes'
                visu: 'yes'
                knx_dpt: 1
                cache: true
                alexa_device : thermo_Kueche 
</code></pre>

Beispiel für einen MDT-Glastron, der Modus wird auf Objekt 12 in der ETS-Parametrierung gesendet (Hierzu eine entsprechende 
Gruppenadresse anlegen)

<pre><code>   
 temperature:
            name: Raumtemperatur
            alexa_description : "Küche Thermostat"
            alexa_name : "Küche Thermostat"
            alexa_device : thermo_Kueche 
            alexa_thermo_config : "0:AUTO 1:HEAT 2:OFF 3:ECO 4:ECO"
            alexa_icon : "THERMOSTAT"
        plan:
            type: num
            visu_acl: rw
            database@mysqldb: init
            knx_dpt: 9
            knx_send: 2/1/2
            knx_listen: 2/1/2
            knx_cache: 2/1/2
            alexa_device : thermo_Kueche 
            alexa_actions : "SetTargetTemperature AdjustTargetTemperature"
        state:
            type: num
            visu_acl: r
            database@mysqldb: init
            knx_dpt: 9
            knx_listen: 2/1/1
            knx_cache: 2/1/1
            alexa_device : thermo_Kueche 
            alexa_retrievable : True
            alexa_actions : "ReportTemperature"
            alexa_icon : "TEMPERATURE_SENSOR"
        mode:
            type: num
            visu_acl: rw
            knx_dpt: 20
            initial_value: 1.0
            alexa_device : thermo_Kueche 
            alexa_actions : "SetThermostatMode"

        humidity:
            type: num
            visu_acl: r
            database@mysqldb: init
            knx_dpt: 9
            knx_listen: 2/1/5
            knx_cache: 2/1/5

        actor_state:
            type: num
            visu_acl: r
            database@mysqldb: init
            knx_dpt: '5.001'
            knx_listen: 2/1/3
            knx_cache: 2/1/3

</code></pre>
