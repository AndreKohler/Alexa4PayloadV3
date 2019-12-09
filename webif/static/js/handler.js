//*******************************************
// Button Handler CreateYaml
//*******************************************

function CreateYaml()
{

// Definition for Alexa-Response
 CrLf = '\n'
 indent = "    "
 YAML = "$ItemName:" + CrLf
 YAML +=indent + "alexa_description: $description" + CrLf
 YAML +=indent + "alexa_name: $alexa_name" + CrLf
 YAML +=indent + "alexa_device: $alexa_device" + CrLf
 YAML +=indent + "alexa_auth_cred: '$alexa_auth_user:$alexa_auth_pwd'" + CrLf
 YAML +=indent + "alexa_icon: CAMERA" + CrLf
 YAML +=indent + "alexa_actions: InitializeCameraStreams" + CrLf
 YAML +=indent + "alexa_camera_imageUri: $Image_Uri " + CrLf
 YAML +=indent + "$StreamInfo" + CrLf
 YAML +=indent + "alexa_csc_uri: '$Stream_IP'"+ CrLf
 YAML +=indent + "alexa_csc_proxy_uri: $proxy_Url" + CrLf
 YAML +=indent + "alexa_proxy_credentials: '$credentials'"

// Definition for Stream
 myStream = '{ "protocols":["$protocol"], "resolutions":[{"width":$width,"height":$height}], "authorizationTypes":["authorization"], "videoCodecs":["$video"], "audioCodecs":["$audio"] }'

 // Get Values from WebPage
 if (document.getElementById("enable_stream_1").checked != true)
    {
      alert("You have to activate minimum one stream")
      return
    }

 Values2Replace  ={ '$ItemName':'Cam_Name',
                    '$description':'Alexa_Description',
                    '$alexa_name':'Alexa_Name',
                    '$alexa_device':'Alexa_Device',
                    '$alexa_auth_user':'user',
                    '$alexa_auth_pwd': 'pwd',
                    '$Image_Uri':'Image_Url',
                    '$proxy_Url':'Proxy_Url',
                    '$credentials':'user'}

 for ( var key in Values2Replace)
 {
    if (Values2Replace.hasOwnProperty(key))
     {
      myValue = document.getElementById(Values2Replace[key]).value
      YAML = YAML.replace(key, myValue)
     }
 }
 for ( i=1; i <=3; i++)
    {
      // Skip not enabled Streams
      if (document.getElementById("enable_stream_"+String(i)).checked == true)
        {
          // Create Stream-String
          console.log("Got info to setup Streamstring for : "+ String(i))
        }
    }


 yaml_resultCodeMirror.setValue(YAML)

}


